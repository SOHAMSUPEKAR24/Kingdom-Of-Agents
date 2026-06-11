import logging
import os
from app.models.schemas import ExecutionTraceSchema

logger = logging.getLogger("antigravity.reality_engine")

class ExecutionRealityEngine:
    def __init__(self):
        pass

    def verify_trace_reality(self, trace: ExecutionTraceSchema, expected_file_outputs: list[str] = None) -> bool:
        """
        Enforces Phase 11 Reality Checks.
        A trace is ONLY real if:
        1. exit_code is 0 (or specifically intended if testing failures).
        2. stdout or stderr is not entirely empty (something actually ran).
        3. If it claims to have generated a file, the file must exist on the local disk.
        """
        logger.info(f"🔎 [REALITY ENGINE] Verifying execution trace '{trace.id}' for task '{trace.task_id}'...")

        if trace.status == "TIMEOUT":
            logger.warning(f"⚠️ [REALITY ENGINE] Trace {trace.id} timed out. Failed reality check.")
            return False

        if trace.exit_code != 0:
            logger.warning(f"⚠️ [REALITY ENGINE] Trace {trace.id} returned non-zero exit code {trace.exit_code}. Failed reality check.")
            return False

        if not trace.stdout_log and not trace.stderr_log:
            logger.error(f"🚨 [REALITY ENGINE] Trace {trace.id} has NO output logs! Hallucinated or mocked execution detected.")
            return False

        if expected_file_outputs:
            for file_path in expected_file_outputs:
                if not os.path.exists(file_path):
                    logger.error(f"🚨 [REALITY ENGINE] Trace {trace.id} claimed to produce '{file_path}' but file is missing from disk! Hallucination detected.")
                    return False

        logger.info(f"✅ [REALITY ENGINE] Trace {trace.id} passed strict reality verification. Execution is genuine.")
        return True

execution_reality_engine = ExecutionRealityEngine()
