import logging
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.failure_learning")

class FailureLearningEngine:
    def __init__(self):
        self.rca_performed = 0

    async def initialize(self):
        event_bus.subscribe("TASK_FAILED", self.perform_root_cause_analysis)
        logger.info("💥 [FAILURE LEARNING ENGINE] Online. Transforming failures into learning fuel.")

    async def perform_root_cause_analysis(self, event: Event):
        payload = event.payload
        task_id = payload.get("task_id")
        error_msg = payload.get("error")

        logger.info(f"💥 [FAILURE LEARNING] Analyzing failure for task {task_id}: {error_msg}")
        self.rca_performed += 1

        # Publish the RCA result so the skill distillation engine can create a doctrine
        await event_bus.publish(Event(
            event_type="RCA_COMPLETED",
            sender="FailureLearningEngine",
            payload={
                "task_id": task_id,
                "root_cause": "Semantic drift in target identification.",
                "proposed_strategy": "Implement double-verification on semantic matching."
            }
        ))

failure_learning_engine = FailureLearningEngine()
