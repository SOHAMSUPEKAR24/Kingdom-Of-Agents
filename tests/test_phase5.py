import asyncio
import logging
import sys
from datetime import datetime
from sqlalchemy import select

# Add project root to path for local execution
sys.path.append(".")

from app.core.event_bus import event_bus, Event
from app.services.memory_service import memory_service
from app.agents.knight import knight
from app.agents.houses import initialize_houses
from app.agents.town_hall import town_hall
from app.models import schemas
from app.models.schemas import (
    init_db, SQLWorldModel, SQLThoughtNode, SQLThoughtEdge, SQLCivilizationDoctrine,
    SQLSelfReflection, SQLStrategicForecast, SQLTask
)
from app.services.meta_cognitive_engine import (
    meta_cognitive_swarm, self_reflection_system, causal_inference, stability_sanity_engine,
    meta_cognitive_engine, world_model_engine, recursive_reasoning, doctrine_synthesis,
    priority_governor, horizon_forecaster
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase5")

async def test_database_initialization():
    logger.info("=== 1. Testing Relational DB Schema Initialization for Phase 5 ===")
    
    async with schemas.async_session() as session:
        # Check world models
        wm_res = await session.execute(select(SQLWorldModel))
        logger.info(f"Existing world models: {len(wm_res.scalars().all())}")

        # Check thought nodes
        tn_res = await session.execute(select(SQLThoughtNode))
        logger.info(f"Existing thought nodes: {len(tn_res.scalars().all())}")

        # Check thought edges
        te_res = await session.execute(select(SQLThoughtEdge))
        logger.info(f"Existing thought edges: {len(te_res.scalars().all())}")

        # Check civilization doctrines
        cd_res = await session.execute(select(SQLCivilizationDoctrine))
        logger.info(f"Existing civilization doctrines: {len(cd_res.scalars().all())}")

        # Check self reflections
        sr_res = await session.execute(select(SQLSelfReflection))
        logger.info(f"Existing self reflections: {len(sr_res.scalars().all())}")

        # Check strategic forecasts
        sf_res = await session.execute(select(SQLStrategicForecast))
        logger.info(f"Existing strategic forecasts: {len(sf_res.scalars().all())}")
        
    logger.info("✓ Relational DB Schema Initialization test PASSED.")

async def test_pre_objective_audit():
    logger.info("=== 2. Testing Pre-Objective Cognitive Audits ===")
    
    objective_id = "test_obj_phase5_audit"
    raw_objective = "Implement high-concurrency zstd memory compression filters."
    
    # Trigger pre-objective audit
    audit_results = await meta_cognitive_swarm.execute_pre_objective_audit(objective_id, raw_objective)
    
    assert audit_results["world_sim"] is not None
    assert audit_results["thought_nodes_count"] == 4 # Stage 1-4 nodes
    assert audit_results["sanity"]["status"] == "STABLE"
    assert audit_results["forecast_id"] is not None
    
    # Assert database persistence
    async with schemas.async_session() as session:
        # Verify 5 thought nodes created for audit sequence (4 stage thoughts + 1 world state projection)
        res = await session.execute(select(SQLThoughtNode).where(SQLThoughtNode.objective_id == objective_id))
        nodes = res.scalars().all()
        logger.info(f"Thought nodes found in DB for audit: {[n.id for n in nodes]}")
        assert len(nodes) == 5
        
        # Verify thought edges exist for sequential stages
        res_edges = await session.execute(select(SQLThoughtEdge))
        edges = res_edges.scalars().all()
        assert len(edges) >= 3
        
        # Verify world state has SQLite database node updated to STRESSED due to 'concurrency' in objective
        res_wm = await session.execute(select(SQLWorldModel).where(SQLWorldModel.id == "env_sqlite_db"))
        db_node = res_wm.scalars().first()
        assert db_node is not None
        assert db_node.status == "STRESSED"
        
        # Verify strategic forecast has been recorded
        res_sf = await session.execute(select(SQLStrategicForecast).where(SQLStrategicForecast.id == audit_results["forecast_id"]))
        forecast = res_sf.scalars().first()
        assert forecast is not None
        assert forecast.forecast_type == "STABILITY_RISK"
        assert forecast.target_horizon == "LONG_TERM"
        
    logger.info("✓ Pre-objective cognitive audit pipeline and persistence PASSED.")

async def test_runaway_recursion_circuit_breaker():
    logger.info("=== 3. Testing Runaway Recursion Circuit Breaker ===")
    
    objective_id = "test_obj_runaway_loop"
    
    # Add > 20 mock thought nodes to trigger recursive overload quarantine
    async with schemas.async_session() as session:
        for idx in range(25):
            node = SQLThoughtNode(
                id=f"thought_node_{objective_id}_mock_{idx}",
                objective_id=objective_id,
                type="LENS",
                title=f"Mock node {idx}",
                summary="Sustaining runaway loops for resilience auditing."
            )
            session.add(node)
        await session.commit()
        
    # Perform stability sanity check
    sanity = await stability_sanity_engine.perform_sanity_check(objective_id)
    assert sanity["status"] == "QUARANTINED_RUNAWAY"
    assert sanity["sanity_index"] < 0.20
    assert sanity["contradiction_saturation"] > 0.80
    
    logger.info("✓ Runaway recursion circuit breaker correctly quarantined saturated thought branches.")

async def test_self_reflection_and_doctrine_evolution():
    logger.info("=== 4. Testing Outcomes Reflection & Doctrine Evolution ===")
    
    objective_id = "test_obj_reflection_99"
    
    # 1. Create a dummy task matching this objective
    async with schemas.async_session() as session:
        t = SQLTask(
            id=f"{objective_id}_task_01_strategy",
            parent_objective=objective_id,
            title="Perform Strategic Alignment Check",
            assigned_house="StrategyHouse",
            status="COMPLETED"
        )
        session.add(t)
        await session.commit()
        
    # 2. Trigger self-reflection assuming prediction was 0.95
    reflection = await self_reflection_system.perform_self_reflection(objective_id, 0.95)
    
    assert reflection.objective_id == objective_id
    assert reflection.compliance_deviation == abs(0.95 - 1.0) # Succeeded so actual is 1.0
    assert "Workflow success" in reflection.derived_philosophy
    
    # Verify doctrine & thought node persistence
    async with schemas.async_session() as session:
        # Check self reflections table
        sr = await session.get(SQLSelfReflection, reflection.id)
        assert sr is not None
        assert sr.compliance_deviation == reflection.compliance_deviation
        
        # Check emergent doctrines table
        stmt = select(SQLCivilizationDoctrine).where(SQLCivilizationDoctrine.title.like(f"%{objective_id}%"))
        res = await session.execute(stmt)
        doctrine = res.scalars().first()
        assert doctrine is not None
        assert "Plan B topology" in doctrine.philosophy_text
        
        # Check thought nodes table
        res_node = await session.execute(select(SQLThoughtNode).where(SQLThoughtNode.objective_id == objective_id, SQLThoughtNode.type == "REFLECTION"))
        t_node = res_node.scalars().first()
        assert t_node is not None
        assert "derived philosophy" in t_node.summary.lower() or "derived doctrine" in t_node.summary.lower()
        
    logger.info("✓ Self-Reflection Outcomes Audit and emergent doctrine synthesis PASSED.")

async def test_causal_inference_failure_diagnosis():
    logger.info("=== 5. Testing Causal Inference Backward Backtrace ===")
    
    objective_id = "test_obj_causal_88"
    
    # Set up objective subtasks: task_01 COMPLETED, task_02 FAILED, task_03 PENDING
    async with schemas.async_session() as session:
        t1 = SQLTask(
            id=f"{objective_id}_task_01_strategy",
            parent_objective=objective_id,
            title="Formulate Strategy",
            assigned_house="StrategyHouse",
            status="COMPLETED"
        )
        t2 = SQLTask(
            id=f"{objective_id}_task_02_engineering",
            parent_objective=objective_id,
            title="Build Core Modules",
            assigned_house="EngineeringHouse",
            status="FAILED",
            dependencies=[t1.id]
        )
        t3 = SQLTask(
            id=f"{objective_id}_task_03_security",
            parent_objective=objective_id,
            title="Audit Compliance",
            assigned_house="SecurityHouse",
            status="PENDING",
            dependencies=[t2.id]
        )
        session.add(t1)
        session.add(t2)
        session.add(t3)
        await session.commit()
        
    # Diagnose failed task
    diagnosis = await causal_inference.diagnose_failure_root_cause(t2.id)
    
    assert diagnosis["failed_task_id"] == t2.id
    assert "concurrency thread locks" in diagnosis["root_cause"].lower()
    # Downstream blocked tasks should list task_03
    assert t3.id in diagnosis["cascading_impact"]
    assert "remediation" in diagnosis
    
    logger.info("✓ Backward causal backtrace and downstream blocked predictions PASSED.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 5: META-COGNITIVE SWARM INTEGRATION TESTS")
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
        await test_pre_objective_audit()
        await test_runaway_recursion_circuit_breaker()
        await test_self_reflection_and_doctrine_evolution()
        await test_causal_inference_failure_diagnosis()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL ANTIGRAVITY PHASE 5 META-COGNITIVE TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
