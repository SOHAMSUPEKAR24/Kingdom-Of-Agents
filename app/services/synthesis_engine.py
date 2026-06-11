import uuid
import os
import json
import logging
from typing import Dict, Any, List
from app.models import schemas
from datetime import datetime

logger = logging.getLogger(__name__)

ARTIFACTS_DIR = os.path.join(os.getcwd(), "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

class FinalResponseSynthesisEngine:
    """Merges all outputs, benchmarks, traces, and debates into a clean final response."""
    
    def synthesize_response(self, objective_id: str, debates: List[Dict[str, Any]], trace: schemas.ExecutionTraceSchema, benchmark: schemas.BenchmarkScoreSchema) -> Dict[str, Any]:
        logger.info(f"🧠 [SYNTHESIS ENGINE] Synthesizing final response for Objective: {objective_id}")
        
        confidence = 100 if trace.exit_code == 0 else max(0, 100 - (100 * (1.0 - (benchmark.score if benchmark else 0.0))))
        
        response = {
            "objective_id": objective_id,
            "final_answer": "Execution completed successfully." if trace.exit_code == 0 else "Execution failed during runtime.",
            "execution_status": trace.status,
            "confidence_percent": confidence,
            "debate_summary": " | ".join([f"Round {d.get('round')}: {d.get('argument')}" for d in debates]),
            "execution_logs": {
                "stdout": trace.stdout_log,
                "stderr": trace.stderr_log,
                "exit_code": trace.exit_code,
                "duration_ms": trace.execution_time_ms
            },
            "benchmark_score": benchmark.score if benchmark else 0.0,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"✅ [SYNTHESIS ENGINE] Final synthesis complete. Confidence: {confidence}%")
        return response


class ArtifactGenerationSystem:
    """Saves real output generated files to the filesystem to ground execution capabilities."""
    
    async def save_artifact(self, objective_id: str, content: str, filename: str, artifact_type: str = "CODE") -> schemas.GeneratedArtifactSchema:
        logger.info(f"💾 [ARTIFACT SYSTEM] Saving artifact {filename} for {objective_id}...")
        file_path = os.path.join(ARTIFACTS_DIR, filename)
        
        with open(file_path, "w") as f:
            f.write(content)
            
        file_size = os.path.getsize(file_path)
        
        artifact = schemas.GeneratedArtifactSchema(
            id=f"art_{uuid.uuid4().hex[:8]}",
            objective_id=objective_id,
            file_path=file_path,
            artifact_type=artifact_type,
            file_size_bytes=file_size
        )
        
        async for session in schemas.get_db_session():
            db_art = schemas.SQLGeneratedArtifact(**artifact.model_dump())
            session.add(db_art)
            await session.commit()
            
        logger.info(f"✅ [ARTIFACT SYSTEM] Artifact saved: {file_path} ({file_size} bytes)")
        return artifact


class RealMemoryDistillationEngine:
    """Distills actual execution traces instead of simulated abstraction."""
    
    def distill_trace(self, trace: schemas.ExecutionTraceSchema) -> str:
        logger.info(f"📝 [MEMORY DISTILLATION] Distilling real execution trace {trace.id}")
        if trace.exit_code == 0:
            return f"Successful execution yielding {len(str(trace.stdout_log))} bytes of output in {trace.execution_time_ms}ms."
        else:
            error_preview = trace.stderr_log[:100] if trace.stderr_log else "Unknown error"
            return f"Failed execution with exit {trace.exit_code}. Error: {error_preview}"


# Global Singletons
synthesis_engine = FinalResponseSynthesisEngine()
artifact_system = ArtifactGenerationSystem()
memory_distillation = RealMemoryDistillationEngine()
