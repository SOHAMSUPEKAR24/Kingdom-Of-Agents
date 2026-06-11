import logging
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.execution_quality")

class ExecutionQualityEngine:
    def __init__(self):
        self.execution_metrics_tracked = 0

    async def initialize(self):
        event_bus.subscribe("TASK_COMPLETED", self.evaluate_execution)
        logger.info("📈 [EXECUTION QUALITY ENGINE] Online. Tracking resource efficiency and execution stability.")

    async def evaluate_execution(self, event: Event):
        payload = event.payload
        task_data = payload.get("task", {})
        execution_time_ms = payload.get("execution_time_ms", 100.0)

        logger.debug(f"📈 [EXECUTION QUALITY] Task {task_data.get('id')} completed in {execution_time_ms}ms.")
        self.execution_metrics_tracked += 1
        
        # If execution takes too long, flag it for optimization
        if execution_time_ms > 5000.0:
            await event_bus.publish(Event(
                event_type="TOOLCHAIN_OPTIMIZATION_REQUEST",
                sender="ExecutionQualityEngine",
                payload={"tool_name": f"Workflow_{task_data.get('id')}", "success_rate": 50.0}
            ))

execution_quality_engine = ExecutionQualityEngine()
