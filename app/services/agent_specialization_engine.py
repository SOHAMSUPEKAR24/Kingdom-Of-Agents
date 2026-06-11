import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import get_db_session, SQLPersistentAgent
import logging

logger = logging.getLogger(__name__)

class AgentSpecializationEngine:
    """
    Evolves expertise profiles based on benchmark successes, reducing weak-domain
    assignments and turning generalist soldiers into domain specialists.
    """
    
    @staticmethod
    async def process_benchmark_result(agent_id: str, domain: str, success: bool, session: AsyncSession = None) -> bool:
        """Adjusts the specialization vector for an agent post-benchmark."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            agent = await db.get(SQLPersistentAgent, agent_id)
            if not agent:
                return False
                
            # If successful, lock in the specialization
            if success and agent.specialization != domain:
                logger.info(f"Agent {agent.name} is specializing deeper into {domain}.")
                agent.specialization = domain
                
            if not session:
                await db.commit()
            return True
        finally:
            if not session:
                await async_gen.aclose()

specialization_engine = AgentSpecializationEngine()
