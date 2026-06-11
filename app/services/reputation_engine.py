from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import get_db_session, SQLPersistentAgent
import logging

logger = logging.getLogger(__name__)

class ReputationEngine:
    """
    Tracks agent reliability, hallucination rates, and benchmark consistency.
    Allows the civilization to know which agents are trustworthy over time.
    """
    
    @staticmethod
    async def update_reputation(agent_id: str, success: bool, hallucinated: bool = False, session: AsyncSession = None) -> bool:
        """Adjusts the reliability and hallucination rates for an agent."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            agent = await db.get(SQLPersistentAgent, agent_id)
            if not agent:
                return False
                
            # Naive EWMA for reliability: 0.9 * old + 0.1 * new
            current_rel = agent.reliability_score
            new_rel = current_rel * 0.9 + (1.0 if success else 0.0) * 0.1
            agent.reliability_score = new_rel
            
            # Naive EWMA for hallucination
            current_hal = agent.hallucination_rate
            new_hal = current_hal * 0.9 + (1.0 if hallucinated else 0.0) * 0.1
            agent.hallucination_rate = new_hal
            
            logger.info(f"Updated reputation for {agent.name}: Reliability={new_rel:.2f}, Hallucination={new_hal:.2f}")
            
            if not session:
                await db.commit()
            return True
        finally:
            if not session:
                await async_gen.aclose()

reputation_engine = ReputationEngine()
