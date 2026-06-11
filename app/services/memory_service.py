import asyncio
import logging
import uuid
import math
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from neo4j import GraphDatabase, AsyncGraphDatabase

from app.core.config import settings
from app.models import schemas
from app.models.schemas import (
    SQLTask, SQLAgentState, SQLLog, SQLMemoryItem,
    TaskSchema, AgentStateSchema, LogSchema, MemoryItemSchema
)

logger = logging.getLogger("antigravity.memory_service")

class MemoryService:
    def __init__(self):
        # Database engines connections
        self.qdrant_client: Optional[QdrantClient] = None
        self.neo4j_driver = None

    async def connect(self):
        """Attempts connection to external databases, no mock fallbacks."""
        # 1. Connect Qdrant (Vector)
        try:
            url = settings.QDRANT_URL
            self.qdrant_client = QdrantClient(url=url, timeout=2.0)
            self.qdrant_client.get_collections()
            logger.info("Connected to Qdrant Vector DB successfully.")
            self._init_qdrant_collection()
        except Exception as e:
            logger.warning(f"Qdrant connection failed: {e}. Vector memory DEGRADED.")
            self.qdrant_client = None

        # 2. Connect Neo4j (Graph)
        try:
            self.neo4j_driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URL,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            async with self.neo4j_driver.session() as session:
                await session.run("RETURN 1")
            logger.info("Connected to Neo4j Graph DB successfully.")
        except Exception as e:
            logger.warning(f"Neo4j connection failed: {e}. Graph topology DEGRADED.")
            self.neo4j_driver = None

    async def disconnect(self):
        if self.neo4j_driver:
            await self.neo4j_driver.close()

    def _init_qdrant_collection(self):
        try:
            if not self.qdrant_client:
                return
            collections = self.qdrant_client.get_collections().collections
            exists = any(c.name == "kingdom_memories" for c in collections)
            if not exists:
                self.qdrant_client.create_collection(
                    collection_name="kingdom_memories",
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                logger.info("Created Qdrant collection 'kingdom_memories'")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")

    # ==========================================
    # RELATIONAL LONG-TERM MEMORY (Postgres/SQLite)
    # ==========================================

    async def store_task(self, task: TaskSchema):
        async with schemas.async_session() as session:
            db_task = SQLTask(
                id=task.id,
                parent_objective=task.parent_objective,
                title=task.title,
                assigned_house=task.assigned_house,
                assigned_soldier=task.assigned_soldier,
                status=task.status,
                input_data=task.input_data,
                output_data=task.output_data,
                dependencies=task.dependencies
            )
            await session.merge(db_task)
            await session.commit()
            logger.debug(f"Relational memory: Saved task '{task.id}' ({task.status})")

    async def get_task(self, task_id: str) -> Optional[TaskSchema]:
        async with schemas.async_session() as session:
            result = await session.execute(select(SQLTask).where(SQLTask.id == task_id))
            db_task = result.scalars().first()
            if db_task:
                return TaskSchema.model_validate(db_task)
            return None

    async def get_all_tasks(self) -> List[TaskSchema]:
        async with schemas.async_session() as session:
            result = await session.execute(select(SQLTask).order_by(SQLTask.created_at.desc()))
            db_tasks = result.scalars().all()
            return [TaskSchema.model_validate(t) for t in db_tasks]

    async def store_log(self, task_id: Optional[str], sender: str, message: str, priority: str = "INFO"):
        async with schemas.async_session() as session:
            db_log = SQLLog(
                task_id=task_id,
                sender=sender,
                message=message,
                priority=priority
            )
            session.add(db_log)
            await session.commit()
            logger.debug(f"Relational memory: Logged '{message[:40]}...' from {sender}")

    async def get_logs(self, limit: int = 100) -> List[LogSchema]:
        async with schemas.async_session() as session:
            result = await session.execute(select(SQLLog).order_by(SQLLog.timestamp.desc()).limit(limit))
            db_logs = result.scalars().all()
            return [LogSchema.model_validate(l) for l in db_logs]

    # ==========================================
    # VECTOR SEMANTIC MEMORY (Qdrant & Semantic Compression)
    # ==========================================

    def _generate_mock_embedding(self, text: str) -> List[float]:
        import re
        text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text_clean.split()
        vector = [0.0] * 384
        
        def det_hash(s: str) -> int:
            h = 0
            for char in s:
                h = (h * 31 + ord(char)) & 0xFFFFFFFF
            return h

        for word in words:
            val = det_hash(word)
            for idx in range(3):
                pos = (val + idx * 79) % 384
                vector[pos] += 1.0
            if len(word) > 4:
                prefix = word[:4]
                val_pref = det_hash(prefix)
                for idx in range(2):
                    pos = (val_pref + idx * 79) % 384
                    vector[pos] += 0.5
        sq_sum = sum(x**2 for x in vector)
        if sq_sum > 0:
            norm = math.sqrt(sq_sum)
            vector = [x / norm for x in vector]
        else:
            vector[0] = 1.0
        return vector

    async def store_semantic_memory(self, title: str, raw_content: str, memory_type: str, capability: str = "UNKNOWN", artifact_path: str = None) -> MemoryItemSchema:
        compressed = self._compress_semantically(raw_content)
        orig_len = len(raw_content)
        comp_len = len(compressed)
        ratio = (comp_len / orig_len) if orig_len > 0 else 1.0
        stats = {
            "original": orig_len,
            "compressed": comp_len,
            "ratio": round(ratio, 3),
            "retrieval_count": 0
        }

        memory_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        async with schemas.async_session() as session:
            db_mem = SQLMemoryItem(
                id=memory_id,
                title=title,
                raw_content=raw_content,
                compressed_content=compressed,
                compression_ratio=stats,
                memory_type=memory_type,
                created_at=timestamp
            )
            session.add(db_mem)
            await session.commit()

        vector = self._generate_mock_embedding(f"{title} {compressed}")

        if self.qdrant_client:
            try:
                self.qdrant_client.upsert(
                    collection_name="kingdom_memories",
                    points=[
                        PointStruct(
                            id=memory_id,
                            vector=vector,
                            payload={
                                "title": title,
                                "compressed_content": compressed,
                                "memory_type": memory_type,
                                "capability": capability,
                                "artifact_path": artifact_path,
                                "timestamp": timestamp.isoformat(),
                                "retrieval_count": 0
                            }
                        )
                    ]
                )
            except Exception as e:
                logger.error(f"Failed Qdrant insertion: {e}. Vector memory is DEGRADED.")
        else:
            logger.warning(f"Skipping Qdrant storage for {memory_id} (Qdrant offline)")

        logger.info(f"💾 Stored Semantic Memory: '{title}' (Ratio: {stats['ratio']})")
        return MemoryItemSchema(
            id=memory_id,
            title=title,
            raw_content=raw_content,
            compressed_content=compressed,
            compression_ratio=stats,
            memory_type=memory_type,
            created_at=timestamp
        )

    def _compress_semantically(self, text: str) -> str:
        lines = text.split("\n")
        non_empty = [l.strip() for l in lines if l.strip()]
        if len(non_empty) <= 2:
            return text
        compressed_lines = []
        for line in non_empty:
            if line.startswith("#") or "error" in line.lower() or "success" in line.lower() or "lesson" in line.lower() or "critical" in line.lower():
                compressed_lines.append(line)
        if not compressed_lines:
            compressed_lines = [non_empty[0], "...", non_empty[-1]]
        return " | ".join(compressed_lines)

    async def search_semantic_memories(self, query: str, limit: int = 5, capability: str = None) -> List[Dict[str, Any]]:
        query_vector = self._generate_mock_embedding(query)
        decay_constant = 0.05
        now = datetime.utcnow()

        results = []
        if self.qdrant_client:
            try:
                from qdrant_client.http.models import Filter, FieldCondition, MatchValue
                query_filter = None
                if capability:
                    query_filter = Filter(
                        must=[
                            FieldCondition(
                                key="capability",
                                match=MatchValue(value=capability)
                            )
                        ]
                    )
                    
                hits = self.qdrant_client.search(
                    collection_name="kingdom_memories",
                    query_vector=query_vector,
                    query_filter=query_filter,
                    limit=limit * 2
                )
                for hit in hits:
                    ts_str = hit.payload.get("timestamp")
                    created_at = datetime.fromisoformat(ts_str) if ts_str else now
                    retrieval_cnt = hit.payload.get("retrieval_count", 0)
                    
                    delta_t = (now - created_at).total_seconds() / 86400.0
                    decay_factor = math.exp(-decay_constant * delta_t)
                    utility_bonus = 1.0 + math.log(retrieval_cnt + 1.0)
                    discounted_score = hit.score * decay_factor * utility_bonus
                    
                    results.append({
                        "id": str(hit.id),
                        "raw_score": hit.score,
                        "score": round(discounted_score, 4),
                        "title": hit.payload.get("title"),
                        "content": hit.payload.get("compressed_content"),
                        "memory_type": hit.payload.get("memory_type"),
                        "capability": hit.payload.get("capability"),
                        "artifact_path": hit.payload.get("artifact_path"),
                        "retrieval_count": retrieval_cnt,
                        "timestamp": created_at
                    })
            except Exception as e:
                logger.error(f"Qdrant search failed: {e}")
        else:
            logger.warning("Skipping Qdrant search (Qdrant offline)")
        
        results.sort(key=lambda x: x["score"], reverse=True)
        top_results = results[:limit]

        for res in top_results:
            memory_id = res["id"]
            try:
                async with schemas.async_session() as session:
                    db_item = await session.get(SQLMemoryItem, memory_id)
                    if db_item:
                        ratio_data = dict(db_item.compression_ratio or {})
                        cnt = ratio_data.get("retrieval_count", 0) + 1
                        ratio_data["retrieval_count"] = cnt
                        db_item.compression_ratio = ratio_data
                        await session.commit()
            except Exception as e:
                logger.error(f"Failed to increment SQL retrieval count: {e}")
                
            if self.qdrant_client:
                try:
                    retrieved_point = self.qdrant_client.retrieve(collection_name="kingdom_memories", ids=[memory_id])
                    if retrieved_point:
                        payload = retrieved_point[0].payload
                        cnt = payload.get("retrieval_count", 0) + 1
                        payload["retrieval_count"] = cnt
                        self.qdrant_client.set_payload(
                            collection_name="kingdom_memories",
                            payload={"retrieval_count": cnt},
                            points=[memory_id]
                        )
                except Exception as e:
                    logger.error(f"Failed to update Qdrant payload retrieval_count: {e}")
                    
        return top_results

    # ==========================================
    # GRAPH TOPOLOGY MEMORY (Neo4j & NetworkX)
    # ==========================================

    async def store_topology_relation(self, source_id: str, target_id: str, relation_type: str):
        if self.neo4j_driver:
            try:
                async with self.neo4j_driver.session() as session:
                    cypher = """
                    MERGE (s:Node {id: $source_id})
                    ON CREATE SET s.label = $source_id, s.type = 'SOLDIER'
                    MERGE (t:Node {id: $target_id})
                    ON CREATE SET t.label = $target_id, t.type = 'TASK'
                    MERGE (s)-[r:RELATION {type: $rel_type}]->(t)
                    RETURN count(r)
                    """
                    await session.run(cypher, source_id=source_id, target_id=target_id, rel_type=relation_type)
            except Exception as e:
                logger.error(f"Neo4j failed topology update: {e}")
        else:
            logger.warning("Skipping Neo4j store (Neo4j offline). Using SQLite fallback.")
            try:
                from app.models.schemas import SQLTopologyNode, SQLTopologyEdge, async_session
                async with async_session() as session:
                    # Upsert source
                    s_node = await session.get(SQLTopologyNode, source_id)
                    if not s_node:
                        s_node = SQLTopologyNode(id=source_id, label=source_id, type="SOLDIER")
                        session.add(s_node)
                    # Upsert target
                    t_node = await session.get(SQLTopologyNode, target_id)
                    if not t_node:
                        t_node = SQLTopologyNode(id=target_id, label=target_id, type="TASK")
                        session.add(t_node)
                    # Add edge
                    edge = SQLTopologyEdge(source_id=source_id, target_id=target_id, rel_type=relation_type)
                    session.add(edge)
                    await session.commit()
            except Exception as e:
                logger.error(f"SQLite fallback topology update failed: {e}")

    async def retire_graph_soldier(self, soldier_id: str):
        if self.neo4j_driver:
            try:
                async with self.neo4j_driver.session() as session:
                    await session.run(
                        "MATCH (n:Node {id: $sid}) SET n.type = 'RETIRED_SOLDIER'",
                        sid=soldier_id
                    )
            except Exception as e:
                logger.error(f"Neo4j failed soldier retirement: {e}")
        else:
            try:
                from app.models.schemas import SQLTopologyNode, async_session
                async with async_session() as session:
                    s_node = await session.get(SQLTopologyNode, soldier_id)
                    if s_node:
                        s_node.type = 'RETIRED_SOLDIER'
                        await session.commit()
            except Exception as e:
                logger.error(f"SQLite fallback soldier retirement failed: {e}")

    async def get_topology(self) -> Dict[str, Any]:
        if not self.neo4j_driver:
            logger.warning("Neo4j offline. Using SQLite fallback topology.")
            try:
                from app.models.schemas import SQLTopologyNode, SQLTopologyEdge, async_session
                from sqlalchemy import select
                async with async_session() as session:
                    # Get nodes
                    res_nodes = await session.execute(select(SQLTopologyNode))
                    db_nodes = res_nodes.scalars().all()
                    nodes = [{"id": n.id, "label": n.label, "type": n.type, "details": n.details or ""} for n in db_nodes]

                    # Get edges
                    res_edges = await session.execute(select(SQLTopologyEdge))
                    db_edges = res_edges.scalars().all()
                    edges = [{"source": e.source_id, "target": e.target_id, "type": e.rel_type} for e in db_edges]
                    
                    return {"nodes": nodes, "edges": edges}
            except Exception as e:
                logger.error(f"SQLite fallback get_topology failed: {e}")
                return {"nodes": [], "edges": []}
            
        try:
            async with self.neo4j_driver.session() as session:
                result_nodes = await session.run("MATCH (n:Node) RETURN n.id as id, n.label as label, n.type as type, coalesce(n.details, '{}') as details")
                nodes = []
                async for record in result_nodes:
                    nodes.append({
                        "id": record["id"],
                        "label": record["label"] or record["id"],
                        "type": record["type"] or "UNKNOWN",
                        "details": record["details"] or ""
                    })

                result_edges = await session.run("MATCH (a:Node)-[r]->(b:Node) RETURN a.id as source, b.id as target, r.type as type")
                edges = []
                async for record in result_edges:
                    edges.append({
                        "source": record["source"],
                        "target": record["target"],
                        "type": record["type"] or "CONNECTS"
                    })
                return {"nodes": nodes, "edges": edges}
        except Exception as e:
            logger.error(f"Neo4j get_topology failed: {e}.")
            return {"nodes": [], "edges": []}

    async def synthesize_memory_clusters(self) -> int:
        # In reality mode, we skip Qdrant mock synthesis to avoid OOM, or implement true scroll
        logger.info("🧠 [MEMORY SYNTHESIS] Skipping synthesis without vector mock. (True pagination required for Qdrant)")
        return 0

# Global Memory Service Instance
memory_service = MemoryService()
