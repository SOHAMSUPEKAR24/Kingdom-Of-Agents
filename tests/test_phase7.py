import asyncio
import logging
import sys
from datetime import datetime

# Add project root to path for local execution
sys.path.append(".")

from app.models.schemas import init_db, SQLCognitiveNode, SQLMemoryShard, SQLFederatedGovernor, SQLCivilizationState
from app.services.distributed_civilization import distributed_civilization
from app.core.event_bus import event_bus, Event

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase7")

async def test_node_registration_and_scaling():
    logger.info("=== 1. Testing Distributed Node Registration & Mesh Scaling ===")
    
    # Check registration
    await distributed_civilization.register_node("test_node_reasoning", "STRATEGIC_REASONING")
    await distributed_civilization.register_node("test_node_worldmodel", "WORLD_MODELING")
    
    active_nodes = await distributed_civilization.get_active_nodes()
    assert len(active_nodes) >= 2, "Mesh should contain at least registered test nodes."
    
    specs = [n.specialization for n in active_nodes]
    assert "STRATEGIC_REASONING" in specs, "Should have a registered reasoning node."
    assert "WORLD_MODELING" in specs, "Should have a registered world modeling node."
    
    # Check autonomous scaling action
    scaled_id = await distributed_civilization.scale_node_mesh("DOCTRINE_GENERATION")
    assert "doctrine_generation" in scaled_id.lower(), "Scaled node ID should reference specialization."
    
    post_scale_nodes = await distributed_civilization.get_active_nodes()
    node_ids = [n.id for n in post_scale_nodes]
    assert scaled_id in node_ids, "Scaled node should be registered in mesh state topology."
    
    logger.info("✓ Distributed node registration & mesh scaling passed successfully.")

async def test_federated_raft_consensus_elections():
    logger.info("=== 2. Testing RAFT Consensus Governor Elections ===")
    
    # Register governors
    await distributed_civilization.register_governor("test_node_reasoning", "FOLLOWER")
    await distributed_civilization.register_governor("test_node_worldmodel", "FOLLOWER")
    
    govs = await distributed_civilization.get_governors()
    assert len(govs) >= 2, "Should have registered governors."
    
    # Run election
    await distributed_civilization.run_governor_election()
    
    updated_govs = await distributed_civilization.get_governors()
    leaders = [g for g in updated_govs if g.raft_role == "LEADER"]
    assert len(leaders) == 1, "There must be exactly one elected leader node under RAFT protocol."
    assert updated_govs[0].current_term > 1, "RAFT election term must increment."
    
    logger.info(f"✓ RAFT leader election successful. Leader: {leaders[0].id}, Term: {leaders[0].current_term}")

async def test_memory_sharding_and_replication():
    logger.info("=== 3. Testing Distributed Memory Sharding & Compression ===")
    
    content = "A highly sensitive kingdom strategic doctrine regarding evolutionary tool versioning safety measures."
    shard = await distributed_civilization.create_memory_shard(
        shard_type="DOCTRINE", 
        host_node_id="test_node_reasoning", 
        content=content
    )
    
    assert shard.shard_type == "DOCTRINE", "Shard type must match."
    assert shard.host_node_id == "test_node_reasoning", "Host node binding must match."
    assert shard.original_size_bytes == len(content), "Original size must be stored."
    assert shard.compressed_size_bytes < shard.original_size_bytes, "Memory compression should yield byte size savings."
    assert shard.status == "HEALTHY", "New shards should initialize as HEALTHY."
    
    # Test replication
    await distributed_civilization.replicate_shard_state(shard.id, "test_node_worldmodel")
    
    shards = await distributed_civilization.get_memory_shards()
    tgt_shard = next((s for s in shards if s.id == shard.id), None)
    assert tgt_shard is not None, "Shard must be persisted."
    assert tgt_shard.status == "HEALTHY", "Replicated shard status should resolve to healthy."
    
    logger.info("✓ Distributed memory sharding & compressed savings validated.")

async def test_latency_aware_cognitive_routing():
    logger.info("=== 4. Testing Latency-Aware Cognitive Routing ===")
    
    # Execute distributed routing simulator
    planning_result = await distributed_civilization.execute_cross_node_planning(
        "Simulate full evolutionary tool deployment branch and audit alignment drift"
    )
    
    assert "status" in planning_result, "Cross-node planning should return status."
    assert planning_result["status"] == "SYNCHRONIZED", "Planning should succeed across active nodes."
    assert planning_result["synchronized_nodes_count"] > 0, "Should utilize registered nodes."
    
    logger.info("✓ Latency-aware cross-node cognitive router verified.")

async def test_nervous_reflexes_logging():
    logger.info("=== 5. Testing Swarm Nervous Reflex Logging ===")
    
    initial_length = len(distributed_civilization.active_reflexes)
    
    # Trigger dynamic reflex
    await distributed_civilization.trigger_nervous_reflex(
        "COGNITIVE_HEARTBEAT",
        "Global synchronization heartbeat tick verified across planetary nodes.",
        "INFO"
    )
    
    assert len(distributed_civilization.active_reflexes) > initial_length, "Reflex should be added to live console."
    latest_reflex = distributed_civilization.active_reflexes[0]
    assert latest_reflex["event"] == "COGNITIVE_HEARTBEAT", "Reflex type must match."
    assert latest_reflex["priority"] == "INFO", "Reflex priority must match."
    
    logger.info("✓ Swarm nervous system reflex logging validated.")

async def test_failure_containment_and_self_healing():
    logger.info("=== 6. Testing Failure Containment Isolation & Self-Healing ===")
    
    # Add a node that will fail
    node_to_fail = "node_doomed_to_fail"
    await distributed_civilization.register_node(node_to_fail, "TRUST_GOVERNANCE")
    await distributed_civilization.register_governor(node_to_fail, "FOLLOWER")
    
    # Put a shard on the failing node
    failed_shard = await distributed_civilization.create_memory_shard(
        shard_type="TRUST",
        host_node_id=node_to_fail,
        content="Sensitive trust evaluation ledger matching HouseWeights"
    )
    
    # Publish NODE_ANOMALY failure event on event bus
    event = Event(
        event_type="NODE_ANOMALY",
        sender="TestRunner",
        payload={"node_id": node_to_fail, "reason": "Loss of synchronization pulse due to compute starvation"}
    )
    
    # Trigger recovery loop by dispatching event to event bus listener
    await distributed_civilization.handle_node_anomaly(event)
    
    # Verify node status is isolated/quarantined as FAILED
    active_nodes = await distributed_civilization.get_active_nodes()
    failed_node = next((n for n in active_nodes if n.id == node_to_fail), None)
    assert failed_node is not None, "Node should still exist in database."
    assert failed_node.status == "FAILED", "Failed node must be isolated to FAILED status."
    assert failed_node.latency_ms >= 999.0, "Failed node latency must be flagged to max fail threshold."
    
    # Verify memory shards are rebalanced/redistributed onto healthy hosts
    shards = await distributed_civilization.get_memory_shards()
    restored_shard = next((s for s in shards if s.id == failed_shard.id), None)
    assert restored_shard is not None, "Shard must survive."
    assert restored_shard.host_node_id != node_to_fail, "Workload memory shard must be evacuated from failed host node."
    assert restored_shard.status == "REPLICATING", "Evacuated shard should temporarily enter REPLICATING state."
    
    # Verify governor state is updated
    govs = await distributed_civilization.get_governors()
    failed_gov = next((g for g in govs if g.id == node_to_fail), None)
    assert failed_gov is not None
    assert failed_gov.status == "QUARANTINED", "Failed governor should be isolated/quarantined."
    assert failed_gov.raft_role == "FOLLOWER", "Failed leader/follower governor role must yield to healthy nodes."
    
    logger.info("✓ Failure isolation containment & self-healing rebalancing loops passed successfully!")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 7: DISTRIBUTED CIVILIZATION TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize SQLite fallback memory database for isolated execution
        await init_db()
        
        await test_node_registration_and_scaling()
        await test_federated_raft_consensus_elections()
        await test_memory_sharding_and_replication()
        await test_latency_aware_cognitive_routing()
        await test_nervous_reflexes_logging()
        await test_failure_containment_and_self_healing()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL PHASE 7 DISTRIBUTED CIVILIZATION TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
