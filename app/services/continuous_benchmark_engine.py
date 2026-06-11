import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import SQLRealBenchmarkResult
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

class ContinuousBenchmarkEngine:
    """
    Dynamically scales benchmark difficulty over generations to prevent capability plateauing.
    """

    async def evaluate_plateau(self, environment: str, session: AsyncSession) -> bool:
        """
        Determines if the civilization has plateaued on a specific benchmark environment.
        """
        result = await session.execute(
            select(SQLRealBenchmarkResult)
            .where(SQLRealBenchmarkResult.environment == environment)
            .order_by(SQLRealBenchmarkResult.created_at.desc())
            .limit(5)
        )
        recent_scores = [b.score for b in result.scalars().all()]
        
        if len(recent_scores) == 5 and all(s >= 0.95 for s in recent_scores):
            logger.info(f"📈 [BENCHMARK ENGINE] Plateau detected on {environment}. Increasing difficulty tier.")
            return True
            
        return False

continuous_benchmark_engine = ContinuousBenchmarkEngine()
