import logging
from datetime import datetime
from sqlalchemy import select

from app.core.event_bus import event_bus, Event
from app.models.schemas import async_session, SQLToolMastery

logger = logging.getLogger("antigravity.tool_mastery")

class ToolMasteryEngine:
    def __init__(self):
        pass

    async def initialize(self):
        event_bus.subscribe("TOOL_EXECUTED", self.track_execution)
        logger.info("🔧 [TOOL MASTERY ENGINE] Online. Tracking tool execution metrics.")

    async def track_execution(self, event: Event):
        payload = event.payload
        tool_name = payload.get("tool_name")
        success = payload.get("success", False)
        latency_ms = payload.get("latency_ms", 0.0)

        if not tool_name:
            return

        async with async_session() as session:
            # Upsert logic
            res = await session.execute(select(SQLToolMastery).where(SQLToolMastery.tool_name == tool_name))
            record = res.scalars().first()

            if not record:
                # Create if not exists
                record = SQLToolMastery(
                    id=tool_name.lower().replace(" ", "_"),
                    tool_name=tool_name,
                    total_executions=0,
                    successful_executions=0,
                    failed_executions=0,
                    success_rate=0.0,
                    avg_latency_ms=0.0
                )
                session.add(record)

            # Update metrics
            record.total_executions += 1
            if success:
                record.successful_executions += 1
            else:
                record.failed_executions += 1

            record.success_rate = (record.successful_executions / record.total_executions) * 100
            
            # Simple moving average for latency
            record.avg_latency_ms = ((record.avg_latency_ms * (record.total_executions - 1)) + latency_ms) / record.total_executions
            record.last_used = datetime.utcnow()

            await session.commit()
            
            logger.info(f"📊 [TOOL MASTERY] {tool_name} usage tracked. Success Rate: {record.success_rate:.1f}%")

        # If success rate drops too low, request optimization
        if record.total_executions > 10 and record.success_rate < 80.0:
            await event_bus.publish(Event(
                event_type="TOOLCHAIN_OPTIMIZATION_REQUEST",
                sender="ToolMasteryEngine",
                payload={"tool_name": tool_name, "success_rate": record.success_rate}
            ))

tool_mastery_engine = ToolMasteryEngine()
