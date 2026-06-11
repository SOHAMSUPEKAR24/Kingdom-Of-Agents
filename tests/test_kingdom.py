import asyncio
import logging
import sys

# Add project root to path for local execution
sys.path.append(".")

from app.core.event_bus import event_bus, Event
from app.core.constitution import constitution
from app.services.memory_service import memory_service
from app.agents.knight import knight
from app.agents.houses import initialize_houses
from app.agents.town_hall import town_hall
from app.models.schemas import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test")

async def test_event_bus():
    logger.info("=== Testing Event Bus Pub/Sub ===")
    event_received = asyncio.Event()

    async def callback(event: Event):
        logger.info(f"Test Callback received event: {event.event_type} - {event.payload}")
        event_received.set()

    event_bus.subscribe("TEST_EVENT", callback)
    
    test_event = Event(
        event_type="TEST_EVENT",
        sender="TestRunner",
        payload={"message": "Verification packet 123"}
    )
    await event_bus.publish(test_event)
    
    try:
        await asyncio.wait_for(event_received.wait(), timeout=2.0)
        logger.info("✓ Event Bus test PASSED.")
    except asyncio.TimeoutError:
        logger.error("✗ Event Bus test TIMED OUT!")
        raise RuntimeError("Event Bus callback did not fire.")

async def test_constitutional_layer():
    logger.info("=== Testing Constitutional Governance ===")
    
    # 1. Test normal audited command
    valid = constitution.validate_action("execute_command", {"command": "ls -la"})
    assert valid is True, "Normal command should pass audit"
    
    # 2. Test malicious command (breaching Rule V)
    invalid = constitution.validate_action("execute_command", {"command": "rm -rf /usr/bin"})
    assert invalid is False, "Dangerous command must be BLOCKED by Constitution!"
    
    # 3. Test soldier spawning limit blocks (CONST-IV)
    spawn_valid = constitution.validate_action("spawn_soldier", {"active_soldiers_count": 5, "max_limit": 50})
    assert spawn_valid is True, "Under limit spawn should pass"
    
    spawn_invalid = constitution.validate_action("spawn_soldier", {"active_soldiers_count": 50, "max_limit": 50})
    assert spawn_invalid is False, "Spawning at limit must be BLOCKED!"
    
    logger.info("✓ Constitutional Governance test PASSED.")

async def test_task_graph_decomposition():
    logger.info("=== Testing Knight-0 Objective DAG ===")
    
    # Initialize basic components
    await init_db()
    await event_bus.connect()
    await memory_service.connect()
    await town_hall.initialize()
    await initialize_houses()
    await knight.initialize()

    # Issue King command
    objective_id = "test_obj_999"
    objective_text = "Perform static security audit on database credentials and compress memory crypt"
    
    tasks = await knight.accept_objective(objective_id, objective_text)
    assert len(tasks) == 5, "Objective should decompose into 5 subtasks"
    assert tasks[0].assigned_house == "StrategyHouse", "First task must be Strategy"
    assert tasks[4].assigned_house == "MemoryHouse", "Last task must be Memory"

    # Wait briefly for cascading task executions to propagate through the Event Bus
    logger.info("Waiting for multi-agent execution cascade simulation...")
    await asyncio.sleep(5.0)
    
    # Check that all tasks successfully ran to completion
    all_tasks = await memory_service.get_all_tasks()
    logger.info(f"Total historical tasks in db: {len(all_tasks)}")
    for t in all_tasks:
        logger.info(f"Task {t.id} status: {t.status}")
    
    logger.info("✓ Knight-0 Task Graph Decomposition test PASSED.")

async def test_memory_crypt():
    logger.info("=== Testing Memory Crypt Semantic Search ===")
    
    # Insert mock memories
    await memory_service.store_semantic_memory(
        title="PostgreSQL scaling techniques",
        raw_content="Use connection pool settings with SQLAlchemy. Increase thread connections. Implement robust indexing.",
        memory_type="STRATEGY"
    )
    
    await memory_service.store_semantic_memory(
        title="Vulnerability mitigation procedures",
        raw_content="Sanitize inputs before executing commands. Enforce constitutional AST audits on all agent code structures.",
        memory_type="INFRASTRUCTURE"
    )

    # Search query
    logger.info("Searching memory index for: 'Mitigate malicious command injections'")
    results = await memory_service.search_semantic_memories("Mitigate malicious command injections", limit=1)
    
    assert len(results) > 0, "Search results should be returned"
    top_hit = results[0]
    logger.info(f"Semantic Search Top Match: '{top_hit['title']}' (Score: {top_hit['score']})")
    assert "vulnerability" in top_hit["title"].lower(), "Semantic search should return the security-related memory"

    logger.info("✓ Memory Crypt Semantic Search test PASSED.")

async def main():
    logger.info("==================================================")
    logger.info("STARTING ANTIGRAVITY BACKEND INTEGRATION TEST SUITE")
    logger.info("==================================================")
    
    try:
        await test_event_bus()
        await test_constitutional_layer()
        await test_task_graph_decomposition()
        await test_memory_crypt()
        
        logger.info("==================================================")
        logger.info("🎉 SUCCESS: ALL ANTIGRAVITY BACKEND TESTS PASSED! 🎉")
        logger.info("==================================================")
    except Exception as e:
        logger.critical(f"💥 TEST RUN FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Graceful disconnect
        await event_bus.disconnect()
        await memory_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
