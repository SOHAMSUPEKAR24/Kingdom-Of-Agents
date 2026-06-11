import uuid
import logging
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLSpecialistDynasty

logger = logging.getLogger(__name__)

class SpecialistDynastyEngine:
    """
    Manages persistent specialist lineages (e.g., Browser Dynasty, Software Engineering Dynasty)
    across restarts and aggregates capability metrics for the dynasty.
    """

    def __init__(self):
        self.name = "SPECIALIST_DYNASTY_ENGINE"
        self.version = "1.0.0"

    async def ensure_dynasty_exists(self, db_session: AsyncSession, dynasty_name: str, domain: str = "General") -> SQLSpecialistDynasty:
        """Ensures a dynasty exists, creating it if necessary."""
        query = select(SQLSpecialistDynasty).where(SQLSpecialistDynasty.dynasty_name == dynasty_name)
        result = await db_session.execute(query)
        dynasty = result.scalars().first()

        if not dynasty:
            dynasty_id = f"DYN-{uuid.uuid4().hex[:8]}"
            dynasty = SQLSpecialistDynasty(
                id=dynasty_id,
                dynasty_name=dynasty_name,
                domain=domain,
                total_mastery_level=1.0,
                member_count=0
            )
            db_session.add(dynasty)
            logger.info(f"👑 [DYNASTY_ENGINE] Created new persistent dynasty: {dynasty_name}")

        return dynasty

    async def register_agent_to_dynasty(self, db_session: AsyncSession, agent_id: str, dynasty_name: str) -> SQLSpecialistDynasty:
        """Registers a new agent to a dynasty and increments the member count."""
        dynasty = await self.ensure_dynasty_exists(db_session, dynasty_name)
        dynasty.member_count += 1
        logger.info(f"🛡️ [DYNASTY_ENGINE] Agent {agent_id} joined the {dynasty_name}. Members: {dynasty.member_count}")
        return dynasty

    async def update_dynasty_mastery(self, db_session: AsyncSession, dynasty_name: str, mastery_delta: float) -> Optional[SQLSpecialistDynasty]:
        """Updates the total mastery level of a dynasty based on its members' progress."""
        query = select(SQLSpecialistDynasty).where(SQLSpecialistDynasty.dynasty_name == dynasty_name)
        result = await db_session.execute(query)
        dynasty = result.scalars().first()

        if dynasty:
            dynasty.total_mastery_level += mastery_delta
            logger.info(f"📈 [DYNASTY_ENGINE] {dynasty_name} mastery increased by {mastery_delta:.2f}. Total: {dynasty.total_mastery_level:.2f}")
        return dynasty

    async def get_all_dynasties(self, db_session: AsyncSession) -> List[SQLSpecialistDynasty]:
        """Retrieves all active specialist dynasties."""
        query = select(SQLSpecialistDynasty)
        result = await db_session.execute(query)
        return list(result.scalars().all())

specialist_dynasty_engine = SpecialistDynastyEngine()
