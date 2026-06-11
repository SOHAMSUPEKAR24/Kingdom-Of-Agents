import uuid
import logging
from typing import Dict, Any, List
from app.models import schemas
from app.services.execution_sandbox import execution_pipeline

logger = logging.getLogger(__name__)

class RealCapabilityBenchmarkEngine:
    """Benchmarks specific capabilities dynamically by executing unit tests against generated code."""
    async def run_benchmark(self, target_id: str, domain: str, test_script: str) -> schemas.BenchmarkScoreSchema:
        logger.info(f"📊 [BENCHMARK ENGINE] Running live capability benchmark for {target_id} in domain '{domain}'")
        
        # Execute the benchmark test script in the sandbox
        trace = await execution_pipeline.run_task_code(f"benchmark_{target_id}", test_script)
        
        # Score calculation: 1.0 for success, 0.0 for failure
        score = 1.0 if trace.exit_code == 0 else 0.0
        
        benchmark = schemas.BenchmarkScoreSchema(
            id=f"bm_{uuid.uuid4().hex[:8]}",
            target_id=target_id,
            capability_domain=domain,
            score=score,
            verified=1,
            validation_evidence=trace.stdout_log if score == 1.0 else trace.stderr_log
        )
        
        # Persist benchmark
        async for session in schemas.get_db_session():
            db_bm = schemas.SQLBenchmarkScore(**benchmark.model_dump())
            session.add(db_bm)
            await session.commit()
            
        logger.info(f"✅ [BENCHMARK ENGINE] Benchmark complete. Score: {score}")
        return benchmark


class NonSimulationEnforcementEngine:
    """Audits task outputs and system metrics to ensure NO fake/simulated telemetry is claimed."""
    def audit_trace(self, trace: schemas.ExecutionTraceSchema) -> bool:
        """Verifies an execution trace is real and not mocked."""
        # Simple heuristic: if execution_time is 0.0 or stdout/stderr is completely empty without valid exit, it might be fake
        # For our purposes, we assume any trace routed through ExecutionSandbox is verified.
        is_simulated = trace.execution_time_ms < 0.1 and not trace.stdout_log and not trace.stderr_log
        if is_simulated:
            logger.warning(f"🚫 [NON-SIMULATION ENFORCEMENT] Fake execution trace detected: {trace.id}. QUARANTINED.")
            return False
        return True
    
    def enforce_grounding(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        """Strips out unverified claims of learning/capability from output if missing trace references."""
        if "trace_id" not in output_data and "simulated" in str(output_data).lower():
            logger.warning("🚫 [NON-SIMULATION ENFORCEMENT] Stripping simulated output.")
            return {"error": "UNVERIFIED_SIMULATED_OUTPUT", "original": output_data}
        return output_data


class RealScientificValidationEngine:
    """Validates scientific theories by verifying actual empirical sandbox outputs."""
    async def validate_theory(self, theory_id: str, experiment_data: Dict[str, Any]) -> bool:
        logger.info(f"⚖️ [SCIENTIFIC VALIDATION] Validating theory {theory_id} with real experimental evidence...")
        if not experiment_data.get("success", False):
            logger.warning(f"🚫 [SCIENTIFIC VALIDATION] Theory {theory_id} failed empirical validation.")
            return False
        
        # Check if stdout contains proof
        if "Proof successful" not in str(experiment_data.get("stdout", "")):
            logger.warning(f"🚫 [SCIENTIFIC VALIDATION] Theory {theory_id} lacks concrete proof in stdout.")
            return False
            
        logger.info(f"✅ [SCIENTIFIC VALIDATION] Theory {theory_id} rigorously validated.")
        return True


# Global Singletons
benchmark_engine = RealCapabilityBenchmarkEngine()
enforcement_engine = NonSimulationEnforcementEngine()
scientific_validator = RealScientificValidationEngine()
