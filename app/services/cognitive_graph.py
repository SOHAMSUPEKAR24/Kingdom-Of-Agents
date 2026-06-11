import logging
import networkx as nx
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy import select

from app.models import schemas
from app.models.schemas import (
    SQLTask, SQLAgentGenome, SQLToolVersion, SQLReinforcementEvent, SQLKingdomDoctrine,
    TaskSchema, AgentGenomeSchema, ToolVersionSchema
)
from app.services.memory_service import memory_service

logger = logging.getLogger("antigravity.cognitive_graph")

class CognitiveGraphService:
    def __init__(self):
        pass

    async def infer_relationships(self) -> List[Dict[str, Any]]:
        """
        Scans active data (relational DB state & memory topology) to automatically assert
        cognitive relationships such as MUTATED_FROM, TRUST_ANOMALY, and FAILURE_PATH.
        """
        inferred = []
        now = datetime.utcnow()

        logger.info("🧠 [COGNITIVE GRAPH] Initiating automated relationship inference...")

        async with schemas.async_session() as session:
            # 1. Infer MUTATED_FROM from agent genomes
            stmt_genomes = select(SQLAgentGenome).where(SQLAgentGenome.parent_id.isnot(None))
            res_genomes = await session.execute(stmt_genomes)
            genomes = res_genomes.scalars().all()
            for g in genomes:
                source = g.id
                target = g.parent_id
                # Add relationship to topology
                await memory_service.store_topology_relation(source, target, "MUTATED_FROM")
                inferred.append({
                    "source": source,
                    "target": target,
                    "type": "MUTATED_FROM",
                    "reason": f"Genome lineage link from agent {g.agent_id or g.id} to parent {g.parent_id}"
                })

            # 2. Infer MUTATED_FROM from tool versions
            stmt_tools = select(SQLToolVersion).where(SQLToolVersion.parent_tool.isnot(None))
            res_tools = await session.execute(stmt_tools)
            tools = res_tools.scalars().all()
            for t in tools:
                source = t.id
                target = t.parent_tool
                await memory_service.store_topology_relation(source, target, "MUTATED_FROM")
                inferred.append({
                    "source": source,
                    "target": target,
                    "type": "MUTATED_FROM",
                    "reason": f"Tool evolution link from version {t.version} to parent {t.parent_tool}"
                })

            # 3. Infer TRUST_ANOMALY for low-trust genomes
            stmt_anomalies = select(SQLAgentGenome).where(SQLAgentGenome.trust_metric < 0.7)
            res_anomalies = await session.execute(stmt_anomalies)
            anomalous_genomes = res_anomalies.scalars().all()
            for ag in anomalous_genomes:
                source = ag.id
                target = ag.house
                await memory_service.store_topology_relation(source, target, "TRUST_ANOMALY")
                inferred.append({
                    "source": source,
                    "target": target,
                    "type": "TRUST_ANOMALY",
                    "reason": f"Agent {ag.agent_id or ag.id} trust metric ({ag.trust_metric}) dropped below warning threshold (0.7)"
                })

            # 4. Infer FAILURE_PATH for failed dependent tasks
            stmt_failed = select(SQLTask).where(SQLTask.status == "FAILED")
            res_failed = await session.execute(stmt_failed)
            failed_tasks = res_failed.scalars().all()
            for ft in failed_tasks:
                # Find downstream dependencies that might be impacted
                stmt_dependent = select(SQLTask)
                res_dep = await session.execute(stmt_dependent)
                all_tasks = res_dep.scalars().all()
                for t in all_tasks:
                    if ft.id in t.dependencies:
                        await memory_service.store_topology_relation(t.id, ft.id, "FAILURE_PATH")
                        inferred.append({
                            "source": t.id,
                            "target": ft.id,
                            "type": "FAILURE_PATH",
                            "reason": f"Cascade risk detected: Dependent task {t.id} blocked by failed antecedent task {ft.id}"
                        })

        logger.info(f"🧠 [COGNITIVE GRAPH] Inference complete. Asserted {len(inferred)} new relationships.")
        return inferred

    async def get_lineage_trace(self, node_id: str) -> List[str]:
        """
        Traverses MUTATED_FROM/lineage relationships to trace ancestors of a node using Neo4j.
        """
        logger.debug(f"Tracing genetic ancestry lineage for: {node_id}")
        trace = [node_id]
        
        if not memory_service.neo4j_driver:
            logger.warning("Neo4j offline. Cannot trace lineage.")
            return trace
            
        try:
            async with memory_service.neo4j_driver.session() as session:
                cypher = """
                MATCH p=(n:Node {id: $node_id})-[:RELATION* {type: 'MUTATED_FROM'}]->(ancestor:Node)
                RETURN [x in nodes(p) | x.id] as path
                ORDER BY length(p) DESC LIMIT 1
                """
                res = await session.run(cypher, node_id=node_id)
                record = await res.single()
                if record:
                    return record["path"]
        except Exception as e:
            logger.error(f"Neo4j lineage trace failed: {e}")
            
        return trace

    async def get_bottleneck_centrality(self) -> Dict[str, float]:
        """
        Calculates network degree centrality over active topology nodes using Neo4j.
        Identifies hot-spots and governance bottlenecks.
        """
        if not memory_service.neo4j_driver:
            return {}
            
        try:
            async with memory_service.neo4j_driver.session() as session:
                cypher = """
                MATCH (n:Node)-[r]-()
                RETURN n.id as id, count(r) as degree
                ORDER BY degree DESC LIMIT 20
                """
                res = await session.run(cypher)
                centrality = {}
                async for record in res:
                    centrality[record["id"]] = float(record["degree"])
                return centrality
        except Exception as e:
            logger.error(f"Neo4j bottleneck centrality failed: {e}")
            return {}

# Global Cognitive Graph Service Instance
cognitive_graph = CognitiveGraphService()
