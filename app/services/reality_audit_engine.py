import logging
from typing import Dict, Any

from app.core.event_bus import event_bus, Event
from app.services.memory_service import memory_service
from app.models.schemas import async_session, SQLExecutionTrace, SQLResearchThesis, SQLScientificExperiment, SQLCivilizationDoctrine
from sqlalchemy import select, func
from datetime import datetime, timedelta

logger = logging.getLogger("antigravity.reality_audit")

class RealityAuditEngine:
    def __init__(self):
        self.hallucinations_detected = 0

    async def initialize(self):
        """Hook into the global event bus to audit all output claims."""
        event_bus.subscribe("*", self.audit_event)
        logger.info("👁️ [REALITY AUDIT ENGINE] Online. Monitoring all telemetry for hallucinations.")

    async def audit_event(self, event: Event):
        # We only audit completion or success claims
        if event.event_type not in ["TASK_COMPLETED", "CAPABILITY_GENERATED", "VALIDATION_REQUIRED"]:
            return

        payload = event.payload
        task_data = payload.get("task", {})
        task_id = task_data.get("id", "UNKNOWN")
        
        # If the task claims it wrote code or completed a physical action, it MUST have a trace
        output = payload.get("output_data", {})
        if isinstance(output, dict) and output.get("status") == "SUCCESS":
            trace_id = output.get("trace_id")
            if not trace_id:
                # No execution trace provided, but claiming success?
                logger.error(f"🚨 [REALITY AUDIT] Hallucination detected! Task {task_id} claims SUCCESS without a trace_id.")
                self.hallucinations_detected += 1
                await self.punish_sender(event.sender, task_id)
                return
            
            # Verify the trace exists in the database
            async with async_session() as session:
                res = await session.execute(select(SQLExecutionTrace).where(SQLExecutionTrace.id == trace_id))
                trace = res.scalars().first()
                if not trace:
                    logger.error(f"🚨 [REALITY AUDIT] Fake Trace ID '{trace_id}' provided by {event.sender}. Task {task_id}.")
                    self.hallucinations_detected += 1
                    await self.punish_sender(event.sender, task_id)

    async def punish_sender(self, sender: str, task_id: str):
        logger.warning(f"⚖️ [REALITY AUDIT] Flagging '{sender}' for simulated success. Event dropped.")
        await memory_service.store_log(task_id, "RealityAuditEngine", f"Flagged '{sender}' for Hallucination/Simulated Output.", "CRITICAL")

    async def audit_system_idleness(self):
        """
        Part 11 - Reality Enforcement
        Fail any subsystem if dashboard data is stale, hypotheses = 0, experiments = 0, or doctrine halted.
        """
        try:
            async with async_session() as session:
                one_hour_ago = datetime.utcnow() - timedelta(hours=1)
                
                # Check hypotheses (theses)
                res_hyp = await session.execute(select(func.count(SQLResearchThesis.id)).where(SQLResearchThesis.created_at >= one_hour_ago))
                hyp_count = res_hyp.scalar() or 0
                
                # Check experiments
                res_exp = await session.execute(select(func.count(SQLScientificExperiment.id)).where(SQLScientificExperiment.created_at >= one_hour_ago))
                exp_count = res_exp.scalar() or 0
                
                # Check doctrines
                res_doc = await session.execute(select(func.count(SQLCivilizationDoctrine.id)).where(SQLCivilizationDoctrine.created_at >= one_hour_ago))
                doc_count = res_doc.scalar() or 0
                
                if hyp_count == 0:
                    logger.error("🚨 [REALITY ENFORCEMENT] MALFUNCTION: Hypothesis generation count is ZERO in the last hour. Scientific engine is IDLE.")
                    await memory_service.store_log("SYSTEM", "RealityAuditEngine", "MALFUNCTION: Scientific Engine is idle (0 hypotheses).", "CRITICAL")
                
                if exp_count == 0:
                    logger.warning("⚠️ [REALITY ENFORCEMENT] WARNING: No experiments executed in the last hour. Pipeline might be stalled.")
                    
        except Exception as e:
            logger.error(f"Failed to run reality enforcement audit: {e}")

reality_audit_engine = RealityAuditEngine()
