import logging
import uuid
from datetime import datetime
from sqlalchemy import select

from app.core.event_bus import event_bus, Event
from app.models.schemas import async_session, SQLSkillScore

logger = logging.getLogger("antigravity.skill_scoring")

class SkillScoringSystem:
    def __init__(self):
        pass

    async def initialize(self):
        event_bus.subscribe("BENCHMARK_COMPLETED", self.update_skill_score)
        logger.info("📈 [SKILL SCORING SYSTEM] Online. Tracking proficiency evolution.")

    async def update_skill_score(self, event: Event):
        payload = event.payload
        domain = payload.get("domain")
        score = payload.get("score_percentage")
        run_id = payload.get("run_id")

        if not domain or score is None:
            return

        async with async_session() as session:
            res = await session.execute(select(SQLSkillScore).where(SQLSkillScore.skill_domain == domain))
            record = res.scalars().first()

            if not record:
                record = SQLSkillScore(
                    id=str(uuid.uuid4()),
                    skill_domain=domain,
                    proficiency_score=score,
                    total_practice_hours=0.0,
                    benchmark_history=[run_id],
                    updated_at=datetime.utcnow()
                )
                session.add(record)
            else:
                # Evolve the proficiency score (e.g. weighted average)
                record.proficiency_score = (record.proficiency_score * 0.7) + (score * 0.3)
                
                # Make sure to handle lists safely in JSON columns
                history = list(record.benchmark_history) if record.benchmark_history else []
                history.append(run_id)
                record.benchmark_history = history
                record.updated_at = datetime.utcnow()

            await session.commit()
            logger.info(f"📈 [SKILL SCORING] Domain '{domain}' proficiency updated to {record.proficiency_score:.1f}/100")

            # Trigger practice if score drops
            if score < 90.0:
                await event_bus.publish(Event(
                    event_type="WEAKNESS_DETECTED",
                    sender="SkillScoringSystem",
                    payload={"domain": domain, "score": score, "failed_cases": payload.get("failed_cases", [])}
                ))

skill_scoring_system = SkillScoringSystem()
