import logging
import uuid
import math
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import select

from app.models import schemas
from app.models.schemas import SQLKingdomDoctrine, SQLMemoryItem
from app.services.memory_service import memory_service

logger = logging.getLogger("antigravity.wisdom_engine")

class WisdomEngineService:
    def __init__(self):
        pass

    async def synthesize_doctrines_from_failures(self, similarity_threshold: float = 0.75) -> int:
        """
        Scans all failure memories, clusters related failures using semantic similarity,
        synthesizes general high-level operational doctrines for clusters,
        and persists them into the relational DB and semantic memory store.
        """
        logger.info("🧠 [WISDOM ENGINE] Initiating failure-pattern analysis and doctrine synthesis...")
        
        # 1. Fetch all FAILURE memories from local mock vector store and DB
        # To be robust, let's fetch from mock vector DB
        failures = [
            item for item in memory_service._mock_vector_db 
            if item["payload"].get("memory_type") == "FAILURE"
        ]
        
        if len(failures) < 2:
            logger.info("🧠 [WISDOM ENGINE] Insufficient failure memories to synthesize doctrines.")
            return 0
            
        doctrines_synthesized = 0
        clustered_ids = set()
        
        # 2. Perform simple clustering
        for i in range(len(failures)):
            item_i = failures[i]
            id_i = item_i["id"]
            if id_i in clustered_ids:
                continue
                
            cluster = [item_i]
            v1 = item_i["vector"]
            
            for j in range(i + 1, len(failures)):
                item_j = failures[j]
                id_j = item_j["id"]
                if id_j in clustered_ids:
                    continue
                    
                v2 = item_j["vector"]
                # Calculate cosine similarity
                score = sum(a * b for a, b in zip(v1, v2))
                if score >= similarity_threshold:
                    cluster.append(item_j)
            
            if len(cluster) >= 2:
                # We have a cluster of related failures! Synthesize a doctrine.
                titles = [c["payload"]["title"] for c in cluster]
                contents = [c["payload"]["compressed_content"] for c in cluster]
                
                # Extract general operational wisdom
                doctrine_text = (
                    f"DOCTRINE: Swarm operational patterns revealed recurring failures in related domains:\n"
                    f"Pattern: {', '.join(titles)}\n"
                    f"Operational Guidance: To prevent recursion faults, memory poisonings, or safety breaches, "
                    f"ensure all similar code modules execute within isolated AST sandboxes with explicitly validated boundary limits."
                )
                
                doctrine_id = str(uuid.uuid4())
                source_ids = [c["id"] for c in cluster]
                
                # A. Save in Relational Database
                try:
                    async with schemas.async_session() as session:
                        db_doctrine = SQLKingdomDoctrine(
                            id=doctrine_id,
                            doctrine_text=doctrine_text,
                            source_failure_clusters=source_ids,
                            created_at=datetime.utcnow()
                        )
                        session.add(db_doctrine)
                        await session.commit()
                except Exception as e:
                    logger.error(f"Failed to save doctrine in relational database: {e}")
                
                # B. Save in Vector Database as a strategy memory for future retrieval
                await memory_service.store_semantic_memory(
                    title=f"Kingdom Wisdom Doctrine - {cluster[0]['payload']['title']}",
                    raw_content=doctrine_text,
                    memory_type="STRATEGY"
                )
                
                # C. Link in graph topology
                for c in cluster:
                    clustered_ids.add(c["id"])
                    await memory_service.store_topology_relation(c["id"], doctrine_id, "MUTATED_FROM")
                
                doctrines_synthesized += 1
                logger.info(f"🧠 [WISDOM SYNTHESIS SUCCESS] Created Doctrine '{doctrine_id}' from {len(cluster)} failures.")
                
        return doctrines_synthesized

wisdom_engine = WisdomEngineService()
