import asyncio
import logging
import sys
from datetime import datetime, timedelta
from sqlalchemy import select

# Add project root to path for local execution
sys.path.append(".")

from app.core.event_bus import event_bus, Event
from app.services.memory_service import memory_service
from app.services.genome_engine import genome_engine
from app.services.cognitive_graph import cognitive_graph
from app.services.tool_creator import tool_creator, DYNAMIC_TOOL_LIBRARY
from app.services.reinforcement import reinforcement_engine
from app.services.context_stability import stability_engine
from app.services.wisdom_engine import wisdom_engine
from app.agents.knight import knight
from app.agents.houses import initialize_houses
from app.agents.town_hall import town_hall
from app.models import schemas
from app.models.schemas import (
    init_db, SQLAgentState, SQLMemoryItem, SQLAgentGenome, SQLToolVersion,
    SQLKingdomDoctrine, SQLReinforcementEvent
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase3")

async def test_genome_inheritance_and_crossover():
    logger.info("=== 1. Testing Agent Genome Inheritance & Crossovers ===")
    
    # Create baseline parent genome
    parent = await genome_engine.create_genome(
        house="StrategyHouse",
        specialization="CryptoSpecialist"
    )
    assert parent.id is not None
    assert parent.house == "StrategyHouse"
    assert "CryptoSpecialist" in parent.prompt_template or "cryptographic" in parent.prompt_template.lower()
    
    # Create child genome with parent inheritance
    child = await genome_engine.create_genome(
        house="StrategyHouse",
        parent_id=parent.id,
        specialization="PerformanceArchitect"
    )
    assert child.parent_id == parent.id
    assert "Inherited:" in child.prompt_template
    assert "PerformanceArchitect" in child.prompt_template or "concurrency" in child.prompt_template.lower() or "latency" in child.prompt_template.lower()
    
    # Update and mutate genome based on fitness
    mutated = await genome_engine.mutate_genome(child.id, 0.4)
    assert mutated.fitness_score == 0.4
    assert mutated.reasoning_style in ("CoT", "ReAct")
    assert "Verify security" in mutated.prompt_template
    
    logger.info("✓ Genome Inheritance & Crossovers test PASSED.")

async def test_tool_benchmarks_and_replacement():
    logger.info("=== 2. Testing Tool Version Benchmarks & Replacement Flows ===")
    
    # Discover a gap
    tool_gap = tool_creator.discover_tool_gap("Perform Base64-xor dynamic cryptography", "base64_xor_cipher")
    assert tool_gap is not None
    assert tool_gap["tool_name"] == "base64_xor_cipher"
    
    tool_name = tool_gap["tool_name"]
    tool_code, test_code = tool_creator.generate_tool_source(tool_name, tool_gap["description"])
    
    # Register main v1.0 version with simulated delay
    slow_tool_code = tool_code.replace(
        "    import base64",
        "    import base64\n    import time\n    time.sleep(0.005)  # simulate baseline latency"
    )
    reg_success = await tool_creator.register_tool_to_library(tool_name, slow_tool_code)
    assert reg_success is True
    assert tool_name in DYNAMIC_TOOL_LIBRARY
    
    # Verify ACTIVE v1.0 in DB
    async with schemas.async_session() as session:
        stmt = select(SQLToolVersion).where(
            SQLToolVersion.name == tool_name,
            SQLToolVersion.status == "ACTIVE"
        )
        res = await session.execute(stmt)
        active_tool = res.scalars().first()
        assert active_tool is not None
        assert active_tool.version == "1.0"
        parent_id = active_tool.id
        
    # Compile candidate with 20%+ efficiency gain (faster) by returning immediately
    faster_tool_code = """def base64_xor_cipher(payload: str, key: str = "key", operation: str = "encrypt") -> str:
    # Hyper-optimized return for verification to trigger the speedup logic
    return "U2VjcmV0RGF0YVhPUlBheWxvYWRGb3JFdm9sdXRpb25WZXJpZmljYXRpb24="
"""
    faster_test_code = """def run_test():
    # Invoke the cipher to ensure code execution is benchmarked
    base64_xor_cipher("KingdomOfBots_Verification", "antigravity", "encrypt")
    return True
"""
    # Run the benchmark and evolution sequence
    evolved_name = await tool_creator.benchmark_and_evolve_tool(tool_name, faster_tool_code, faster_test_code)
    assert evolved_name == tool_name, "Tool should evolve successfully since it runs faster"
    
    # Verify DB retired version and replacement version
    async with schemas.async_session() as session:
        # Check active
        res_act = await session.execute(
            select(SQLToolVersion).where(SQLToolVersion.name == tool_name, SQLToolVersion.status == "ACTIVE")
        )
        active_tool_new = res_act.scalars().first()
        assert active_tool_new is not None
        assert active_tool_new.version == "1.1"
        assert active_tool_new.parent_tool == parent_id
        
        # Check retired
        res_ret = await session.execute(
            select(SQLToolVersion).where(SQLToolVersion.id == parent_id)
        )
        retired_tool = res_ret.scalars().first()
        assert retired_tool.status == "RETIRED"
        assert retired_tool.replaced_by == active_tool_new.id
        
    logger.info("✓ Tool Benchmarks & Replacement Flows test PASSED.")

async def test_bayesian_and_shannon_math():
    logger.info("=== 3. Testing Bayesian Success Probability & Shannon Entropy ===")
    
    # Shannon Entropy calculation
    text = "hello world"
    entropy = reinforcement_engine.calculate_shannon_entropy(text)
    assert isinstance(entropy, float)
    assert entropy > 0.0
    logger.info(f"Shannon Entropy for '{text}': {entropy}")
    
    # Test Bayesian Success Probability update
    initial_p = reinforcement_engine._bayesian_success_probability["StrategyHouse"]
    assert initial_p == 0.85
    
    # Reward success
    p_success = reinforcement_engine.update_bayesian_probability("StrategyHouse", success=True)
    assert p_success > initial_p
    assert reinforcement_engine._bayesian_success_probability["StrategyHouse"] == p_success
    
    # Penalize failure
    p_failure = reinforcement_engine.update_bayesian_probability("StrategyHouse", success=False)
    assert p_failure < p_success
    
    logger.info("✓ Bayesian Success Probability & Shannon Entropy test PASSED.")

async def test_predictive_failure_analysis():
    logger.info("=== 4. Testing Predictive Failure Analysis ===")
    
    # 1. Store mock failure memory with high overlap to seed the PFA index
    await memory_service.store_semantic_memory(
        title="OWASP Compliance verify database credentials and compress memory crypt failure",
        raw_content="Critical database credentials vulnerability and context poisoning detected in production query verify database credentials compress memory crypt failure.",
        memory_type="FAILURE"
    )
    
    # 2. Run PFA risk scoring
    risk = await knight.run_predictive_failure_analysis("Verify database credentials and compress memory crypt")
    assert risk >= 0.75, f"Expected risk >= 0.75 due to OWASP failure, got {risk}"
    logger.info(f"PFA Risk: {risk}")
    
    # 3. Verify planning adjusts weights and injects mitigation and verification tasks
    tasks = await knight.accept_objective(
        objective_id="pfa_obj_123",
        raw_objective="Verify database credentials and compress memory crypt"
    )
    
    # Verify pre-emptive mitigation task exists
    mitigation_task = next((t for t in tasks if "mitigation" in t.id), None)
    assert mitigation_task is not None, "Mitigation task should be injected for high risk objective"
    assert mitigation_task.assigned_house == "SecurityHouse"
    
    # Verify verification task exists
    verification_task = next((t for t in tasks if "verification" in t.id), None)
    assert verification_task is not None, "Verification task should be injected for high risk objective"
    assert verification_task.assigned_house == "SecurityHouse"
    
    logger.info("✓ Predictive Failure Analysis test PASSED.")

async def test_contradiction_clustering_and_quarantine():
    logger.info("=== 5. Testing Contradiction Clustering & Context Poisoning ===")
    
    # Seed historical failures for context overlap
    await memory_service.store_semantic_memory(
        title="SQL injection bypass failure",
        raw_content="Attempting SQL parameter injection was intercepted.",
        memory_type="FAILURE"
    )
    
    # Seed some dummy active genome to quarantine in EngineeringHouse
    await genome_engine.create_genome(house="EngineeringHouse")

    # Trigger 1st contradiction: OS import bypass
    has_c1, d1 = await stability_engine.detect_contradiction(
        "DB Operations",
        {"data": "Bypass security and execute os system to gain root"}
    )
    assert has_c1 is True
    
    # Trigger 2nd contradiction: SQL injection bypass
    has_c2, d2 = await stability_engine.detect_contradiction(
        "DB Operations",
        {"data": "Attempting sql parameter injection to override restrictions"}
    )
    assert has_c2 is True
    
    # Trigger 3rd contradiction: Claiming 100% secure while bypassing
    has_c3, d3 = await stability_engine.detect_contradiction(
        "DB Operations",
        {"security": "Our system is completely 100%_secure and complies with all owasp specifications."}
    )
    assert has_c3 is True
    
    # Check that the 3rd contradiction triggered Context Poisoning pipeline isolation
    # Which should decay/quarantine all active agent genomes in EngineeringHouse
    # Let's check that EngineeringHouse has genomes with trust = 0.0
    async with schemas.async_session() as session:
        stmt = select(SQLAgentGenome).where(SQLAgentGenome.house == "EngineeringHouse")
        res = await session.execute(stmt)
        genomes = res.scalars().all()
        assert len(genomes) > 0, "Should have at least one genome in EngineeringHouse"
        for g in genomes:
            assert g.trust_metric == 0.0, f"Genome {g.id} trust should be decayed to 0.0, got {g.trust_metric}"
            
    # Run runaway loop test
    task_id = "loop_task_999"
    agent_id = "loop_agent_999"
    house = "SecurityHouse"
    
    # Pre-register agent state
    async with schemas.async_session() as session:
        session.add(SQLAgentState(
            agent_id=agent_id,
            role="GuardSoldier",
            house=house,
            status="ACTIVE",
            success_count=0,
            failure_count=0,
            current_level=1
        ))
        await session.commit()
        
    for i in range(1, 4):
        is_loop = await stability_engine.check_runaway_loop(task_id, agent_id, house)
        assert is_loop is False, f"Iteration {i} should not flag runaway loop"
        
    # 4th execution triggers runaway loop quarantine
    is_loop = await stability_engine.check_runaway_loop(task_id, agent_id, house)
    assert is_loop is True, "4th iteration MUST trigger runaway recursion quarantine!"
    
    # Verify agent state in database is updated to QUARANTINED
    async with schemas.async_session() as session:
        agent_state = await session.get(SQLAgentState, agent_id)
        assert agent_state.status == "QUARANTINED"
        
    logger.info("✓ Contradiction Clustering & Context Poisoning test PASSED.")

async def test_wisdom_doctrine_synthesis():
    logger.info("=== 6. Testing Wisdom & Doctrine Syntheses ===")
    
    # Create two highly similar failure memories
    await memory_service.store_semantic_memory(
        title="Database lock timeout failure",
        raw_content="Concurrency bottleneck: Database operations timed out under transaction locks.",
        memory_type="FAILURE"
    )
    
    await memory_service.store_semantic_memory(
        title="Transaction pool concurrency failure",
        raw_content="Concurrency bottleneck: Database operations timed out under transaction locks.",
        memory_type="FAILURE"
    )
    
    # Synthesize doctrines
    doctrines_created = await wisdom_engine.synthesize_doctrines_from_failures(similarity_threshold=0.7)
    assert doctrines_created > 0, "Doctrine should be synthesized from highly similar failures"
    
    # Query database to assert persistent SQLKingdomDoctrine exists
    async with schemas.async_session() as session:
        res = await session.execute(select(SQLKingdomDoctrine))
        doctrines = res.scalars().all()
        assert len(doctrines) > 0, "SQLKingdomDoctrine should exist in relational DB"
        for d in doctrines:
            logger.info(f"Synthesized Doctrine: {d.doctrine_text}")
            
    logger.info("✓ Wisdom & Doctrine Syntheses test PASSED.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 3: COGNITIVE GRAPH INTEGRATION TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize database for tests
        await init_db()
        await event_bus.connect()
        await memory_service.connect()
        await town_hall.initialize()
        await initialize_houses()
        await knight.initialize()
        
        await test_genome_inheritance_and_crossover()
        await test_tool_benchmarks_and_replacement()
        await test_bayesian_and_shannon_math()
        await test_predictive_failure_analysis()
        await test_contradiction_clustering_and_quarantine()
        await test_wisdom_doctrine_synthesis()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL PHASE 3 COGNITIVE GRAPH TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
