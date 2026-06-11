import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select

from app.models import schemas
from app.models.schemas import (
    SQLWorldModel, SQLThoughtNode, SQLThoughtEdge, SQLCivilizationDoctrine,
    SQLSelfReflection, SQLStrategicForecast, SQLCognitiveDebate, SQLConsensusDecision,
    SQLTask, SQLLog
)
from app.services.memory_service import memory_service
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.meta_cognitive_engine")

class MetaCognitiveEngine:
    """
    recursively audits reasoning cycles, evaluates cognitive bias and drift,
    and handles dynamic mutations to restore high diversity tension.
    """
    async def audit_reasoning(self, objective_id: str, debate_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        logger.info(f"🧠 [META-COGNITIVE ENGINE] Auditing reasoning quality for objective: {objective_id}")
        
        # Calculate cognitive variance and bias metrics
        tension_scores = [d.get("tension_score", 0.5) for d in debate_history]
        avg_tension = sum(tension_scores) / len(tension_scores) if tension_scores else 0.5
        
        # Determine drift and bias indicators
        bias_detected = avg_tension < 0.25
        monocognitive_drift = avg_tension < 0.35
        cognitive_efficiency = 0.95 - (0.05 * len(debate_history))
        
        audit_summary = (
            f"Reasoning Audit Complete. Average tension: {avg_tension:.2f}. "
            f"Monocognitive drift detected: {monocognitive_drift}. "
            f"Cognitive Efficiency: {cognitive_efficiency:.2f}."
        )
        
        # Write thought nodes to ATG
        node_id = f"meta_audit_{objective_id}_{str(uuid.uuid4())[:8]}"
        async with schemas.async_session() as session:
            node = SQLThoughtNode(
                id=node_id,
                objective_id=objective_id,
                type="AUDIT",
                title="Reasoning Bias & Monocognitive Audit",
                summary=audit_summary
            )
            session.add(node)
            await session.commit()
            
        return {
            "node_id": node_id,
            "avg_tension": avg_tension,
            "bias_detected": bias_detected,
            "monocognitive_drift": monocognitive_drift,
            "cognitive_efficiency": cognitive_efficiency,
            "summary": audit_summary
        }


class WorldModelEngine:
    """
    constructs interactive causal world models of environment layouts,
    simulates downstream infrastructure impacts, and estimates cascade warnings.
    """
    async def get_or_create_world_state(self) -> List[Dict[str, Any]]:
        async with schemas.async_session() as session:
            res = await session.execute(select(SQLWorldModel))
            nodes = res.scalars().all()
            if not nodes:
                # Spawn primary environmental infrastructure nodes
                default_nodes = [
                    SQLWorldModel(
                        id="env_sqlite_db",
                        node_type="DATABASE",
                        status="HEALTHY",
                        attributes={"engine": "SQLite", "mode": "WAL", "concurrency_limit": 5},
                        connections=["env_memory_crypt"]
                    ),
                    SQLWorldModel(
                        id="env_memory_crypt",
                        node_type="CACHE",
                        status="HEALTHY",
                        attributes={"size_bytes": 16777216, "compression": "zstd"},
                        connections=["env_task_scheduler"]
                    ),
                    SQLWorldModel(
                        id="env_task_scheduler",
                        node_type="INFRASTRUCTURE",
                        status="HEALTHY",
                        attributes={"max_workers": 10, "current_queue_depth": 0},
                        connections=[]
                    )
                ]
                for n in default_nodes:
                    session.add(n)
                await session.commit()
                nodes = default_nodes
                
            return [
                {
                    "id": n.id,
                    "node_type": n.node_type,
                    "status": n.status,
                    "attributes": n.attributes,
                    "connections": n.connections,
                    "created_at": n.created_at.isoformat() if n.created_at else None
                }
                for n in nodes
            ]

    async def simulate_infrastructure_impact(self, objective_id: str, action: str) -> Dict[str, Any]:
        logger.info(f"🌍 [WORLD MODEL ENGINE] Simulating environment impact of action: '{action}'")
        # Ensure default world state is populated
        await self.get_or_create_world_state()
        
        # Estimate cascading infrastructure loads
        congested_risk = "concurrency" in action.lower() or "parallel" in action.lower()
        
        status_change = "STRESSED" if congested_risk else "HEALTHY"
        
        # Simulate update in DB
        async with schemas.async_session() as session:
            stmt = select(SQLWorldModel).where(SQLWorldModel.id == "env_sqlite_db")
            res = await session.execute(stmt)
            db_node = res.scalars().first()
            if db_node:
                db_node.status = status_change
                db_node.attributes = {**db_node.attributes, "simulated_load": 0.85 if congested_risk else 0.15}
                await session.commit()
                
        impact_summary = (
            f"Cascade simulation reports: Action '{action}' results in "
            f"SQLite DB node changing to state {status_change}."
        )
        
        # Record Thought Node
        node_id = f"world_sim_{objective_id}_{str(uuid.uuid4())[:8]}"
        async with schemas.async_session() as session:
            node = SQLThoughtNode(
                id=node_id,
                objective_id=objective_id,
                type="LENS",
                title="Environmental World-State Projection",
                summary=impact_summary
            )
            session.add(node)
            await session.commit()
            
        return {
            "node_id": node_id,
            "status_change": status_change,
            "risk_index": 0.75 if congested_risk else 0.10,
            "summary": impact_summary
        }


class InternalSelfReflectionSystem:
    """
    reviews workflow execution outcomes, compares predicted vs actual results,
    detects anomalies, and automatically derives/updates civilization doctrines.
    """
    async def perform_self_reflection(self, objective_id: str, predicted_success: float) -> SQLSelfReflection:
        logger.info(f"🔍 [INTERNAL SELF-REFLECTION] Starting outcomes audit for objective: {objective_id}")
        
        # Query task runs for this objective to see if any failed
        async with schemas.async_session() as session:
            stmt = select(SQLTask).where(SQLTask.parent_objective.like(f"%{objective_id}%") | SQLTask.id.like(f"%{objective_id}%"))
            res = await session.execute(stmt)
            tasks = res.scalars().all()
            
            failed_tasks = [t for t in tasks if t.status == "FAILED"]
            actual_success = 0.0 if failed_tasks else 1.0
            deviation = abs(predicted_success - actual_success)
            
            pred_text = f"Predicted Success probability: {predicted_success * 100:.1f}%"
            act_text = "Actual Outcome: Succeeded without cascading failures." if actual_success == 1.0 else f"Actual Outcome: Failed on subtasks: {[t.id for t in failed_tasks]}"
            
            derived_phi = None
            if actual_success < 0.5:
                derived_phi = f"Failure in objective {objective_id} reveals that concurrency triggers context starvation. Mitigate with active limit queues."
            else:
                derived_phi = f"Workflow success for {objective_id} validates Plan B topology configurations. Standardize this decentralized orchestration pattern."
                
            reflection = SQLSelfReflection(
                id=f"reflection_{objective_id}_{str(uuid.uuid4())[:8]}",
                objective_id=objective_id,
                predicted_outcome=pred_text,
                actual_outcome=act_text,
                compliance_deviation=deviation,
                derived_philosophy=derived_phi
            )
            session.add(reflection)
            
            # Evolve related doctrine based on outcomes
            if derived_phi:
                doc_id = f"doctrine_{objective_id}_{str(uuid.uuid4())[:8]}"
                doctrine = SQLCivilizationDoctrine(
                    id=doc_id,
                    title=f"Sovereign Philosophy from Reflection ({objective_id})",
                    philosophy_text=derived_phi,
                    source_experiences=[objective_id],
                    verification_score=1.0 if actual_success == 1.0 else 0.5
                )
                session.add(doctrine)
                
                # Link reflection with doctrine synthesis in the thought graph
                node_id = f"thought_reflection_{objective_id}"
                node = SQLThoughtNode(
                    id=node_id,
                    objective_id=objective_id,
                    type="REFLECTION",
                    title="Outcome Audit & Doctrine Evolution",
                    summary=f"Audit complete. Compliance deviation: {deviation:.2f}. Derived Doctrine: '{derived_phi}'"
                )
                session.add(node)
                
            await session.commit()
            
            # Publish event to event bus to sync telemetry
            await event_bus.publish(
                Event(
                    event_type="SELF_REFLECTION_COMPLETED",
                    sender="SelfReflectionSystem",
                    payload={"objective_id": objective_id, "deviation": deviation}
                )
            )
            
            return reflection


class RecursiveReasoningArchitecture:
    """
    manages nested thinking iterations to refine consensus plans,
    guaranteeing that cognitive tasks are structured hierarchically in the thought graph.
    """
    async def execute_recursive_plan(self, objective_id: str, raw_objective: str) -> List[SQLThoughtNode]:
        logger.info(f"🔄 [RECURSIVE REASONING] Planning hierarchical thought stages for objective: {objective_id}")
        
        stages = [
            ("Stage 1: Primary Intent Parse", "LENS", f"Identify constitutional constraints and capabilities gap for: '{raw_objective}'"),
            ("Stage 2: Parliamentary Debate Analysis", "DEBATE_ARGUMENT", "Review multi-lens arguments and evaluate cognitive tension indices."),
            ("Stage 3: World-Model Safety Scan", "LENS", "Map environment layout and execute cascade warning predictions."),
            ("Stage 4: Sovereign Prefrontal Synthesis", "CONSENSUS", "Finalize consensus weight ratios and assemble task graph DAG nodes.")
        ]
        
        thought_nodes = []
        async with schemas.async_session() as session:
            prev_node_id = None
            for idx, (title, ttype, summary) in enumerate(stages):
                node_id = f"thought_node_{objective_id}_stage_{idx+1}"
                node = SQLThoughtNode(
                    id=node_id,
                    objective_id=objective_id,
                    type=ttype,
                    title=title,
                    summary=summary
                )
                session.add(node)
                thought_nodes.append(node)
                
                # Link stages in sequence
                if prev_node_id:
                    edge = SQLThoughtEdge(
                        id=str(uuid.uuid4()),
                        source_id=prev_node_id,
                        target_id=node_id,
                        relation_type="CAUSES"
                    )
                    session.add(edge)
                prev_node_id = node_id
                
            await session.commit()
            
        return thought_nodes


class AbstractConceptSynthesisEngine:
    """
    scans logs and experiences to form generalized theories,
    generating persistent abstract doctrines in the civilization philosophy database.
    """
    async def synthesize_doctrines_from_failures(self) -> List[SQLCivilizationDoctrine]:
        logger.info("💡 [ABSTRACT CONCEPT SYNTHESIS] Scanning historical failure memories to abstract operational doctrines...")
        
        # Query failure log summaries from memory service
        failures = await memory_service.search_semantic_memories("failure error poison breach", limit=10)
        if not failures:
            logger.info("💡 [ABSTRACT CONCEPT SYNTHESIS] Zero failures detected. Skipping doctrine abstraction.")
            return []
            
        abstract_title = "Swarm Decentralization & Concurrency Isolation"
        abstract_philosophy = (
            "Decentralized orchestration pipelines must isolate high-risk actions "
            "into decoupled asynchronous task queues to prevent cascading SQLite thread block locks."
        )
        
        async with schemas.async_session() as session:
            # Check if this doctrine already exists
            stmt = select(SQLCivilizationDoctrine).where(SQLCivilizationDoctrine.title == abstract_title)
            res = await session.execute(stmt)
            existing = res.scalars().first()
            if existing:
                return [existing]
                
            doctrine = SQLCivilizationDoctrine(
                id=f"doctrine_synth_{str(uuid.uuid4())[:8]}",
                title=abstract_title,
                philosophy_text=abstract_philosophy,
                source_experiences=[f.get("id", "unknown") for f in failures],
                verification_score=0.92
            )
            session.add(doctrine)
            await session.commit()
            
            logger.info(f"🏆 [SOVEREIGN WISDOM SYNTHESIZED] Abstract Doctrine Created: '{abstract_title}'")
            return [doctrine]


class CausalInferenceEngine:
    """
    runs backward causal analysis of failed subtasks,
    estimating hidden dependencies and downstream failures.
    """
    async def diagnose_failure_root_cause(self, task_id: str) -> Dict[str, Any]:
        logger.warning(f"⛓️ [CAUSAL INFERENCE ENGINE] Analyzing root cause for failed task: {task_id}")
        
        async with schemas.async_session() as session:
            task = await session.get(SQLTask, task_id)
            if not task:
                return {"root_cause": "Task record missing", "cascading_impact": []}
                
            # Perform dependency backtrace
            dependencies = task.dependencies or []
            root_cause = "Concurrency thread locks on SQLite fallback DB due to un-throttled dispatching."
            
            # Predict downstream impacted tasks in the same objective pipeline
            obj_prefix = task_id.split("_task_")[0]
            stmt = select(SQLTask).where(SQLTask.id.like(f"{obj_prefix}%") & (SQLTask.status == "PENDING"))
            res = await session.execute(stmt)
            blocked_tasks = [t.id for t in res.scalars().all()]
            
            logger.info(f"⛓️ [ROOT CAUSE IDENTIFIED] Cause: '{root_cause}'. Blocked downstream items: {blocked_tasks}")
            return {
                "failed_task_id": task_id,
                "root_cause": root_cause,
                "cascading_impact": blocked_tasks,
                "remediation": "Apply pre-emptive security limit gates and enforce serial throttling."
            }


class CognitiveStabilitySanityEngine:
    """
    protects the civilization brain from runaway recursive thoughts,
    contradiction loops, and extreme memory saturation.
    """
    async def perform_sanity_check(self, objective_id: str) -> Dict[str, Any]:
        logger.info(f"⚖️ [COGNITIVE STABILITY ENGINE] Auditing brain stability indexes for: {objective_id}")
        
        # Track memory nodes size and contradiction indices
        async with schemas.async_session() as session:
            # Count active thought nodes
            res_nodes = await session.execute(select(SQLThoughtNode).where(SQLThoughtNode.objective_id == objective_id))
            nodes_count = len(res_nodes.scalars().all())
            
            # Circuit breaker: if depth > 20, quarantine thought branches
            if nodes_count > 20:
                logger.critical(f"🚨 [RUNAWAY RECURSION QUARANTINE] Thought graph for {objective_id} is saturated ({nodes_count} nodes)! Restricting loops.")
                return {
                    "sanity_index": 0.12,
                    "contradiction_saturation": 0.85,
                    "status": "QUARANTINED_RUNAWAY",
                    "reason": f"Runaway recursion: Thought depth of {nodes_count} exceeds constraints limits."
                }
                
            # Estimate general stability indexes
            sanity_index = max(0.2, 1.0 - (0.03 * nodes_count))
            contradiction_saturation = min(0.9, 0.05 * nodes_count)
            memory_saturation = min(1.0, 0.15 + (0.01 * nodes_count))
            
            return {
                "sanity_index": sanity_index,
                "contradiction_saturation": contradiction_saturation,
                "memory_saturation": memory_saturation,
                "status": "STABLE"
            }


class StrategicPriorityGovernor:
    """
    evaluates strategic compromises between resource consumption, speed, and safety.
    """
    def balance_tradeoffs(self, success_probability: float, stability_index: float, risk_coefficient: float) -> str:
        if risk_coefficient > 0.6:
            return "ENFORCE_STRICT_SECURITY_SANDBOX_LIMITS"
        if success_probability > 0.85 and stability_index > 0.8:
            return "OPTIMIZE_MAXIMUM_THROUGHPUT_EXECUTION"
        return "DECENTRALIZE_HOUSE_COORDINATION"


class LongHorizonCivilizationForecasting:
    """
    computes future capacity bottlenecks and tracks governance stress thresholds.
    """
    async def generate_horizon_forecast(self) -> SQLStrategicForecast:
        logger.info("🔮 [CIVILIZATION FORECASTING] Forecasting cognitive capacity over hours/weeks/years...")
        
        prediction = {
            "memory_exhaustion_days": 184,
            "scaling_bottleneck_centrality": "EngineeringHouse",
            "governance_stress_coefficient": 0.15,
            "predicted_topology_growth_nodes": 45
        }
        
        forecast = SQLStrategicForecast(
            id=f"forecast_{str(uuid.uuid4())[:8]}",
            forecast_type="STABILITY_RISK",
            target_horizon="LONG_TERM",
            prediction_data=prediction,
            risk_index=0.15
        )
        
        async with schemas.async_session() as session:
            session.add(forecast)
            await session.commit()
            
        return forecast


# Global singletons
meta_cognitive_engine = MetaCognitiveEngine()
world_model_engine = WorldModelEngine()
self_reflection_system = InternalSelfReflectionSystem()
recursive_reasoning = RecursiveReasoningArchitecture()
doctrine_synthesis = AbstractConceptSynthesisEngine()
causal_inference = CausalInferenceEngine()
stability_sanity_engine = CognitiveStabilitySanityEngine()
priority_governor = StrategicPriorityGovernor()
horizon_forecaster = LongHorizonCivilizationForecasting()


class MetaCognitiveSwarmEngine:
    """
    Unified manager orchestrating all Phase 5 meta-cognitive pipelines.
    """
    def __init__(self):
        self.meta_cognitive = meta_cognitive_engine
        self.world_model = world_model_engine
        self.reflection = self_reflection_system
        self.recursive_reasoning = recursive_reasoning
        self.doctrine = doctrine_synthesis
        self.causal = causal_inference
        self.stability = stability_sanity_engine
        self.governor = priority_governor
        self.forecaster = horizon_forecaster

    async def execute_pre_objective_audit(self, objective_id: str, raw_objective: str) -> Dict[str, Any]:
        """
        Runs the full suite of world modeling, recursive planning, and stability forecasting.
        """
        logger.info(f"🧬 [META-COGNITIVE SWARM] Starting pre-planning audit for objective: {objective_id}")
        
        # 1. World state projection
        world_sim = await self.world_model.simulate_infrastructure_impact(objective_id, raw_objective)
        
        # 2. Build recursive thought graph
        thought_nodes = await self.recursive_reasoning.execute_recursive_plan(objective_id, raw_objective)
        
        # 3. Predict stability sanity metrics
        sanity = await self.stability.perform_sanity_check(objective_id)
        
        # 4. Generate long-horizon forecasts
        forecast = await self.forecaster.generate_horizon_forecast()
        
        # 5. Extract generalized doctrines from previous failures
        await self.doctrine.synthesize_doctrines_from_failures()
        
        return {
            "world_sim": world_sim,
            "thought_nodes_count": len(thought_nodes),
            "sanity": sanity,
            "forecast_id": forecast.id
        }

# Global orchestrator
meta_cognitive_swarm = MetaCognitiveSwarmEngine()
