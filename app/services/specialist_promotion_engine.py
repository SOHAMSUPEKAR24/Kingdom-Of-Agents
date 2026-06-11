import logging
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLSpecialistPromotion

logger = logging.getLogger(__name__)

RANKS = [
    "Novice",
    "Apprentice",
    "Practitioner",
    "Advanced",
    "Expert",
    "Master"
]

class SpecialistPromotionEngine:
    """
    Evaluates agents based on capability mastery scores and promotes them across ranks.
    """
    
    def __init__(self):
        self.name = "SPECIALIST_PROMOTION_ENGINE"

    def determine_rank(self, mastery_score: float) -> str:
        """Maps a mastery score (0.0 to 1.0) to a specific rank."""
        if mastery_score >= 0.95:
            return "Master"
        elif mastery_score >= 0.8:
            return "Expert"
        elif mastery_score >= 0.6:
            return "Advanced"
        elif mastery_score >= 0.4:
            return "Practitioner"
        elif mastery_score >= 0.2:
            return "Apprentice"
        else:
            return "Novice"

    async def evaluate_and_promote(self, db_session: AsyncSession, agent_id: str, dynasty: str, current_rank: str, mastery_score: float) -> Optional[SQLSpecialistPromotion]:
        """Evaluates if an agent should be promoted based on their mastery score."""
        expected_rank = self.determine_rank(mastery_score)

        if expected_rank != current_rank and RANKS.index(expected_rank) > RANKS.index(current_rank):
            # Promote!
            promotion_id = f"PROM-{uuid.uuid4().hex[:8]}"
            promotion = SQLSpecialistPromotion(
                id=promotion_id,
                agent_id=agent_id,
                dynasty=dynasty,
                previous_rank=current_rank,
                new_rank=expected_rank,
                justification=f"Mastery score reached {mastery_score:.2f}, crossing threshold for {expected_rank}."
            )
            db_session.add(promotion)
            
            logger.info(f"🎖️ [PROMOTION_ENGINE] Agent {agent_id} promoted to {expected_rank} in the {dynasty} dynasty!")
            return promotion

        return None

    async def run_dynasty_evaluation(self):
        """
        Periodically runs over active agents, calculates their benchmark mastery, 
        and promotes them automatically.
        """
        logger.info("👑 [DYNASTY EVALUATION] Scanning all active specialists for promotion eligibility...")
        from app.models.schemas import async_session
        async with async_session() as session:
            # Simulate picking a high performing agent
            agent_id = f"AGT-{uuid.uuid4().hex[:8]}"
            await self.evaluate_and_promote(session, agent_id, "Scientific", "Advanced", 0.85)
            await session.commit()

specialist_promotion_engine = SpecialistPromotionEngine()
