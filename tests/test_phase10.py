import asyncio
import os
import uuid
import sys
from app.models import schemas
from app.services.execution_sandbox import execution_pipeline, knowledge_engine, experiment_runner
from app.services.validation_benchmark import benchmark_engine, enforcement_engine, scientific_validator
from app.services.synthesis_engine import synthesis_engine, artifact_system
from sqlalchemy.future import select

# Configure logging for standard output
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("antigravity.test_phase10")

async def test_phase10_execution():
    logger.info("=== 1. Testing Database Table Initialization ===")
    await schemas.init_db()

    async with schemas.async_session() as session:
        # 1. Verify SQLTask assigned_soldier bug is fixed
        test_task = schemas.SQLTask(
            id=f"test_task_{uuid.uuid4().hex[:8]}",
            parent_objective="test",
            title="test bug",
            assigned_house="test_house",
            assigned_soldier="test_soldier_001"
        )
        session.add(test_task)
        await session.commit()
        
        result = await session.execute(select(schemas.SQLTask).where(schemas.SQLTask.id == test_task.id))
        fetched_task = result.scalar_one_or_none()
        assert fetched_task is not None
        assert fetched_task.assigned_soldier == "test_soldier_001"
        logger.info("✓ SQLTask assigned_soldier Phase 9 bug confirmed repaired.")

    logger.info("=== 2. Testing Real Execution Sandbox ===")
    
    # 2. Test Sandbox Code Execution
    code_to_run = "print('Hello Real Execution')"
    trace = await execution_pipeline.run_task_code("task_exec_123", code_to_run)
    assert trace.exit_code == 0
    assert "Hello Real Execution" in trace.stdout_log
    assert trace.status == "SUCCESS"
    logger.info("✓ Real Python Sandbox Execution successful. Output verified.")
    
    # 3. Test Sandbox Failure Tracking
    bad_code = "print(1/0)"
    trace_bad = await execution_pipeline.run_task_code("task_exec_bad", bad_code)
    assert trace_bad.exit_code != 0
    assert "ZeroDivisionError" in trace_bad.stderr_log
    assert trace_bad.status == "FAILED"
    logger.info("✓ Real Python Sandbox error handling & stderr tracking verified.")

    logger.info("=== 3. Testing Real Capability Benchmarking ===")
    
    # 4. Test Benchmark Engine
    benchmark_script = "assert 2 + 2 == 4\nprint('Benchmark Passed')"
    score = await benchmark_engine.run_benchmark("target_skill_42", "Mathematics", benchmark_script)
    assert score.score == 1.0
    assert score.verified == 1
    assert "Benchmark Passed" in score.validation_evidence
    logger.info("✓ Benchmark Engine evaluated live capability script accurately.")

    logger.info("=== 4. Testing Non-Simulation Enforcement Engine ===")
    
    # 5. Auditing Fake Traces
    fake_trace = schemas.ExecutionTraceSchema(id="fake", task_id="fake", execution_time_ms=0.0, exit_code=0)
    assert not enforcement_engine.audit_trace(fake_trace)
    
    valid_output = {"data": "real"}
    fake_output = {"data": "simulated learning completed"}
    stripped = enforcement_engine.enforce_grounding(fake_output)
    assert "error" in stripped
    logger.info("✓ Non-Simulation Enforcement effectively quarantined mock/fake execution telemetry.")

    logger.info("=== 5. Testing Final Artifact Generation & Synthesis ===")
    
    # 6. Test Real Artifact Saving
    artifact = await artifact_system.save_artifact("obj_123", "print('hello')", "test_script.py")
    assert os.path.exists(artifact.file_path)
    assert artifact.file_size_bytes > 0
    logger.info("✓ Artifact Generation successfully dumped real code to filesystem.")

    # 7. Test Response Synthesis
    debates = [{"round": 1, "argument": "Proceed with real execution."}]
    final_response = synthesis_engine.synthesize_response("obj_123", debates, trace, score)
    assert final_response["confidence_percent"] == 100
    assert final_response["execution_status"] == "SUCCESS"
    assert "Hello Real Execution" in final_response["execution_logs"]["stdout"]
    logger.info("✓ Final Response Synthesis perfectly merged live traces, benchmarks, and outputs.")

    logger.info("==========================================================")
    logger.info("🎉 SUCCESS: ALL PHASE 10 REAL EXECUTION CAPABILITY TESTS PASSED! 🎉")
    logger.info("==========================================================")


if __name__ == "__main__":
    asyncio.run(test_phase10_execution())
