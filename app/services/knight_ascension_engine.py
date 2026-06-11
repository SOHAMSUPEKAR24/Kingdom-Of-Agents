import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLAscensionMetric, SQLExperienceVector
import uuid
import datetime

logger = logging.getLogger(__name__)

class KnightAscensionEngine:
    """
    The ultimate synthesis loop for Knight-0. 
    Aggregates data from all engines and evolves Knight-0's orchestration capability.
    """

    async def run_ascension_cycle(self, session: AsyncSession) -> SQLAscensionMetric:
        """
        Evaluates recent civilization success and bumps Knight-0's ascension metrics.
        """
        time_threshold = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        
        # Look at recent experience vectors
        result = await session.execute(
            select(SQLExperienceVector)
            .where(SQLExperienceVector.created_at >= time_threshold)
        )
        recent_exps = result.scalars().all()
        
        success_rate = 1.0
        if recent_exps:
            success_rate = sum(e.success_rating for e in recent_exps) / len(recent_exps)
            
        # Get previous metric to increment
        prev_result = await session.execute(
            select(SQLAscensionMetric)
            .order_by(SQLAscensionMetric.recorded_at.desc())
            .limit(1)
        )
        prev = prev_result.scalar_one_or_none()
        
        base_depth = prev.reasoning_depth if prev else 1.0
        
        # Evolve based on success
        new_depth = base_depth + (0.01 if success_rate > 0.8 else -0.005)
        
        metric = SQLAscensionMetric(
            id=f"asc_{uuid.uuid4().hex[:8]}",
            knight_id="Knight-0",
            reasoning_depth=new_depth,
            world_model_accuracy=success_rate,
            strategic_foresight=new_depth * 1.1
        )
        
        session.add(metric)
        
        # Part 9: Modify physical hyperparameters
        from app.models.schemas import SQLCivilizationState
        state_result = await session.execute(select(SQLCivilizationState).limit(1))
        civ_state = state_result.scalars().first()
        if civ_state:
            civ_state.total_compute_budget += (100.0 if success_rate > 0.8 else 10.0)
            civ_state.synchronicity_index = new_depth
            logger.info(f"👑 [ASCENSION] Mutated Civilization State: Budget={civ_state.total_compute_budget}, Sync={civ_state.synchronicity_index}")
        
        await session.flush()
        
        logger.info(f"👑 [ASCENSION] Knight-0 Ascension Cycle Complete. Reasoning Depth: {new_depth:.3f}")
        return metric

knight_ascension_engine = KnightAscensionEngine()
