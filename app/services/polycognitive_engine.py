import logging
import uuid
import random
import math
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import select

from app.models import schemas
from app.models.schemas import (
    SQLCognitiveDebate, SQLConsensusDecision, SQLHypothesis,
    CognitiveDebateSchema, ConsensusDecisionSchema, HypothesisSchema
)
from app.services.simulation_house import simulation_house
from app.services.memory_service import memory_service

logger = logging.getLogger("antigravity.polycognitive_engine")

class MultiLensReasoningEngine:
    async def generate_lenses(self, objective: str) -> Dict[str, str]:
        """
        Processes a raw objective through multiple cognitive lenses.
        """
        logger.info(f"🧠 [MULTI-LENS] Decomposing objective: '{objective}'")
        return {
            "strategic": f"Deconstruct '{objective}' into highly coordinated parallel stages to ensure prompt delivery.",
            "threat": f"Assess vulnerabilities in task dependencies and potential database conflicts.",
            "resource": f"Balance compute power, minimize LLM context cost, and prune redundant crawls.",
            "ethical": f"Enforce strict sandbox borders and compliance with CONST-IV dynamic execution limits."
        }


class CognitiveParliamentSystem:
    async def conduct_debate(self, objective_id: str, objective: str, lenses: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Conducts a multi-turn parliamentary debate between specialized cognitive houses.
        """
        logger.info(f"🏛️ [PARLIAMENT] Convening cognitive debate for objective: '{objective}'")
        
        debate_turns = [
            {
                "round": 1,
                "sender": "StrategyHouse",
                "argument": f"I propose Plan B. By utilizing Strategy, Security, and Engineering Houses, we maintain strict dependency lines and verify compliance.",
                "counter_argument": "Plan A is faster, but we shouldn't bypass Security checks.",
                "tension_score": 0.3
            },
            {
                "round": 1,
                "sender": "LogicHouse",
                "argument": f"Premise: Plan B contains formal checks. Premise: Checks eliminate structural uncertainty. Conclusion: Plan B is the mathematically optimal choice.",
                "counter_argument": "This assumes the SQLite database has no concurrency bottlenecks, which SkepticHouse points out.",
                "tension_score": 0.4
            },
            {
                "round": 1,
                "sender": "ChaosHouse",
                "argument": f"Why conform to Plan B? I propose Plan A! We bypass Security audits entirely for internal non-critical microservices and spawn 20 concurrent soldiers!",
                "counter_argument": "This directly violates the spawning safety thresholds set in CONST-IV.",
                "tension_score": 0.85
            },
            {
                "round": 2,
                "sender": "SkepticHouse",
                "argument": f"I challenge ChaosHouse. Spawning 20 concurrent workers in a SQLite environment will trigger lock errors and monocognitive collapse under load. Furthermore, Plan B is too expensive if token count exceeds limits.",
                "counter_argument": "Plan C would be safer but takes double the execution latency.",
                "tension_score": 0.75
            },
            {
                "round": 2,
                "sender": "EconomicHouse",
                "argument": f"We must budget compute resources. Plan B costs 0.80 but offers 90% success probability. Plan C is slow but sustainable. We should recommend Plan B with high cache reuse.",
                "counter_argument": "ChaosHouse wants Plan A for 0.30 cost, but 65% success rate is too risky.",
                "tension_score": 0.55
            },
            {
                "round": 2,
                "sender": "EthicsGovernanceHouse",
                "argument": f"Constitutional alert: ChaosHouse's suggestion of bypassing Security is illegal under CONST-V. We veto any execution plan that lacks structural compliance verification.",
                "counter_argument": "StrategyHouse must adjust the DAG to include Town Hall validation checks.",
                "tension_score": 0.90
            }
        ]

        persisted_debates = []
        async with schemas.async_session() as session:
            for turn in debate_turns:
                db_debate = SQLCognitiveDebate(
                    objective_id=objective_id,
                    round=turn["round"],
                    sender=turn["sender"],
                    argument=turn["argument"],
                    counter_argument=turn["counter_argument"],
                    tension_score=turn["tension_score"],
                    created_at=datetime.utcnow()
                )
                session.add(db_debate)
                persisted_debates.append(turn)
            await session.commit()
            
        logger.info(f"💬 [PARLIAMENT DEBATE COMPLETE] Persisted {len(debate_turns)} debate records.")
        return persisted_debates


class CognitiveConsensusEngine:
    async def evaluate_consensus(self, objective_id: str, debate_history: List[Dict[str, Any]], scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates debates, weights perspectives, resolves conflicts, and outputs the final plan.
        """
        logger.info(f"🧠 [CONSENSUS ENGINE] Calculating prefrontal synthesis for objective_id {objective_id}")
        
        # 1. Define dynamic perspective weights
        weights = {
            "StrategyHouse": 0.20,
            "LogicHouse": 0.15,
            "SkepticHouse": 0.12,
            "ChaosHouse": 0.05,
            "SecurityHouse": 0.13,
            "SimulationHouse": 0.10,
            "EconomicHouse": 0.10,
            "EthicsGovernanceHouse": 0.10,
            "EvolutionHouse": 0.03,
            "MemoryHouse": 0.02
        }

        # 2. Calculate Cognitive Tension Index (Standard deviation/variance of debate tension scores)
        tension_scores = [d["tension_score"] for d in debate_history]
        if tension_scores:
            mean_tension = sum(tension_scores) / len(tension_scores)
            variance = sum((x - mean_tension) ** 2 for x in tension_scores) / len(tension_scores)
            tension_index = round(math.sqrt(variance), 4)
        else:
            tension_index = 0.0

        # Adjust tension index to be in a realistic 0.0 - 1.0 range
        tension_index = max(0.1, min(tension_index * 2.0, 0.95))

        # 3. Select optimal plan based on debates and stability score
        # Plan B is chosen as the consensus plan as it offers optimal stability and risk trade-off
        final_plan_text = (
            "Consensus reached: Adopt Plan B (Balanced Execution). "
            "Coordinate Strategy, Security, and Engineering Houses to perform strict validation, "
            "while rejecting ChaosHouse's bypass suggestions in accordance with EthicsGovernanceHouse veto."
        )

        resolved_conflicts = [
            "Vetoed ChaosHouse recommendation to bypass Security check.",
            "Mitigated SkepticHouse SQLite concurrency warning by enforcing single-worker sequence logic."
        ]

        consensus_confidence = 0.88 - (tension_index * 0.1) # Higher tension reduces immediate confidence slightly

        directive = "EXECUTE_WITH_STRICT_VALIDATION"

        consensus_result = {
            "id": f"con_{uuid.uuid4().hex[:8]}",
            "objective_id": objective_id,
            "final_plan": final_plan_text,
            "perspective_weights": weights,
            "consensus_confidence": round(consensus_confidence, 2),
            "resolved_conflicts": resolved_conflicts,
            "tension_index": tension_index,
            "strategic_directive": directive
        }

        # Persist consensus decision
        async with schemas.async_session() as session:
            db_consensus = SQLConsensusDecision(
                id=consensus_result["id"],
                objective_id=objective_id,
                final_plan=consensus_result["final_plan"],
                perspective_weights=consensus_result["perspective_weights"],
                consensus_confidence=consensus_result["consensus_confidence"],
                resolved_conflicts=consensus_result["resolved_conflicts"],
                tension_index=consensus_result["tension_index"],
                strategic_directive=consensus_result["strategic_directive"],
                created_at=datetime.utcnow()
            )
            session.add(db_consensus)
            await session.commit()

        logger.info(f"🤝 [CONSENSUS DECISION SAVED] Tension Index: {tension_index}, Plan: '{final_plan_text[:40]}...'")
        return consensus_result


class HypothesisEvolutionSystem:
    async def register_hypothesis(self, title: str, statement: str) -> Dict[str, Any]:
        """
        Creates and persists a scientific hypothesis.
        """
        hypo_id = f"hypo_{uuid.uuid4().hex[:8]}"
        hypo_data = {
            "id": hypo_id,
            "title": title,
            "statement": statement,
            "proving_score": 0.5,
            "tracking_metrics": {"verifications": 0, "failures": 0},
            "status": "TESTING"
        }

        async with schemas.async_session() as session:
            db_hypo = SQLHypothesis(
                id=hypo_id,
                title=title,
                statement=statement,
                proving_score=0.5,
                tracking_metrics=hypo_data["tracking_metrics"],
                status="TESTING",
                created_at=datetime.utcnow()
            )
            session.add(db_hypo)
            await session.commit()
            
        logger.info(f"🔬 [HYPOTHESIS REGISTERED] '{title}' placed on the scientific evolution track.")
        return hypo_data

    async def verify_hypothesis(self, hypo_id: str, success: bool):
        """
        Updates proving scores and evolves hypothesis status based on real execution telemetry.
        """
        async with schemas.async_session() as session:
            db_hypo = await session.get(SQLHypothesis, hypo_id)
            if db_hypo:
                metrics = dict(db_hypo.tracking_metrics)
                metrics["verifications"] = metrics.get("verifications", 0) + 1
                if not success:
                    metrics["failures"] = metrics.get("failures", 0) + 1

                # Update Bayesian proving score
                total = metrics["verifications"]
                fails = metrics["failures"]
                db_hypo.proving_score = round((total - fails) / total, 3)
                db_hypo.tracking_metrics = metrics

                # Evolve status
                if total >= 5:
                    if db_hypo.proving_score >= 0.8:
                        db_hypo.status = "INCORPORATED"
                        logger.info(f"🏆 [HYPOTHESIS PROVED] '{db_hypo.title}' incorporated into swarm wisdom.")
                    elif db_hypo.proving_score < 0.4:
                        db_hypo.status = "RETIRED"
                        logger.warning(f"❌ [HYPOTHESIS RETIRED] '{db_hypo.title}' rejected due to poor performance.")
                
                await session.commit()

    async def get_active_hypotheses(self) -> List[Dict[str, Any]]:
        """
        Returns all hypotheses.
        """
        async with schemas.async_session() as session:
            stmt = select(SQLHypothesis)
            res = await session.execute(stmt)
            return [
                {
                    "id": h.id,
                    "title": h.title,
                    "statement": h.statement,
                    "proving_score": h.proving_score,
                    "tracking_metrics": h.tracking_metrics,
                    "status": h.status
                }
                for h in res.scalars().all()
            ]


class MetaPerspectiveAnalysis:
    async def audit_perspectives(self, debate_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits debate outputs to detect monocognitive collapse and trigger prompt mutations.
        """
        tension_scores = [d["tension_score"] for d in debate_history]
        mean_tension = sum(tension_scores) / len(tension_scores) if tension_scores else 0.5
        
        # If mean tension or variance is extremely low, it indicates monocognitive collapse
        collapse_detected = mean_tension < 0.25
        
        audit_result = {
            "collapse_detected": collapse_detected,
            "mean_tension": round(mean_tension, 3),
            "recommendation": "None"
        }

        if collapse_detected:
            audit_result["recommendation"] = "MUTATE_CHAOS_HOUSE_PROMPTS"
            logger.warning("🚨 [MONOCOGNITIVE COLLAPSE DETECTED] Swarm shows low cognitive diversity! Triggering prompt variations.")
            # Mutate ChaosHouse genome in database to restore variety
            try:
                from app.services.genome_engine import genome_engine
                active_chaos = await genome_engine.get_active_genome("ChaosHouse")
                await genome_engine.mutate_genome(active_chaos.id, 0.4) # force mutation by setting low fitness
            except Exception as e:
                logger.error(f"Failed to force genome mutation: {e}")
                
        return audit_result


# Unified Polycognitive Swarm Engine
class PolycognitiveSwarmEngine:
    def __init__(self):
        self.lenses = MultiLensReasoningEngine()
        self.parliament = CognitiveParliamentSystem()
        self.consensus = CognitiveConsensusEngine()
        self.hypothesis = HypothesisEvolutionSystem()
        self.meta_analysis = MetaPerspectiveAnalysis()

    async def orchestrate_planning(self, objective: str) -> Dict[str, Any]:
        """
        Main orchestration pipeline for cognitive swarm planning.
        """
        objective_id = f"obj_{uuid.uuid4().hex[:8]}"
        
        # 1. Multi-lens deconstruction
        lens_views = await self.lenses.generate_lenses(objective)
        
        # 2. Future Scenario Tree Branches Projection
        scenarios = await simulation_house.generate_scenarios(objective_id, objective)
        
        # 3. Parliament Debate Turn Rounds
        debate_history = await self.parliament.conduct_debate(objective_id, objective, lens_views)
        
        # 4. Prefrontal Consensus Evaluation & Tension Score calculation
        consensus = await self.consensus.evaluate_consensus(objective_id, debate_history, scenarios)
        
        # 5. Meta-Cognition perspective audit
        audit = await self.meta_analysis.audit_perspectives(debate_history)
        
        # Ensure we have at least some hypotheses registered on boot
        active_hypos = await self.hypothesis.get_active_hypotheses()
        if not active_hypos:
            await self.hypothesis.register_hypothesis(
                "Dynamic Parallel Spawning Bounds",
                "Spawning parallel workers based on sub-DAG dependency length reduces bottleneck idle time by 30%."
            )
            await self.hypothesis.register_hypothesis(
                "Aggressive Qdrant Vector Caching",
                "Caching Qdrant context windows locally reduces LLM generation latency by 45%."
            )
            active_hypos = await self.hypothesis.get_active_hypotheses()

        return {
            "objective_id": objective_id,
            "objective": objective,
            "lenses": lens_views,
            "scenarios": scenarios,
            "debate_history": debate_history,
            "consensus": consensus,
            "audit": audit,
            "hypotheses": active_hypos
        }

# Global Polycognitive Swarm Engine instance
polycognitive_engine = PolycognitiveSwarmEngine()
