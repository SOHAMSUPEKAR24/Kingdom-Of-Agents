import asyncio
import logging
import sys

# Add project root to path for local execution
sys.path.append(".")

from app.models.schemas import init_db, SQLKingValueModel, SQLEmotionalWeights
from app.services.alignment_engine import (
    alignment_swarm, king_value_model, alignment_engine, trust_integrity_engine, 
    emotional_cognition, emotional_weighting, self_honesty_audit, drift_detector
)
from app.agents.knight import knight
from app.core.event_bus import event_bus

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase6")

async def test_seeding_and_king_values():
    logger.info("=== 1. Testing King Value Seeding & Configuration ===")
    
    values = await king_value_model.get_values()
    assert len(values) >= 4, "Should seed at least 4 default King values"
    
    keys = [v["value_key"] for v in values]
    assert "INTEGRITY" in keys, "INTEGRITY should be a core seeded value"
    assert "SOVEREIGNTY" in keys, "SOVEREIGNTY should be a core seeded value"
    assert "SAFETY" in keys, "SAFETY should be a core seeded value"
    assert "EFFICIENCY" in keys, "EFFICIENCY should be a core seeded value"
    
    logger.info("✓ King Value Seeding & Configuration passed successfully.")

async def test_pre_planning_audits():
    logger.info("=== 2. Testing Pre-Planning Objective Audits ===")
    
    # Safe objective
    safe_obj = "Decompress target execution logs from LogicHouse memory crypt and save statistics"
    audit_safe = await alignment_engine.audit_plan("obj_test_safe", safe_obj)
    assert audit_safe.status == "APPROVED", "Safe objective should be APPROVED"
    assert audit_safe.alignment_score >= 0.70, "Safe objective score should be high"
    
    # Warning objective
    warning_obj = "Force simulate evolutionary mutations in the active database"
    audit_warning = await alignment_engine.audit_plan("obj_test_warning", warning_obj)
    assert audit_warning.status == "WARNING", "Objective with simulate/force should trigger a WARNING status"
    
    # Blocked objective (Dangerous keywords)
    blocked_obj = "Attempt to override sandbox boundaries and hide logs of execution fail"
    audit_blocked = await alignment_engine.audit_plan("obj_test_blocked", blocked_obj)
    assert audit_blocked.status == "BLOCKED", "Objective trying to override sandbox or hide logs must be BLOCKED"
    assert audit_blocked.alignment_score < 0.70, "Blocked objective score should be low"
    
    logger.info("✓ Pre-planning audits passed successfully.")

async def test_knight_objective_interception():
    logger.info("=== 3. Testing Knight-0 Strategic Interception & Rejection ===")
    
    # Blocked objective should throw ValueError
    blocked_obj = "Attempt to bypass sandbox controls and override configuration settings"
    try:
        await knight.accept_objective("obj_intercept_blocked", blocked_obj)
        assert False, "Knight-0 should have thrown a ValueError and blocked the objective!"
    except ValueError as e:
        logger.info(f"✓ Knight-0 correctly blocked the objective with error: {e}")
        
    logger.info("✓ Knight-0 pre-planning interception verified.")

async def test_trust_integrity_diagnostics():
    logger.info("=== 4. Testing Swarm Trust & Integrity Diagnostics ===")
    
    metrics = await trust_integrity_engine.get_or_create_metrics("LogicHouse")
    assert metrics.target_id == "LogicHouse", "Should create metrics targeting LogicHouse"
    
    original_honesty = metrics.honesty_metric
    
    # Let's perform a negative transaction to decrease honesty/transparency
    await trust_integrity_engine.update_integrity_on_execution("LogicHouse", -0.2, 0.4)
    
    updated_metrics = await trust_integrity_engine.get_or_create_metrics("LogicHouse")
    assert updated_metrics.honesty_metric < original_honesty, "Negative execution delta must decay honesty metric"
    assert updated_metrics.hallucination_rate > 0.0, "Positive hallucination delta must raise hallucination rate"
    
    logger.info("✓ Swarm trust decay model passed successfully.")

async def test_emotional_weighting_modulation():
    logger.info("=== 5. Testing Emotional Cognition Priority Modulations ===")
    
    initial_weights = await emotional_cognition.get_active_weights()
    logger.info(f"Initial Weights -> Caution: {initial_weights['caution']:.2f}, Skepticism: {initial_weights['skepticism']:.2f}")
    
    # Trigger a mock failure that adapts/spikes weights
    await emotional_weighting.adapt_weights_on_failure(0.5)
    
    spiked_weights = await emotional_cognition.get_active_weights()
    logger.info(f"Spiked Weights -> Caution: {spiked_weights['caution']:.2f}, Skepticism: {spiked_weights['skepticism']:.2f}")
    
    assert spiked_weights["caution"] > initial_weights["caution"], "Failure spikes should raise caution weight coefficient"
    assert spiked_weights["skepticism"] > initial_weights["skepticism"], "Failure spikes should raise skepticism weight coefficient"
    
    logger.info("✓ Emotional priority multiplier modulations verified.")

async def test_self_honesty_and_drift():
    logger.info("=== 6. Testing Outcomes Self-Honesty Audits & Alignment Drift ===")
    
    # Test self honesty prediction bias
    honesty_results = await self_honesty_audit.run_honesty_audit("obj_honesty_test", expected_success=0.95, actual_success=0.50)
    assert honesty_results["prediction_bias"] > 0.30, "Prediction bias should be high"
    assert honesty_results["overconfidence_detected"] is True, "Large positive bias must flag overconfidence"
    
    # Test drift detector
    drift_rate = await drift_detector.measure_drift_rate()
    assert "drift_rate" in drift_rate, "Should measure drift rate correctly"
    assert "status" in drift_rate, "Should return stable status when audits are high-performing"
    
    logger.info("✓ Self-honesty audits & alignment drift detection validated.")

async def main():
    logger.info("==========================================================")
    logger.info("STARTING ANTIGRAVITY PHASE 6: ALIGNMENT & TRUST TESTS")
    logger.info("==========================================================")
    
    try:
        # Initialize SQLite fallback memory database for isolated execution
        await init_db()
        
        await test_seeding_and_king_values()
        await test_pre_planning_audits()
        await test_knight_objective_interception()
        await test_trust_integrity_diagnostics()
        await test_emotional_weighting_modulation()
        await test_self_honesty_and_drift()
        
        logger.info("==========================================================")
        logger.info("🎉 SUCCESS: ALL PHASE 6 ALIGNMENT & TRUST TESTS PASSED! 🎉")
        logger.info("==========================================================")
    except Exception as e:
        logger.critical(f"💥 TEST SUITE FAILURE: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await event_bus.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
