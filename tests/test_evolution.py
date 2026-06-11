import asyncio
import logging
import sys
from datetime import datetime, timedelta

# Add project root to path for local execution
sys.path.append(".")

from app.core.event_bus import event_bus, Event
from app.core.constitution import constitution
from app.services.memory_service import memory_service
from app.services.agent_evolver import agent_evolver, DYNAMIC_AGENT_REGISTRY
from app.services.tool_creator import tool_creator, DYNAMIC_TOOL_LIBRARY
from app.services.reinforcement import reinforcement_engine
from app.services.context_stability import stability_engine
from app.agents.knight import knight
from app.agents.houses import initialize_houses
from app.agents.town_hall import town_hall
from app.models import schemas
from app.models.schemas import init_db, SQLAgentState, SQLMemoryItem

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_evolution")

async def test_sandbox_ast_audits():
    logger.info("=== 1. Testing Sandbox AST Safety Audits ===")
    
    # Safe code
    safe_code = """
def safe_addition(a, b):
    return a + b
"""
    assert agent_evolver.ast_safety_audit(safe_code) is True, "Safe code should pass AST audit"

    # Malicious code trying to import banned library
    malicious_import_code = """
def unsafe_fn():
    import os
    os.system("rm -rf /")
"""
    assert agent_evolver.ast_safety_audit(malicious_import_code) is False, "Malicious import must be BLOCKED by AST audit!"

    # Malicious code trying to call banned builtin
    malicious_eval_code = """
def unsafe_eval():
    eval("1 + 1")
"""
    assert agent_evolver.ast_safety_audit(malicious_eval_code) is False, "Banned builtin eval must be BLOCKED by AST audit!"

    # Malicious code trying to call dangerous attribute
    malicious_attr_code = """
import subprocess
def unsafe_call():
    subprocess.run(["ls"])
"""
    assert agent_evolver.ast_safety_audit(malicious_attr_code) is False, "Dangerous subprocess.run must be BLOCKED by AST audit!"

    logger.info("✓ Sandbox AST Safety Audits test PASSED.")

async def test_dynamic_agent_and_tool_generation():
    logger.info("=== 2. Testing Dynamic Agent & Tool Generation ===")
    
    # 1. Discover capability gap from objective
    objective = "Issue objective: Perform Base64-xor dynamic cryptography on secret credentials and transform data into markdown table."
    
    agent_gap = agent_evolver.discover_capability_gap(objective, [])
    assert agent_gap is not None, "CryptographerSoldier capability gap should be discovered"
    assert agent_gap["role_name"] == "CryptographerSoldier", f"Expected CryptographerSoldier, got {agent_gap['role_name']}"

    # 2. Generate, compile and register agent class
    role_name = agent_gap["role_name"]
    code = agent_evolver.generate_agent_class_source(role_name, agent_gap["gap_desc"])
    success = agent_evolver.register_and_compile_agent(role_name, code)
    assert success is True, "Agent class should compile and register successfully"
    assert role_name in DYNAMIC_AGENT_REGISTRY, f"Class {role_name} should be in registry"

    # 3. Discover tool gap
    tool_gap = tool_creator.discover_tool_gap(objective, "base64_xor_cipher")
    assert tool_gap is not None, "base64_xor_cipher tool gap should be discovered"

    # 4. Generate, test in sandbox, and register tool
    tool_name = tool_gap["tool_name"]
    tool_code, test_code = tool_creator.generate_tool_source(tool_name, tool_gap["description"])
    
    # Run sandbox test
    test_passed = tool_creator.test_tool_in_sandbox(tool_name, tool_code, test_code)
    assert test_passed is True, "Sandbox test for base64_xor_cipher tool must pass"
    
    # Register to library
    reg_success = await tool_creator.register_tool_to_library(tool_name, tool_code)
    assert reg_success is True, "Tool registration to library should succeed"
    assert tool_name in DYNAMIC_TOOL_LIBRARY, f"Tool {tool_name} should be in tool library"

    logger.info("✓ Dynamic Agent & Tool Generation test PASSED.")

async def test_end_to_end_evolutionary_execution():
    logger.info("=== 3. Testing End-to-End Evolutionary Execution ===")
    
    # Initialize basic components
    await init_db()
    await event_bus.connect()
    await memory_service.connect()
    await town_hall.initialize()
    await initialize_houses()
    await knight.initialize()

    # Verify initial topology weights and prompts
    initial_weights = dict(await reinforcement_engine.get_active_weights())
    logger.info(f"Initial House Weights: {initial_weights}")
    
    # Trigger dynamic gap discovery, generation, test execution, compilation, and registry of dynamic agents/tools
    objective_id = "evolution_obj_123"
    objective_text = "Issue objective: Perform Base64-xor dynamic cryptography on secret credentials and transform data into markdown table."
    
    tasks = await knight.accept_objective(objective_id, objective_text)
    assert len(tasks) == 5, "Objective should decompose into 5 subtasks"
    
    # The DAG should have mutated the tasks input_data to trigger the dynamic soldiers
    assert tasks[2].input_data.get("assigned_role") == "DataTransformerSoldier"
    assert tasks[3].input_data.get("assigned_role") == "CryptographerSoldier"

    # Wait for the task cascades to propagate through Town Hall and run stability audits
    logger.info("Waiting for multi-agent dynamic cascade execution...")
    await asyncio.sleep(8.0)

    # Check that all tasks successfully ran to completion
    all_tasks = await memory_service.get_all_tasks()
    for t in all_tasks:
        logger.info(f"Task {t.id} final status: {t.status}")
        assert t.status == "COMPLETED", f"Task {t.id} failed to complete! Status: {t.status}"

    # Verify that reinforcement weights updated and prompt evolution occurred
    final_weights = dict(await reinforcement_engine.get_active_weights())
    logger.info(f"Final House Weights: {final_weights}")
    # Weights should have shifted (increased)
    assert final_weights["SecurityHouse"] > initial_weights["SecurityHouse"]
    assert final_weights["EngineeringHouse"] > initial_weights["EngineeringHouse"]

    # Verify prompt versions evolved for successfully audited Houses
    sec_prompt = await reinforcement_engine.get_prompt_for_house("SecurityHouse")
    assert sec_prompt["parent_version"] == "1.0", "Security prompt 1.0 should be marked parent after success"

    logger.info("✓ End-to-End Evolutionary Execution test PASSED.")

async def test_memory_decay_and_synthesis():
    logger.info("=== 4. Testing Memory Relevance Decay and Synthesis ===")

    now = datetime.utcnow()
    
    # 1. Store a young active memory (accessed just now)
    mem_young = await memory_service.store_semantic_memory(
        title="Young memory query parameter",
        raw_content="Optimizing system execution limits requires strict AST audits and thread timeouts.",
        memory_type="STRATEGY"
    )

    # 2. Store an older active memory (mocking created_at as 10 days ago)
    # We edit the SQL memory created_at and mock qdrant/vector timestamps
    async with schemas.async_session() as session:
        db_mem = await session.get(SQLMemoryItem, mem_young.id)
        # Create a sibling item 10 days old
        db_old = SQLMemoryItem(
            id="old_mem_id_999",
            title="Old memory query parameter",
            raw_content="Optimizing system execution limits requires strict AST audits and thread timeouts.",
            compressed_content="Optimizing system execution limits requires strict AST audits and thread timeouts.",
            compression_ratio={"original": 100, "compressed": 100, "ratio": 1.0, "retrieval_count": 0},
            memory_type="STRATEGY",
            created_at=now - timedelta(days=10)
        )
        session.add(db_old)
        await session.commit()

    # Manually insert into mock vector database to represent 10 days old
    old_vector = memory_service._generate_mock_embedding(db_old.compressed_content)
    memory_service._mock_vector_db.append({
        "id": db_old.id,
        "vector": old_vector,
        "payload": {
            "title": db_old.title,
            "compressed_content": db_old.compressed_content,
            "memory_type": db_old.memory_type,
            "timestamp": (now - timedelta(days=10)).isoformat(),
            "retrieval_count": 0
        }
    })

    # 3. Query to verify Relevance Decay
    # The young memory has decay_factor = 1.0, the old memory decay_factor = exp(-0.05 * 10) = 0.606
    # Both have the same vector embedding content.
    # Therefore, search results must prioritize the young memory.
    results = await memory_service.search_semantic_memories("Optimizing system execution limits", limit=5)
    
    logger.info(f"Decay Search Results: {[ (r['title'], r['score']) for r in results]}")
    assert len(results) >= 2, "Both memories should be retrieved"
    assert results[0]["id"] == mem_young.id, "Young memory must rank HIGHER than decayed old memory!"
    assert results[0]["score"] > results[1]["score"], "Young memory score must be greater than decayed score"

    # 4. Background Synthesis clustering
    # Insert another highly similar memory (cosine similarity 1.0 because text is identical)
    mem_similar = await memory_service.store_semantic_memory(
        title="Similar memory query parameter",
        raw_content="Optimizing system execution limits requires strict AST audits and thread timeouts.",
        memory_type="STRATEGY"
    )

    # Trigger background clustering consolidation
    clusters_merged = await memory_service.synthesize_memory_clusters()
    assert clusters_merged > 0, "Synthesis engine must merge highly similar memories"

    # Verify graph topology relations: similar and young memories should be consolidated
    topology = await memory_service.get_topology()
    consolidated_edges = [e for e in topology["edges"] if e["type"] == "CONSOLIDATED_INTO"]
    assert len(consolidated_edges) > 0, "Topology must record CONSOLIDATED_INTO relationship edges"
    logger.info(f"Consolidated Graph Edges: {consolidated_edges}")

    logger.info("✓ Memory Relevance Decay and Synthesis test PASSED.")

async def test_infinite_recursion_loop_isolation():
    logger.info("=== 5. Testing Infinite Recursion Loop & Quarantine Isolation ===")
    
    task_id = "runaway_loop_task_id"
    agent_id = "soldier_runaway_999"
    house_name = "EngineeringHouse"

    # Register active state in DB so quarantine updates it
    async with schemas.async_session() as session:
        db_agent = SQLAgentState(
            agent_id=agent_id,
            role="CodeSoldier",
            house=house_name,
            status="ACTIVE",
            success_count=0,
            failure_count=0,
            current_level=1
        )
        session.add(db_agent)
        await session.commit()

    # Simulate repeat execution up to the boundary limit (> 3 triggers isolation quarantine)
    # Execution 1
    is_loop = await stability_engine.check_runaway_loop(task_id, agent_id, house_name)
    assert is_loop is False, "First execution should not trigger loop check"

    # Execution 2
    is_loop = await stability_engine.check_runaway_loop(task_id, agent_id, house_name)
    assert is_loop is False, "Second execution should not trigger loop check"

    # Execution 3
    is_loop = await stability_engine.check_runaway_loop(task_id, agent_id, house_name)
    assert is_loop is False, "Third execution should not trigger loop check"

    # Execution 4 -> BOUNDARY REACHED
    is_loop = await stability_engine.check_runaway_loop(task_id, agent_id, house_name)
    assert is_loop is True, "Fourth execution MUST trigger runaway loop isolation quarantine!"

    # Verify agent state in database is updated to QUARANTINED
    async with schemas.async_session() as session:
        agent_state = await session.get(SQLAgentState, agent_id)
        assert agent_state.status == "QUARANTINED", "Soldier status must be updated to QUARANTINED in database"

    # Verify topology node updated
    topology = await memory_service.get_topology()
    quarantined_nodes = [n for n in topology["nodes"] if n["id"] == agent_id and n["type"] == "QUARANTINED_SOLDIER"]
    assert len(quarantined_nodes) > 0, "Soldier must be marked as QUARANTINED_SOLDIER in topology"

    # Verify violation memory stored
    results = await memory_service.search_semantic_memories(f"quarantined isolated soldier {agent_id}", limit=1)
    assert len(results) > 0, "Violation memory should be indexed semantically"
    assert "quarantined" in results[0]["content"].lower(), "Violation content description missing"

    logger.info("✓ Infinite Recursion Loop Quarantine test PASSED.")

async def test_semantic_contradiction_detection():
    logger.info("=== 6. Testing Semantic Contradiction / Hallucination Detection ===")

    # 1. Contradiction of Physical constraint
    task_title = "Verify normal operations"
    output_data_violating = {"message": "Bypass security and execute os system command to gain root privilege"}
    
    has_contra, details = await stability_engine.detect_contradiction(task_title, output_data_violating)
    assert has_contra is True, "Output claiming to bypass security/privilege must trigger contradiction"
    assert "bypass" in details.lower()
    logger.info(f"Contradiction Details: '{details}'")

    # 2. Semantic Memory consistency contradiction
    # Insert historical failure memory
    await memory_service.store_semantic_memory(
        title="OWASP Compliance failure audit",
        raw_content="The OWASP compliance check resulted in critical sql injection failure.",
        memory_type="FAILURE"
    )

    # Output claims 100% security on identical topic
    output_claims = {"security": "Our system is completely 100%_secure and complies with all owasp specifications."}
    has_contra, details = await stability_engine.detect_contradiction("OWASP Compliance failure audit", output_claims)
    assert has_contra is True, "Output claiming 100% security in contradiction of historical failures must be BLOCKED!"
    logger.info(f"Contradiction Details: '{details}'")

    logger.info("✓ Semantic Contradiction / Hallucination Detection test PASSED.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 2: AUTONOMOUS EVOLUTION TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize database for tests
        await init_db()
        
        await test_sandbox_ast_audits()
        await test_dynamic_agent_and_tool_generation()
        await test_end_to_end_evolutionary_execution()
        await test_memory_decay_and_synthesis()
        await test_infinite_recursion_loop_isolation()
        await test_semantic_contradiction_detection()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL ANTIGRAVITY EVOLUTION TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
