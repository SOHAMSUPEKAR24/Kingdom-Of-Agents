import logging
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.schemas import SQLLongHorizonObjective, SQLCivilizationState
import uuid

logger = logging.getLogger(__name__)

class ContinuityMemoryEngine:
    """
    Synthesizes months of history into summarized strategic blocks.
    Keeps Knight-0 aware of its entire evolution timeline.
    """

    async def summarize_civilization_epoch(self, months_back: int, session: AsyncSession) -> dict:
        """
        Creates a high-level summary of the civilization's growth over a specific period.
        """
        threshold = datetime.datetime.utcnow() - datetime.timedelta(days=30 * months_back)
        
        # Count objectives completed
        result = await session.execute(
            select(func.count(SQLLongHorizonObjective.id))
            .where(SQLLongHorizonObjective.created_at >= threshold)
            .where(SQLLongHorizonObjective.status == "COMPLETED")
        )
        completed = result.scalar() or 0
        
        # Get active state
        state_res = await session.execute(select(SQLCivilizationState).limit(1))
        state = state_res.scalar_one_or_none()
        
        budget_spent = state.spent_compute_budget if state else 0.0
        
        summary = {
            "epoch_months": months_back,
            "objectives_completed": completed,
            "compute_consumed": budget_spent,
            "evolution_status": "ASCENDING" if completed > 0 else "STAGNANT"
        }
        
        logger.info(f"⏳ [MEMORY CONTINUITY] Summarized epoch (-{months_back} months). Status: {summary['evolution_status']}")
        return summary

continuity_memory_engine = ContinuityMemoryEngine()
