import asyncio
import logging
import sys
import uuid
from datetime import datetime

# Add project root to path for local execution
sys.path.append(".")

from app.models import schemas
from app.models.schemas import (
    init_db,
    SQLCognitiveMutation,
    SQLDoctrineCompetition,
    SQLCognitiveGenome,
    SQLMetaLearningRun,
    SQLTask
)
from app.services.meta_learning import meta_learning
from app.services.memory_service import memory_service
from app.core.event_bus import event_bus, Event
from app.agents.knight import knight

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase8")

async def test_cognitive_genome_evolution_crossover():
    logger.info("=== 1. Testing Cognitive Genome Evolution & DNA Crossover ===")
    
    # 1. Trigger genome evolution check to seed initial parents in sqlite
    genomes = await meta_learning.evolve_cognitive_genomes()
    assert len(genomes) >= 3, "Evolution should yield parent_a, parent_b, and child hybrid genome."
    
    parent_a, parent_b, child = genomes[0], genomes[1], genomes[2]
    
    # Validate DNA property crossover inheritance bounds
    assert child.reasoning_style in (parent_a.reasoning_style, parent_b.reasoning_style), "Child must inherit reasoning style."
    assert child.debate_format in (parent_a.debate_format, parent_b.debate_format), "Child must inherit debate format."
    assert child.memory_coefficient is not None, "Child memory coefficient must be calculated."
    assert child.generation == max(parent_a.generation, parent_b.generation) + 1, "Child generation must increment."
    
    logger.info(f"🧬 Spawned child hybrid genome: {child.id} (Gen {child.generation}). Reasoning: {child.reasoning_style}")
    logger.info("✓ Cognitive Genome Evolution DNA crossover tests passed successfully.")

async def test_learning_stability_containment_checks():
    logger.info("=== 2. Testing Learning Stability & Containment Audits ===")
    
    # 1. Propose safe mutation parameters (recursion depth = 1, speed_target = 1.0, exploration_rate = 0.5)
    safe_params = {"recursion_depth": 1, "speed_target": 1.0, "exploration_rate": 0.5}
    safe_score = await meta_learning.evaluate_stability_score(safe_params)
    assert safe_score >= 0.80, "Safe mutation parameters should yield stability score >= 0.80"
    
    mutation_safe = await meta_learning.propose_architecture_evolution(
        mutation_type="TOPOLOGY_MUTATION",
        description="Optimize strategic thought routing topology rules.",
        parameters=safe_params
    )
    assert mutation_safe.status == "PROPOSED", "Safe mutation should be set to PROPOSED status."
    
    # Restructure active cognition commits safe proposal
    committed_mutation = await meta_learning.restructure_active_cognition(mutation_safe.id)
    assert committed_mutation.status == "COMMITTED", "Approved mutation should be COMMITTED to active topology."
    
    # 2. Propose unsafe/dangerous mutation parameters (recursion_depth = 5, speed_target = 2.0, exploration_rate = 0.9)
    unsafe_params = {"recursion_depth": 5, "speed_target": 2.0, "exploration_rate": 0.9}
    unsafe_score = await meta_learning.evaluate_stability_score(unsafe_params)
    assert unsafe_score < 0.80, "Dangerous mutation parameters must yield stability score < 0.80"
    
    mutation_unsafe = await meta_learning.propose_architecture_evolution(
        mutation_type="REASONING_MUTATION",
        description="Dangerous deep recursive search strategy adjustment.",
        parameters=unsafe_params
    )
    assert mutation_unsafe.status == "BLOCKED", "Dangerous mutation must be immediately BLOCKED/vetoed by Stability Engine."
    
    logger.info("✓ Learning stability containment safety and vetoes validated.")

async def test_philosophy_doctrine_tournaments():
    logger.info("=== 3. Testing Philosophy Doctrine Tournaments ===")
    
    async with schemas.async_session() as session:
        # Pull two genomes for tournament matching
        from sqlalchemy import select
        res = await session.execute(select(SQLCognitiveGenome).limit(2))
        genomes = res.scalars().all()
        assert len(genomes) >= 2, "Need at least two seeded genomes."
        
    comp_a, comp_b = genomes[0].id, genomes[1].id
    
    # Run simulated tournament match
    competition = await meta_learning.run_doctrine_tournament(comp_a, comp_b)
    
    assert competition.id.startswith("comp_"), "Competition ID must be recorded."
    assert competition.winner_id in (comp_a, comp_b), "Winner must be one of the competitors."
    assert competition.metric_a > 0.0 and competition.metric_b > 0.0, "Stress metrics must be scored."
    
    logger.info(f"⚔️ Winner elected in Doctrine Tournament: {competition.winner_id}")
    logger.info("✓ Doctrine Tournament arena simulation passed successfully.")

async def test_experience_distillation_and_failures():
    logger.info("=== 4. Testing Experience Distillation & Failure Intelligence cascades ===")
    
    obj_id = "test_meta_obj_999"
    
    # 1. Distill Successful Objective Run
    # Add simulated successful task to memory representing task execution lineage
    successful_task = SQLTask(
        id=f"{obj_id}_task_01",
        parent_objective=obj_id,
        title="Formulate strategic meta rules",
        assigned_house="StrategyHouse",
        status="COMPLETED"
    )
    async with schemas.async_session() as session:
        session.add(successful_task)
        await session.commit()
        
    run = await meta_learning.distill_completed_run(obj_id)
    assert run.run_type == "EXPERIENCE_DISTILLATION", "Run type must be experience distillation."
    assert run.accuracy_gain > 0, "Successful distillation must yield positive accuracy gain."
    assert "STRATEGIC BLUEPRINT" in run.abstraction_derived, "Distilled abstraction must contain blueprint principles."
    
    # 2. Derive high-level abstraction laws
    law = await meta_learning.derive_abstract_principles(run.id)
    assert "GLOBAL KINGDOM PRINCIPLE" in law, "Should derive abstract global law from blueprint."
    
    # 3. Analyze cascade failure run
    fail_run = await meta_learning.analyze_failure_cascade(obj_id, "Critical exception: SQLite locked, thread timeout exceeded.")
    assert fail_run.accuracy_gain < 0, "Failure run must yield negative reinforcement penalty."
    assert "PROTECTIVE CAUTION DIRECTIVE" in fail_run.abstraction_derived, "Failure directive must be generated."
    
    # Verify safeguards are recorded semantically
    safeguards = await memory_service.search_semantic_memories(f"safeguard caution directive {obj_id}", limit=1)
    assert len(safeguards) > 0, "Safeguard directives must be saved to memory crypt."
    
    logger.info("✓ Experience distillation, abstraction engines, and failure intelligence network tests passed.")

async def test_e2e_knight_meta_learning_integration():
    logger.info("=== 5. Testing Knight-0 E2E Meta-Learning System Hooks ===")
    
    # 1. Accept Objective loads active genome from DB
    objective_id = f"meta_objective_{uuid.uuid4().hex[:4]}"
    raw_objective = "Issue objective: Optimize collective thought routing topologies."
    
    tasks = await knight.accept_objective(objective_id, raw_objective)
    assert len(tasks) > 0, "Objective should decompose successfully into active task DAG."
    
    # Simulate completion of all tasks in DAG to trigger successful meta-learning update
    for t in tasks:
        event = Event(
            event_type="TASK_COMPLETED",
            sender="StrategyHouse",
            payload={"task": {"id": t.id, "status": "COMPLETED", "output_data": {"accuracy": 1.0}}}
        )
        await knight.handle_task_completed(event)
        
    # Check that meta learning runs are saved
    async with schemas.async_session() as session:
        from sqlalchemy import select
        res = await session.execute(select(SQLMetaLearningRun).where(SQLMetaLearningRun.input_objective_id == objective_id))
        ml_runs = res.scalars().all()
        assert len(ml_runs) > 0, "E2E task completion must trigger Meta-Learning experience distillation."
        
    logger.info("✓ Knight-0 Sovereign Governor Meta-Learning hooks executed cleanly.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 8: AUTONOMOUS META-LEARNING TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize SQLite fallback memory database for isolated execution
        await init_db()
        await event_bus.connect()
        await memory_service.connect()
        
        await test_cognitive_genome_evolution_crossover()
        await test_learning_stability_containment_checks()
        await test_philosophy_doctrine_tournaments()
        await test_experience_distillation_and_failures()
        await test_e2e_knight_meta_learning_integration()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL PHASE 8 METAEVOLUTION TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
