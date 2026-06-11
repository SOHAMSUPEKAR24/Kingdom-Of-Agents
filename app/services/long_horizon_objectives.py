import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.schemas import get_db_session, SQLLongHorizonObjective, LongHorizonObjectiveSchema
import logging

logger = logging.getLogger(__name__)

class LongHorizonTracker:
    """
    Manages objectives that span days or weeks.
    Tracks milestones and prevents loss of strategic goals.
    """
    
    @staticmethod
    async def create_objective(title: str, description: str, milestones: List[Dict[str, Any]], house: str, session: AsyncSession = None) -> LongHorizonObjectiveSchema:
        """Creates a long-horizon strategic objective."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            obj_id = f"lho_{uuid.uuid4().hex[:12]}"
            obj = SQLLongHorizonObjective(
                id=obj_id,
                title=title,
                description=description,
                milestones=milestones,
                current_milestone_index=0,
                status="IN_PROGRESS",
                assigned_house=house
            )
            db.add(obj)
            if not session:
                await db.commit()
            return LongHorizonObjectiveSchema.model_validate(obj)
        finally:
            if not session:
                await async_gen.aclose()
                
    @staticmethod
    async def get_active_objectives(session: AsyncSession = None) -> List[LongHorizonObjectiveSchema]:
        """Retrieves all currently active long-horizon objectives."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            stmt = select(SQLLongHorizonObjective).filter_by(status="IN_PROGRESS")
            result = await db.execute(stmt)
            records = result.scalars().all()
            return [LongHorizonObjectiveSchema.model_validate(r) for r in records]
        finally:
            if not session:
                await async_gen.aclose()

long_horizon_tracker = LongHorizonTracker()
