from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import get_db_session, SQLPersistentAgent
import logging

logger = logging.getLogger(__name__)

class LongLivedMindEngine:
    """
    Manages the long-term cognitive development of agents.
    Agents accumulate expertise, level up, and evolve execution tendencies.
    """
    
    @staticmethod
    async def accumulate_experience(agent_id: str, points: float, session: AsyncSession = None) -> bool:
        """Adds experience points and levels up the agent if thresholds are met."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            agent = await db.get(SQLPersistentAgent, agent_id)
            if not agent:
                logger.error(f"Cannot accumulate experience: Agent {agent_id} not found.")
                return False
                
            agent.experience_points += points
            
            # Simple level-up threshold: 100 points per level
            new_level = int(agent.experience_points // 100) + 1
            if new_level > agent.current_level:
                logger.info(f"Agent {agent_id} ({agent.name}) Leveled Up to {new_level}!")
                agent.current_level = new_level
                
            if not session:
                await db.commit()
            return True
        finally:
            if not session:
                await async_gen.aclose()
                
    @staticmethod
    async def develop_specialization(agent_id: str, domain: str, session: AsyncSession = None) -> bool:
        """Deepens specialization for an agent, shaping its Long-Lived Mind."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            stmt = update(SQLPersistentAgent).where(SQLPersistentAgent.id == agent_id).values(
                specialization=domain
            )
            result = await db.execute(stmt)
            if not session:
                await db.commit()
            return result.rowcount > 0
        finally:
            if not session:
                await async_gen.aclose()

long_lived_mind = LongLivedMindEngine()
