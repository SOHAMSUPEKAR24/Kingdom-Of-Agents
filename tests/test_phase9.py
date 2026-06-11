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
    SQLScientificDiscovery,
    SQLCausalChain,
    SQLSimulationBranch,
    SQLResearchThesis,
    SQLScientificExperiment,
    SQLTask
)
from app.services.scientific_cognition import scientific_cognition
from app.services.memory_service import memory_service
from app.core.event_bus import event_bus, Event
from app.agents.houses import houses_registry
from app.agents.factory import agent_factory
from app.agents.knight import knight

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase9")

async def test_database_initialization():
    logger.info("=== 1. Testing Database Table Initialization ===")
    # Databases should be initialized by main/init_db.
    # We will run a select statement on each of the 5 new models to assert they work perfectly.
    from sqlalchemy import select
    async with schemas.async_session() as session:
        # 1. SQLScientificDiscovery
        res_disc = await session.execute(select(SQLScientificDiscovery).limit(1))
        disc = res_disc.scalars().all()
        assert isinstance(disc, list), "Scientific Discovery table must select."

        # 2. SQLCausalChain
        res_causal = await session.execute(select(SQLCausalChain).limit(1))
        causal = res_causal.scalars().all()
        assert isinstance(causal, list), "Causal Chain table must select."

        # 3. SQLSimulationBranch
        res_branch = await session.execute(select(SQLSimulationBranch).limit(1))
        branch = res_branch.scalars().all()
        assert isinstance(branch, list), "Simulation Branch table must select."

        # 4. SQLResearchThesis
        res_thesis = await session.execute(select(SQLResearchThesis).limit(1))
        thesis = res_thesis.scalars().all()
        assert isinstance(thesis, list), "Research Thesis table must select."

        # 5. SQLScientificExperiment
        res_exp = await session.execute(select(SQLScientificExperiment).limit(1))
        exp = res_exp.scalars().all()
        assert isinstance(exp, list), "Scientific Experiment table must select."

    logger.info("✓ All 5 new relational database tables initialized perfectly.")

async def test_scientific_cognition_service_pipelines():
    logger.info("=== 2. Testing Scientific Cognition Service Pipelines ===")
    
    # 1. Telemetry / deep world model network
    telemetry = await scientific_cognition.deep_world_model_network()
    assert "cpu_utilization" in telemetry, "Telemetry must calculate CPU utilization."
    assert "database_latency_ms" in telemetry, "Telemetry must calculate DB latency."
    
    # 2. Hypothesis generation
    hypotheses = await scientific_cognition.hypothesis_generation_validation_system()
    assert len(hypotheses) > 0, "Hypothesis system must propose at least one thesis."
    
    # 3. Causal discovery engine
    causal_chains = await scientific_cognition.causal_discovery_engine()
    assert len(causal_chains) > 0, "Causal discovery must return populated causal chains."
    
    # 4. Experimentation lab & simulated branches
    experiment = await scientific_cognition.experimentation_simulation_civilization_lab()
    assert experiment.id is not None, "Experiment must be logged with valid ID."
    assert experiment.status == "COMPLETED", "Experiment status must be COMPLETED."
    
    async with schemas.async_session() as session:
        from sqlalchemy import select
        res_branch = await session.execute(
            select(SQLSimulationBranch).where(SQLSimulationBranch.experiment_id == experiment.id)
        )
        branches = res_branch.scalars().all()
        assert len(branches) >= 3, "Experiment lab run must auto-spawn branching timelines."
        
    logger.info("✓ Core scientific cognition pipelines completed successfully.")

async def test_specialized_houses_and_soldiers():
    logger.info("=== 3. Testing Specialized Research Houses & Soldiers ===")
    
    # Houses mapping
    target_houses = [
        "ScientificDiscoveryHouse", "CausalAnalysisHouse", "SimulationResearchHouse",
        "TheoryValidationHouse", "UncertaintyReasoningHouse", "InfrastructureScienceHouse",
        "StrategicForecastingHouse", "AbstractionSynthesisHouse"
    ]
    
    # Assert houses are registered
    for h_name in target_houses:
        assert h_name in houses_registry, f"House '{h_name}' must be registered."
        house = houses_registry[h_name]
        assert house.house_name == h_name, "Registered house name must match."
        
    # Test spawner of specialized soldiers
    soldiers_roles = {
        "DiscoverySoldier": "SCIENTIFIC_DISCOVERY",
        "CausalSoldier": "CAUSAL_ANALYSIS",
        "SimulationResearchSoldier": "SIMULATION_RESEARCH",
        "TheorySoldier": "THEORY_VALIDATION",
        "UncertaintySoldier": "UNCERTAINTY_REASONING",
        "InfraScienceSoldier": "INFRASTRUCTURE_SCIENCE",
        "StrategicForecastingSoldier": "STRATEGIC_FORECASTING",
        "AbstractionSoldier": "ABSTRACTION_SYNTHESIS"
    }
    
    for role, perm in soldiers_roles.items():
        soldier = await agent_factory.spawn_soldier(role, "ScientificDiscoveryHouse")
        assert soldier.role == role, f"Spawned soldier role must be {role}."
        assert perm in soldier.permissions, f"Soldier {role} must possess custom permission '{perm}'."
        # Retire the soldier
        await soldier.retire()
        
    logger.info("✓ Evolved Research Houses and specialized Soldier permissions verified.")

async def test_failure_to_theory_conversion():
    logger.info("=== 4. Testing Failure-To-Theory Conversion ===")
    
    task_id = "task_test_fail_123"
    error_msg = "Database deadlocks observed due to overlapping transactional locks under SQLite fallback"
    
    discovery = await scientific_cognition.failure_to_theory_conversion_system(task_id, error_msg)
    assert discovery.id is not None, "Failure conversion must create a valid Discovery."
    assert "Database deadlocks" in discovery.evidence_summary, "Evidence summary must document the crash."
    assert "Safe operation protocols" in discovery.derived_theory, "Derived theory must contain caution directives."
    
    logger.info("✓ Sudden task failure converted perfectly into protective caution doctrine.")

async def test_reality_consistency_sanity_governor():
    logger.info("=== 5. Testing Reality Consistency & Sanity Governor ===")
    
    # Safe theory
    safe_title = "Async write-batching under concurrent writes"
    safe_text = "Enforcing sequential queue buffering mitigates transaction locking overhead."
    is_safe = await scientific_cognition.reality_consistency_sanity_governor(safe_title, safe_text)
    assert is_safe is True, "Consistent logical theory must be approved."
    
    # Unsafe theory: circular reasoning or hallucination term
    unsafe_title = "Instant absolute certainty protocol"
    unsafe_text = "Infinite loop validation guarantees absolute certainty during node network operations."
    is_unsafe = await scientific_cognition.reality_consistency_sanity_governor(unsafe_title, unsafe_text)
    assert is_unsafe is False, "Governor must veto hallucinated or circular reasoning statements."
    
    logger.info("✓ Reality Consistency Sanity Governor vetoed unsafe theories successfully.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 9: SCIENTIFIC COGNITION TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize SQLite fallback memory database for isolated execution
        await init_db()
        await event_bus.connect()
        await memory_service.connect()
        
        await test_database_initialization()
        await test_scientific_cognition_service_pipelines()
        await test_specialized_houses_and_soldiers()
        await test_failure_to_theory_conversion()
        await test_reality_consistency_sanity_governor()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL PHASE 9 SCIENTIFIC CIVILIZATION TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
