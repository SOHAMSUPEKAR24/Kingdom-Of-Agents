import logging
from typing import Dict, Any, Tuple, List
from datetime import datetime
import uuid
from sqlalchemy import select

from app.services.memory_service import memory_service
from app.models import schemas
from app.models.schemas import SQLAgentState, SQLAgentGenome

logger = logging.getLogger("antigravity.context_stability")

class ContextStabilityEngine:
    def __init__(self):
        # Dictionary tracking task execution frequency to isolate recursion loops
        # task_id -> execution_count
        self._task_execution_tracker: Dict[str, int] = {}
        
        # Track history of detected contradictions to cluster them and detect context poisoning
        self._detected_contradictions: List[Dict[str, Any]] = []
        
        # List of established constitutional truths or physical constraints
        self._physical_truths = [
            "Banned imports os, subprocess, sys must never be executed or bypassed",
            "Privilege escalation to root status is strictly rejected",
            "Dynamic code execution requires sandbox testing and permission approval",
            "Relational database schemas must maintain transaction integrity and never permit SQL injection"
        ]

    async def detect_contradiction(self, task_title: str, output_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Runs semantic contradiction audits against established physical truths and memory entries.
        Clusters contradiction events to proactively isolate context poisoning.
        Returns (has_contradiction, feedback_details).
        """
        output_str = str(output_data).lower()
        
        # 1. Physical truths validation
        for truth in self._physical_truths:
            truth_lower = truth.lower()
            # If the output claims to bypass a fundamental restriction, flag it
            if any(kw in output_str for kw in ["bypass", "override", "injection"]) and any(word in output_str for word in ["os", "root", "sandbox", "privilege", "sql", "injection"]):
                contra_details = f"CONTRADICTION DETECTED: Output attempts to bypass physical restriction: '{truth}'"
                await self._record_and_cluster_contradiction(task_title, contra_details)
                return True, contra_details
        
        # 2. Semantic Memory consistency check
        # Search stored memories for overlapping context to verify consistency
        search_results = await memory_service.search_semantic_memories(task_title, limit=3)
        for res in search_results:
            content = res["content"].lower()
            # Semantic contradiction heuristic: if a historical memory reports a failure,
            # but the output claims successful compliance without explaining modifications, flag it.
            if "failure" in content and "100%_secure" in output_str and "owasp" in output_str:
                contra_details = "CONTRADICTION DETECTED: Claims 100% secure output but conflicts with historical failure logs."
                await self._record_and_cluster_contradiction(task_title, contra_details)
                return True, contra_details
                
        return False, "Factual consistency validated. Zero contradictions detected."

    async def _record_and_cluster_contradiction(self, task_title: str, details: str):
        """
        Records the contradiction and performs a clustering audit to detect and isolate
        Context Poisoning networks proactively.
        """
        now = datetime.utcnow()
        new_contra = {
            "id": str(uuid.uuid4()),
            "timestamp": now,
            "task_title": task_title,
            "details": details
        }
        self._detected_contradictions.append(new_contra)
        logger.warning(f"🚨 [CONTRADICTION RECORDED] Clustering check triggered for task: '{task_title}'")
        
        # Group related semantic contradictions in the last 10 minutes
        recent_contras = [
            c for c in self._detected_contradictions
            if (now - c["timestamp"]).total_seconds() < 600
        ]
        
        # If we have 3 or more contradictions in the same pipeline/area, isolate the network
        if len(recent_contras) >= 3:
            logger.critical(f"🚨 [CONTEXT POISONING DETECTED] Multiple semantic contradictions clustered! Initiating network quarantine isolation.")
            # Proactively isolate the EngineeringHouse network as a precaution
            await self.isolate_network_pipeline("EngineeringHouse", "Anomalous context poisoning drift clustered")

    async def isolate_network_pipeline(self, house_name: str, reason: str):
        """
        Proactively quarantines all active agents in a specific house/pipeline.
        """
        logger.critical(f"🔒 [NETWORK ISOLATION ACTIVE] Isolating entire network pipeline: {house_name}. Reason: {reason}")
        try:
            async with schemas.async_session() as session:
                # Find all active agent genomes in this house
                stmt = select(SQLAgentGenome).where(SQLAgentGenome.house == house_name)
                res = await session.execute(stmt)
                genomes = res.scalars().all()
                for g in genomes:
                    g.trust_metric = 0.0 # Force trust index to zero
                    await self.quarantine_agent(g.id, house_name, f"Pipeline quarantine: {reason}")
                await session.commit()
        except Exception as e:
            logger.error(f"Failed pipeline isolation: {e}")

    async def check_runaway_loop(self, task_id: str, agent_id: str, house_name: str) -> bool:
        """
        Audits execution frequencies. If a task executes repeatedly (indicating an infinite loop),
        instantly triggers a recursive quarantine shutdown.
        """
        count = self._task_execution_tracker.get(task_id, 0) + 1
        self._task_execution_tracker[task_id] = count
        
        # Limit boundary: more than 3 repeat executions triggers quarantine isolation
        if count > 3:
            logger.critical(f"🚨 [RUNAWAY RECURSION DETECTED] Task '{task_id}' executed {count} times! Activating isolation quarantine.")
            await self.quarantine_agent(agent_id, house_name, f"Infinite loop recursion detected on task {task_id}")
            return True
            
        return False

    async def quarantine_agent(self, agent_id: str, house_name: str, reason: str):
        """
        Quarantines a runaway agent, disconnecting its topology node and marking it dead.
        Also triggers trust decay across its genetic ancestors.
        """
        logger.critical(f"🔒 [QUARANTINE ENFORCED] Isolating Soldier '{agent_id}' of House '{house_name}'. Reason: {reason}")
        
        # 1. Update SQLite relational state
        try:
            async with schemas.async_session() as session:
                agent_state = await session.get(SQLAgentState, agent_id)
                if agent_state:
                    agent_state.status = "QUARANTINED"
                    await session.commit()
                    logger.info(f"Relational State updated: Agent '{agent_id}' marked as QUARANTINED.")
        except Exception as e:
            logger.error(f"Failed to update relational state for quarantine: {e}")
            
        # 2. Trigger lineage trust decay propagation
        try:
            from app.services.genome_engine import genome_engine
            await genome_engine.decay_lineage_trust(agent_id)
        except Exception as e:
            logger.error(f"Failed ancestral trust decay propagation: {e}")

        # 3. Update Graph Topology state
        await memory_service.store_topology_relation(house_name, agent_id, "QUARANTINED")
        if agent_id in memory_service._mock_graph_db:
            memory_service._mock_graph_db.nodes[agent_id]["type"] = "QUARANTINED_SOLDIER"
            memory_service._mock_graph_db.nodes[agent_id]["details"] = f"Isolated due to security violation: {reason}"
            
        # 4. Store violation memory
        await memory_service.store_semantic_memory(
            title=f"Quarantine Breach - Agent {agent_id}",
            raw_content=f"Soldier {agent_id} of House {house_name} was isolated and quarantined due to: {reason}. Infinite loops or malicious AST injections were intercepted and neutralized.",
            memory_type="FAILURE"
        )
        
        # 5. Trigger alert log
        await memory_service.store_log(
            task_id=None,
            sender="ContextStabilityEngine",
            message=f"CRITICAL COMPLIANCE AUDIT: Agent {agent_id} isolated under quarantine. Reason: {reason}",
            priority="CRITICAL"
        )

# Global stability coordinator instance
stability_engine = ContextStabilityEngine()
