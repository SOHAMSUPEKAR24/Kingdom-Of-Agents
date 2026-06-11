import logging
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLWorldInteractionLog
import datetime

logger = logging.getLogger(__name__)

class ExecutionObserverEngine:
    """
    Monitors all real-time executions (terminal, browser) and generates structured telemetry.
    Acts as the sensory input for the Experience Accumulation Engine.
    """
    
    async def observe_recent_interactions(self, agent_id: str, minutes_back: int, session: AsyncSession) -> List[Dict[str, Any]]:
        """
        Retrieves raw interaction logs for a given agent in the specified time window.
        """
        time_threshold = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_back)
        result = await session.execute(
            select(SQLWorldInteractionLog)
            .where(SQLWorldInteractionLog.agent_id == agent_id)
            .where(SQLWorldInteractionLog.created_at >= time_threshold)
            .order_by(SQLWorldInteractionLog.created_at.desc())
        )
        logs = result.scalars().all()
        
        telemetry = []
        for log in logs:
            telemetry.append({
                "interaction_type": log.interaction_type,
                "target": log.target,
                "success": bool(log.success),
                "action_payload": log.action_payload,
                "outcome_summary": log.outcome_summary,
                "timestamp": log.created_at.isoformat()
            })
        
        return telemetry

execution_observer_engine = ExecutionObserverEngine()
