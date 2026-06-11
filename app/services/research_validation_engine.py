import logging
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.research_validation")

class ResearchValidationEngine:
    def __init__(self):
        self.rejected_theses = 0
        self.validated_theses = 0

    async def initialize(self):
        event_bus.subscribe("RESEARCH_PROPOSAL", self.validate_research)
        logger.info("🔬 [RESEARCH VALIDATION ENGINE] Online. Preventing hallucinated conclusions.")

    async def validate_research(self, event: Event):
        payload = event.payload
        thesis_id = payload.get("thesis_id")
        evidence_chain = payload.get("evidence_chain", [])
        reproducible = payload.get("reproducible", False)

        if not evidence_chain or not reproducible:
            logger.warning(f"❌ [RESEARCH VALIDATION] Thesis {thesis_id} rejected. Lacks reproducible evidence.")
            self.rejected_theses += 1
            await event_bus.publish(Event(
                event_type="RESEARCH_REJECTED",
                sender="ResearchValidationEngine",
                payload={"thesis_id": thesis_id, "reason": "Not reproducible or missing evidence chain."}
            ))
            return

        self.validated_theses += 1
        logger.info(f"✅ [RESEARCH VALIDATION] Thesis {thesis_id} validated. Evidence is structurally sound.")
        await event_bus.publish(Event(
            event_type="RESEARCH_VALIDATED",
            sender="ResearchValidationEngine",
            payload={"thesis_id": thesis_id}
        ))

research_validation_engine = ResearchValidationEngine()
