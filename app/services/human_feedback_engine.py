import logging
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.human_feedback")

class HumanFeedbackEngine:
    def __init__(self):
        self.feedback_processed = 0

    async def initialize(self):
        event_bus.subscribe("HUMAN_FEEDBACK_SUBMITTED", self.process_feedback)
        logger.info("👑 [HUMAN FEEDBACK ENGINE] Online. Awaiting corrections and overrides from the King.")

    async def process_feedback(self, event: Event):
        payload = event.payload
        feedback_type = payload.get("type", "CORRECTION")
        content = payload.get("content", "")
        
        logger.warning(f"👑 [HUMAN FEEDBACK] Received manual {feedback_type}: {content}")
        
        # Human feedback acts as the ultimate ground truth, immediately mutating doctrines or skill trajectories
        self.feedback_processed += 1
        
        await event_bus.publish(Event(
            event_type="NEW_DOCTRINE_CREATED",
            sender="HumanFeedbackEngine",
            payload={"doctrine": f"KING'S OVERRIDE: {content}"}
        ))

human_feedback_engine = HumanFeedbackEngine()
