import logging
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import SQLSpecialistDoctrine

logger = logging.getLogger(__name__)

class DoctrineAutomationEngine:
    """
    Converts repeated successful workflows into reusable doctrines that future agents automatically inherit.
    """
    
    def __init__(self):
        self.name = "DOCTRINE_AUTOMATION_ENGINE"

    async def initialize(self):
        from app.core.event_bus import event_bus
        event_bus.subscribe("EXPERIMENT_COMPLETED", self.handle_experiment_completed)

    async def handle_experiment_completed(self, event):
        payload = event.payload
        exp_id = payload.get("experiment_id")
        result = payload.get("result")
        if exp_id and result == "PROVEN":
            from app.models.schemas import async_session
            async with async_session() as session:
                await self.formulate_doctrine(
                    db_session=session,
                    dynasty="Scientific",
                    capability_domain="Empirical Analysis",
                    execution_trace_id=exp_id,
                    success_score=0.95
                )
                await session.commit()

    async def formulate_doctrine(self, db_session: AsyncSession, dynasty: str, capability_domain: str, execution_trace_id: str, success_score: float) -> Optional[SQLSpecialistDoctrine]:
        """
        Takes a highly successful execution trace and abstracts it into a formal doctrine.
        """
        if success_score < 0.9:
            logger.warning(f"⚠️ [DOCTRINE_ENGINE] Trace {execution_trace_id} score ({success_score}) too low to formulate doctrine.")
            return None

        # Simulate abstraction of the trace into a doctrine
        doctrine_text = f"Always ensure modular separation of concerns when executing {capability_domain} tasks. Derived from {execution_trace_id}."

        doctrine_id = f"DOC-{uuid.uuid4().hex[:8]}"
        doctrine = SQLSpecialistDoctrine(
            id=doctrine_id,
            dynasty=dynasty,
            capability_domain=capability_domain,
            doctrine_text=doctrine_text,
            source_trace_id=execution_trace_id,
            validation_score=success_score
        )
        db_session.add(doctrine)
        
        logger.info(f"📜 [DOCTRINE_ENGINE] New doctrine formulated for {dynasty} in {capability_domain}: {doctrine_id}")
        return doctrine

doctrine_automation_engine = DoctrineAutomationEngine()
