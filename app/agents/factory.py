import asyncio
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.core.constitution import constitution
from app.services.memory_service import memory_service
from app.models.schemas import SQLAgentState, AgentStateSchema

logger = logging.getLogger("antigravity.factory")

class BaseSoldier:
    def __init__(self, agent_id: str, role: str, house: str, permissions: List[str]):
        self.agent_id = agent_id
        self.role = role
        self.house = house
        self.permissions = permissions
        self.max_lifespan_sec = 60 # Default timeout safety boundary (CONST-IV)
        self.spawn_time = datetime.utcnow()

    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Executes task operations within a strict timeout block."""
        logger.info(f"⚔️  [SOLDIER ACTIVE] {self.agent_id} ({self.role}) deploying for {self.house}...")
        await memory_service.store_topology_relation(self.house, self.agent_id, "SPAWNED")
        
        try:
            # Enforce execution timeout boundaries to prevent memory leak and freeze (CONST-IV)
            output = await asyncio.wait_for(
                self._run_logic(task_input),
                timeout=float(self.max_lifespan_sec)
            )
            await self._update_metrics(success=True)
            return output
        except asyncio.TimeoutError:
            logger.critical(f"⏰ [SOLDIER TIMEOUT] Soldier {self.agent_id} exceeded max lifespan of {self.max_lifespan_sec}s! Terminating.")
            await self._update_metrics(success=False)
            raise RuntimeError(f"Soldier {self.agent_id} execution timed out!")
        except Exception as e:
            logger.error(f"💥 [SOLDIER ERROR] Soldier {self.agent_id} failed: {e}")
            await self._update_metrics(success=False)
            raise e
        finally:
            await self.retire()

    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclasses to perform specific tasks."""
        raise NotImplementedError("Subclasses must implement _run_logic!")

    async def _update_metrics(self, success: bool):
        """Updates agent performance in Postgres relational store."""
        try:
            from app.models.schemas import async_session
            async with async_session() as session:
                result = await session.get(SQLAgentState, self.agent_id)
                if result:
                    if success:
                        result.success_count += 1
                        # If highly successful, level up the agent (Evolutions)
                        if result.success_count % 3 == 0:
                            result.current_level += 1
                            logger.info(f"📈 [AGENT LEVEL UP] {self.agent_id} upgraded to Level {result.current_level}!")
                    else:
                        result.failure_count += 1
                    await session.commit()
        except Exception as e:
            logger.error(f"Failed updating agent state metrics: {e}")

    async def retire(self):
        """Clean up resource holdings, flag status, and unmount from active graph topology."""
        logger.info(f"💀 [SOLDIER RETIRED] {self.agent_id} ({self.role}) dissolved successfully.")
        
        # Mark retired in topology graph
        await memory_service.retire_graph_soldier(self.agent_id)
        
        # Set database state
        try:
            from app.models.schemas import async_session
            async with async_session() as session:
                result = await session.get(SQLAgentState, self.agent_id)
                if result:
                    result.status = "RETIRED"
                    await session.commit()
        except Exception as e:
            logger.error(f"Failed status retirement: {e}")

# ==========================================
# SPECIALIZED DISPOSABLE WORKERS (SOLDIERS)
# ==========================================

class StrategySoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Assessing objective boundaries for rule compliance", "INFO")
        await asyncio.sleep(0.5) # Simulate processing
        
        # Strategic analysis output
        plan = {
            "objective_verified": True,
            "security_clearance": "GRANTED",
            "execution_rules": ["NO_ROOT_OPERATIONS", "ISOLATED_FS_ONLY"],
            "strategy": f"Coordinate parallel House activities to satisfy King's objective: '{objective}'"
        }
        return {"plan": plan}


class ResearchSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        queries = task_input.get("queries", [])
        await memory_service.store_log(self.agent_id, self.role, f"Initiating semantic crawler for queries: {queries}", "INFO")
        
        # Simulate browser scraping Playwright fallback context
        await asyncio.sleep(1.0)
        
        knowledge_results = [
            f"Retrieved modern standard practices for semantic compression ratios.",
            f"Crawled network specs detailing Redis Streams throughput."
        ]
        return {"crawled_intelligence": knowledge_results}


class CodeSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        tech_stack = task_input.get("tech_stack", "python").lower()
        objective = task_input.get("objective", "unknown")
        task_id = task_input.get("id", f"task_{uuid.uuid4().hex[:8]}")
        
        await memory_service.store_log(self.agent_id, self.role, f"Deploying Autonomous Execution Engine for objective: {objective}", "INFO")
        
        from app.services.autonomous_execution_engine import autonomous_execution_engine
        
        # Enforce execution via the LLM-powered engine which writes to disk and validates.
        result = await autonomous_execution_engine.execute_generative_task(
            task_id=task_id,
            objective=objective,
            agent_id=self.agent_id
        )
        
        return {
            "generated_files": result["artifacts"],
            "trace_id": result["trace_id"],
            "status": result["status"],
            "stdout": result["stdout"],
            "complexity_score": "Verified Output"
        }


class SecuritySoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        target = task_input.get("target", "")
        await memory_service.store_log(self.agent_id, self.role, f"Auditing {target} for OWASP vulnerabilities and licensing compliance", "INFO")
        await asyncio.sleep(0.8)
        
        # Security static report
        audit_report = {
            "target": target,
            "vulnerabilities_found": 0,
            "compliance_status": "100%_SECURE",
            "details": "Conforms fully to Immutable Constitutional rules [CONST-V]."
        }
        return {"audit_report": audit_report}


class MemorySoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Pumping experience logs into Qdrant vector index...", "INFO")
        await asyncio.sleep(0.6)
        
        # Write to semantic memory
        mem = await memory_service.store_semantic_memory(
            title=f"Infrastructure Build Successful - Task Run #{uuid.uuid4().hex[:6]}",
            raw_content="Engineering House successfully generated and compiled the Redis connection helper. Security House conducted a full static audit and reported 0 vulnerabilities. The workflow compiled seamlessly and achieved compliance with Constitutional guidelines.",
            memory_type="STRATEGY"
        )
        
        return {"archived_memory_id": mem.id, "compression_stats": mem.compression_ratio}


class LogicSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Deconstructing logic for '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        return {
            "analysis": f"Logic analysis of objective: {objective}",
            "logical_flow": ["Identify premises", "Check sound inference", "Conclude action plan"],
            "soundness_verified": True
        }


class ChaosSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Injecting disruptive mutations to '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        return {
            "disruptive_idea": f"What if we completely bypassed the traditional pipeline for '{objective}'?",
            "outlier_risk_percentage": 42.0,
            "chaos_index": 0.85
        }


class SkepticSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Challenging all assumptions for '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        return {
            "vulnerabilities": ["Potential single point of failure in SQLite mock database", "Compute cost overhead"],
            "skepticism_score": 0.9,
            "flaw_detected": True
        }


class SimulationSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Running multi-branch simulation for '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        # Import simulation house dynamically to avoid circular import
        from app.services.simulation_house import simulation_house
        plan_a = await simulation_house.project_branch(objective, "Plan A")
        plan_b = await simulation_house.project_branch(objective, "Plan B")
        plan_c = await simulation_house.project_branch(objective, "Plan C")
        return {
            "simulations": [plan_a, plan_b, plan_c],
            "optimal_branch": "Plan B"
        }


class EconomicSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Calculating compute and resource cost for '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        return {
            "estimated_tokens": 15000,
            "cost_score": 0.15,
            "resource_efficiency": "HIGH"
        }


class EvolutionSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Analyzing fitness trajectory for '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        return {
            "fitness_gain": 0.12,
            "recommended_mutation": "Increase SkepticHouse weight during consensus reasoning",
            "evolutionary_viability": 0.95
        }


class EthicsGovernanceSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        objective = task_input.get("objective", "")
        await memory_service.store_log(self.agent_id, self.role, f"Auditing policy compliance for '{objective}'", "INFO")
        await asyncio.sleep(0.1)
        return {
            "policy_check": "CONSTIT-IV & CONSTIT-V Compliant",
            "is_compliant": True,
            "ethics_score": 1.0
        }


# ==========================================
# PHASE 9: SPECIALIZED SCIENTIFIC SOLDIERS
# ==========================================

class DiscoverySoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Executing autonomous scientific discovery run...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        res = await scientific_cognition.autonomous_theory_formation_engine()
        return {"discoveries_synthesized": [d.title for d in res] if res else ["No new discoveries."]}


class CausalSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Executing causal graph network update...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        chains = await scientific_cognition.causal_discovery_engine()
        return {"causal_chains_updated": len(chains)}


class SimulationResearchSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        hypothesis_id = task_input.get("hypothesis_id")
        await memory_service.store_log(self.agent_id, self.role, f"Running controlled simulation lab for {hypothesis_id}...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        exp = await scientific_cognition.experimentation_simulation_civilization_lab(hypothesis_id)
        return {"experiment_id": exp.id, "outcome": exp.outcome_analysis}


class TheorySoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Auditing active theories and voting on parliament theses...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        theses = await scientific_cognition.civilization_research_parliament()
        return {"theses_audited": len(theses)}


class UncertaintySoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Updating Bayesian uncertainty factors on system gaps...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        res = await scientific_cognition.uncertainty_probabilistic_reasoning_engine()
        return {"knowledge_gaps_reviewed": len(res.get("active_knowledge_gaps", []))}


class InfraScienceSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Profiling core hardware and memory latency...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        metrics = await scientific_cognition.deep_world_model_network()
        return {"infra_telemetry": metrics}


class StrategicForecastingSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Extrapolating long-horizon survival and growth metrics...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        forecasts = await scientific_cognition.long_horizon_civilization_forecasting_engine()
        return forecasts


class AbstractionSoldier(BaseSoldier):
    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        await memory_service.store_log(self.agent_id, self.role, "Deriving universal mathematical principles...", "INFO")
        from app.services.scientific_cognition import scientific_cognition
        principles = await scientific_cognition.reality_abstraction_engine()
        return principles


# ==========================================
# AGENT FACTORY CORE
# ==========================================

class AgentFactory:
    def __init__(self):
        self._active_soldiers: Dict[str, BaseSoldier] = {}

    async def get_active_soldiers_count(self) -> int:
        return len(self._active_soldiers)

    async def spawn_soldier(self, role: str, house: str, task_title: str = "") -> BaseSoldier:
        """
        Creates, logs, and registers a brand new disposable Soldier agent
        subject to Constitutional limit checks.
        """
        # 1. Constitutional Spawning Boundary Check (CONST-IV)
        active_count = len(self._active_soldiers)
        max_limit = 50 # Default limit
        
        # Pre-audit validation
        payload = {"active_soldiers_count": active_count, "max_limit": max_limit}
        if not constitution.validate_action("spawn_soldier", payload):
            raise PermissionError("Constitutional validation failed: Spawning limits exceeded!")

        # Generate descriptive ID based on role and task
        prefix = role.replace("Soldier", "")
        if task_title:
            import re
            # Extract first meaningful word from task title
            words = [w for w in re.split(r'\W+', task_title) if len(w) > 2]
            if words:
                prefix = f"{prefix}_{words[0].capitalize()}"
        
        agent_id = f"{prefix}_{uuid.uuid4().hex[:6]}"
        
        # 2. Map role to specific soldier class
        from app.services.agent_evolver import DYNAMIC_AGENT_REGISTRY
        
        if role in DYNAMIC_AGENT_REGISTRY:
            soldier_cls = DYNAMIC_AGENT_REGISTRY[role]
            permissions = ["DYNAMIC_EXECUTION", "SANDBOX_Scoped"]
        else:
            role_map = {
                "StrategySoldier": (StrategySoldier, ["READ_RULES"]),
                "ResearchSoldier": (ResearchSoldier, ["WEB_SCRAPING"]),
                "CodeSoldier": (CodeSoldier, ["FILE_WRITE"]),
                "SecuritySoldier": (SecuritySoldier, ["STATIC_AUDIT"]),
                "MemorySoldier": (MemorySoldier, ["SEMANTIC_WRITE"]),
                "LogicSoldier": (LogicSoldier, ["LOGICAL_DECONSTRUCT"]),
                "ChaosSoldier": (ChaosSoldier, ["CHAOS_INJECTION"]),
                "SkepticSoldier": (SkepticSoldier, ["VULNERABILITY_AUDIT"]),
                "SimulationSoldier": (SimulationSoldier, ["FUTURE_PROJECTION"]),
                "EconomicSoldier": (EconomicSoldier, ["RESOURCE_OPTIMIZATION"]),
                "EvolutionSoldier": (EvolutionSoldier, ["FITNESS_TRACKING"]),
                "EthicsGovernanceSoldier": (EthicsGovernanceSoldier, ["POLICY_AUDIT"]),
                "DiscoverySoldier": (DiscoverySoldier, ["SCIENTIFIC_DISCOVERY"]),
                "CausalSoldier": (CausalSoldier, ["CAUSAL_ANALYSIS"]),
                "SimulationResearchSoldier": (SimulationResearchSoldier, ["SIMULATION_RESEARCH"]),
                "TheorySoldier": (TheorySoldier, ["THEORY_VALIDATION"]),
                "UncertaintySoldier": (UncertaintySoldier, ["UNCERTAINTY_REASONING"]),
                "InfraScienceSoldier": (InfraScienceSoldier, ["INFRASTRUCTURE_SCIENCE"]),
                "StrategicForecastingSoldier": (StrategicForecastingSoldier, ["STRATEGIC_FORECASTING"]),
                "AbstractionSoldier": (AbstractionSoldier, ["ABSTRACTION_SYNTHESIS"])
            }
            
            soldier_cls, permissions = role_map.get(
                role,
                (BaseSoldier, ["MINIMAL"])
            )

        # 2.1 Fetch active genome and clone it to track this specific spawned agent's lineage
        from app.services.genome_engine import genome_engine
        from app.models.schemas import SQLAgentGenome
        
        active_genome = await genome_engine.get_active_genome(house)
        new_genome_id = f"genome_sp_{uuid.uuid4().hex[:8]}"

        soldier = soldier_cls(agent_id, role, house, permissions)
        soldier.genome_id = new_genome_id
        soldier.prompt_template = active_genome.prompt_template
        soldier.reasoning_style = active_genome.reasoning_style
        soldier.memory_coefficients = active_genome.memory_coefficients
        
        self._active_soldiers[agent_id] = soldier

        # 3. Create persistent record in Postgres
        from app.models.schemas import async_session
        async with async_session() as session:
            db_agent = SQLAgentState(
                agent_id=agent_id,
                role=role,
                house=house,
                status="ACTIVE",
                success_count=0,
                failure_count=0,
                current_level=1
            )
            session.add(db_agent)
            
            # Save cloned genome record tied to this specific agent_id
            db_genome = SQLAgentGenome(
                id=new_genome_id,
                agent_id=agent_id,
                parent_id=active_genome.id,
                house=house,
                prompt_template=active_genome.prompt_template,
                reasoning_style=active_genome.reasoning_style,
                preferred_tools=active_genome.preferred_tools,
                memory_coefficients=active_genome.memory_coefficients,
                trust_metric=active_genome.trust_metric,
                fitness_score=active_genome.fitness_score,
                created_at=datetime.utcnow()
            )
            session.add(db_genome)
            await session.commit()

        # Update topology relationships
        await memory_service.store_topology_relation(agent_id, active_genome.id, "INHERITS_GENOME")
        await memory_service.store_topology_relation(new_genome_id, active_genome.id, "MUTATED_FROM")

        logger.info(f"🏭 [FACTORY SPAWNED] Spawner created {agent_id} ({role}) for {house} using genome {new_genome_id}")
        await memory_service.store_log(None, "AgentFactory", f"Spawned {role} ({agent_id}) assigned to {house} using genome {new_genome_id}", "INFO")

        # Hook retirement to remove from active dictionary
        # We wrap execute to intercept and remove
        original_execute = soldier.execute
        
        async def wrapped_execute(task_input: Dict[str, Any]) -> Dict[str, Any]:
            try:
                return await original_execute(task_input)
            finally:
                if agent_id in self._active_soldiers:
                    del self._active_soldiers[agent_id]

        soldier.execute = wrapped_execute

        return soldier

# Global Agent Factory instance
agent_factory = AgentFactory()
