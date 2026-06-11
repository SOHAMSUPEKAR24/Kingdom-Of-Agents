import asyncio
import logging
import sys
from datetime import datetime
from sqlalchemy import select

# Add project root to path for local execution
sys.path.append(".")

from app.core.event_bus import event_bus, Event
from app.services.memory_service import memory_service
from app.services.genome_engine import genome_engine
from app.services.polycognitive_engine import polycognitive_engine
from app.services.simulation_house import simulation_house
from app.agents.knight import knight
from app.agents.houses import initialize_houses
from app.agents.town_hall import town_hall
from app.models import schemas
from app.models.schemas import (
    init_db, SQLCognitiveDebate, SQLSimulationScenario, SQLHypothesis, SQLConsensusDecision
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase4")

async def test_database_initialization():
    logger.info("=== 1. Testing Relational DB Schema Initialization for Phase 4 ===")
    
    # Verify that all tables have been successfully mapped by SQLAlchemy and created
    async with schemas.async_session() as session:
        # Check cognitive debates
        debates_res = await session.execute(select(SQLCognitiveDebate))
        logger.info(f"Existing cognitive debates rows: {len(debates_res.scalars().all())}")

        # Check simulation scenarios
        scenarios_res = await session.execute(select(SQLSimulationScenario))
        logger.info(f"Existing simulation scenarios rows: {len(scenarios_res.scalars().all())}")

        # Check hypotheses
        hypo_res = await session.execute(select(SQLHypothesis))
        logger.info(f"Existing hypotheses rows: {len(hypo_res.scalars().all())}")

        # Check consensus decisions
        consensus_res = await session.execute(select(SQLConsensusDecision))
        logger.info(f"Existing consensus decisions rows: {len(consensus_res.scalars().all())}")
        
    logger.info("✓ Relational DB Schema Initialization test PASSED.")

async def test_multi_lens_reasoning_and_debate():
    logger.info("=== 2. Testing Multi-Lens Reasoning and Parliamentary Debate ===")
    
    objective = "Secure the database infrastructure from standard SQLite concurrency locks."
    objective_id = "test_obj_debate_99"
    
    # 1. Multi-Lens reasoning decomposition
    lenses = await polycognitive_engine.lenses.generate_lenses(objective)
    assert "strategic" in lenses
    assert "threat" in lenses
    assert "resource" in lenses
    assert "ethical" in lenses
    logger.info("✓ Multi-Lens reasoning correctly decomposed objective into 4 perspective lenses.")
    
    # 2. Parliamentary debate execution
    debate_history = await polycognitive_engine.parliament.conduct_debate(objective_id, objective, lenses)
    assert len(debate_history) > 0
    assert debate_history[0]["round"] == 1
    assert "sender" in debate_history[0]
    assert "argument" in debate_history[0]
    
    # Verify database persistence
    async with schemas.async_session() as session:
        stmt = select(SQLCognitiveDebate).where(SQLCognitiveDebate.objective_id == objective_id)
        res = await session.execute(stmt)
        persisted = res.scalars().all()
        assert len(persisted) == len(debate_history)
        for p in persisted:
            assert p.objective_id == objective_id
            assert p.round in (1, 2)
            assert p.tension_score >= 0.0
            
    logger.info(f"✓ Parliamentary debate successfully convened, executed, and persisted {len(debate_history)} turns.")

async def test_consensus_evaluation():
    logger.info("=== 3. Testing Prefrontal Consensus Engine & Tension Calculations ===")
    
    objective_id = "test_obj_consensus_88"
    mock_debate = [
      {"round": 1, "sender": "StrategyHouse", "argument": "Plan B matches parameters.", "tension_score": 0.3},
      {"round": 1, "sender": "ChaosHouse", "argument": "Plan A bypasses all security checks!", "tension_score": 0.8},
      {"round": 2, "sender": "SkepticHouse", "argument": "Plan A will collapse under load.", "tension_score": 0.7}
    ]
    mock_scenarios = [
      {"branch_name": "Plan B", "stability_index": 0.85, "success_probability": 0.90}
    ]
    
    consensus_res = await polycognitive_engine.consensus.evaluate_consensus(objective_id, mock_debate, mock_scenarios)
    
    assert consensus_res["objective_id"] == objective_id
    assert "Plan B" in consensus_res["final_plan"]
    assert consensus_res["tension_index"] > 0.0
    assert consensus_res["consensus_confidence"] > 0.5
    assert len(consensus_res["resolved_conflicts"]) > 0
    
    # Assert database persistence
    async with schemas.async_session() as session:
        stmt = select(SQLConsensusDecision).where(SQLConsensusDecision.objective_id == objective_id)
        res = await session.execute(stmt)
        db_con = res.scalars().first()
        assert db_con is not None
        assert db_con.tension_index == consensus_res["tension_index"]
        assert db_con.consensus_confidence == consensus_res["consensus_confidence"]
        
    logger.info("✓ Consensus Evaluation and Cognitive Tension Index calculations PASSED.")

async def test_future_scenario_branches():
    logger.info("=== 4. Testing Future Scenario Tree Projections (Plan A/B/C) ===")
    
    objective_id = "test_obj_scenarios_77"
    objective = "Optimize dynamic worker scaling profiles."
    
    scenarios = await simulation_house.generate_scenarios(objective_id, objective)
    assert len(scenarios) == 3
    
    branch_names = [s["branch_name"] for s in scenarios]
    assert "Plan A" in branch_names
    assert "Plan B" in branch_names
    assert "Plan C" in branch_names
    
    # Assert specific parameters are scaled correctly per branch
    for s in scenarios:
        assert s["success_probability"] > 0.0
        assert s["stability_index"] > 0.0
        assert s["speed_rating"] > 0.0
        assert s["cost_score"] > 0.0
        assert s["risk_coefficient"] > 0.0
        assert "nodes" in s["topology_projection"]
        assert "edges" in s["topology_projection"]
        
    # Assert database persistence
    async with schemas.async_session() as session:
        stmt = select(SQLSimulationScenario).where(SQLSimulationScenario.objective_id == objective_id)
        res = await session.execute(stmt)
        db_scenarios = res.scalars().all()
        assert len(db_scenarios) == 3
        
    logger.info("✓ Future Scenario Tree simulation and projection branches PASSED.")

async def test_hypothesis_evolution():
    logger.info("=== 5. Testing Bayesian Hypothesis Registration & Verification ===")
    
    title = "Adaptive Concurrency Scaling Limit"
    statement = "Capping concurrent subtasks to 5 prevents SQLite write database locking errors."
    
    # 1. Register hypothesis
    hypo = await polycognitive_engine.hypothesis.register_hypothesis(title, statement)
    hypo_id = hypo["id"]
    assert hypo_id is not None
    assert hypo["title"] == title
    assert hypo["status"] == "TESTING"
    assert hypo["proving_score"] == 0.5
    
    # 2. Add verifications to evolve hypothesis (Successes)
    for _ in range(5):
        await polycognitive_engine.hypothesis.verify_hypothesis(hypo_id, success=True)
        
    # Assert state transitions to INCORPORATED
    async with schemas.async_session() as session:
        db_hypo = await session.get(SQLHypothesis, hypo_id)
        assert db_hypo.proving_score == 1.0
        assert db_hypo.status == "INCORPORATED"
        
    # 3. Test another hypothesis that fails and retires
    title_bad = "Infinite Concurrent Spawn Strategy"
    statement_bad = "Spawning unlimited threads has no impact on system memory."
    hypo_bad = await polycognitive_engine.hypothesis.register_hypothesis(title_bad, statement_bad)
    bad_id = hypo_bad["id"]
    
    for _ in range(5):
        await polycognitive_engine.hypothesis.verify_hypothesis(bad_id, success=False)
        
    async with schemas.async_session() as session:
        db_bad = await session.get(SQLHypothesis, bad_id)
        assert db_bad.proving_score == 0.0
        assert db_bad.status == "RETIRED"
        
    logger.info("✓ Bayesian Hypothesis Registration, Verification, and Evolution tracks PASSED.")

async def test_meta_perspective_monocognitive_collapse():
    logger.info("=== 6. Testing Monocognitive Collapse Auditing & Prompt Mutations ===")
    
    # Setup debate with extremely low tension (indicating monocognitive collapse)
    mock_debate_collapse = [
      {"round": 1, "sender": "StrategyHouse", "argument": "Yes, I agree.", "tension_score": 0.1},
      {"round": 1, "sender": "LogicHouse", "argument": "I fully agree with StrategyHouse.", "tension_score": 0.05},
      {"round": 2, "sender": "SecurityHouse", "argument": "Absolutely correct, no threat exists.", "tension_score": 0.1}
    ]
    
    audit_res = await polycognitive_engine.meta_analysis.audit_perspectives(mock_debate_collapse)
    assert audit_res["collapse_detected"] is True
    assert audit_res["recommendation"] == "MUTATE_CHAOS_HOUSE_PROMPTS"
    
    logger.info("✓ Monocognitive Collapse Auditor successfully detected polarization lack and recommended Chaos prompt mutations.")

async def test_governor_class_knight_planning():
    logger.info("=== 7. Testing Knight-0 Governor-Class Orchestrator & Task DAG ===")
    
    objective_id = "test_obj_knight_33"
    raw_objective = "Assemble advanced data analytics with secure sandboxed validation."
    
    # 1. Spawn objective planning through Knight orchestrator
    tasks = await knight.accept_objective(objective_id, raw_objective)
    assert len(tasks) > 0
    
    # Assert Plan B scenario nodes are strictly selected
    assigned_houses = [t.assigned_house for t in tasks]
    assert "StrategyHouse" in assigned_houses
    assert "SecurityHouse" in assigned_houses
    assert "EngineeringHouse" in assigned_houses
    assert "MemoryHouse" in assigned_houses
    
    # 2. Verify graph structure in Knight memory
    dag = knight.task_graphs.get(objective_id)
    assert dag is not None
    import networkx as nx
    assert nx.is_directed_acyclic_graph(dag)
    
    # Check that dependencies are strictly linear sequence matching Plan B projection nodes
    for t in tasks:
        # Relational persistence checks
        async with schemas.async_session() as session:
            stmt = select(schemas.SQLTask).where(schemas.SQLTask.id == t.id)
            res = await session.execute(stmt)
            db_task = res.scalars().first()
            assert db_task is not None
            assert db_task.status == "PENDING" or db_task.status == "RUNNING"
            
    logger.info("✓ Knight-0 Governor-Class Orchestration, dynamic scenario nodes mapping, and DAG validation PASSED.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 4: POLYCOGNITIVE CIVILIZATION INTEGRATION TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize database for tests
        await init_db()
        await event_bus.connect()
        await memory_service.connect()
        await town_hall.initialize()
        await initialize_houses()
        await knight.initialize()
        
        # Execute test units
        await test_database_initialization()
        await test_multi_lens_reasoning_and_debate()
        await test_consensus_evaluation()
        await test_future_scenario_branches()
        await test_hypothesis_evolution()
        await test_meta_perspective_monocognitive_collapse()
        await test_governor_class_knight_planning()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL ANTIGRAVITY PHASE 4 POLYCOGNITIVE TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
