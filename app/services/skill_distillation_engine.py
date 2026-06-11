import logging
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.skill_distillation")

class SkillDistillationEngine:
    def __init__(self):
        self.doctrines_created = 0

    async def initialize(self):
        event_bus.subscribe("RCA_COMPLETED", self.distill_skill)
        logger.info("🧪 [SKILL DISTILLATION ENGINE] Online. Distilling experience into reusable expertise.")

    async def distill_skill(self, event: Event):
        payload = event.payload
        proposed_strategy = payload.get("proposed_strategy")

        if proposed_strategy:
            logger.info(f"🧪 [SKILL DISTILLATION] Distilling strategy into permanent doctrine: '{proposed_strategy}'")
            self.doctrines_created += 1

            # Store doctrine (could reuse SQLCivilizationDoctrine)
            await event_bus.publish(Event(
                event_type="NEW_DOCTRINE_CREATED",
                sender="SkillDistillationEngine",
                payload={"doctrine": proposed_strategy}
            ))

skill_distillation_engine = SkillDistillationEngine()
