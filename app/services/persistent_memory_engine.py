import logging
from sqlalchemy import select
from app.models.schemas import async_session, SQLTask, SQLAgentState
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.persistence")

class PersistentMemoryEngine:
    def __init__(self):
        pass

    async def recover_civilization_state(self):
        """
        Runs on startup.
        Scans Postgres for any interrupted ACTIVE agents or RUNNING tasks
        and re-injects them into the event bus so the civilization doesn't
        lose its train of thought across server reboots.
        """
        logger.info("💾 [PERSISTENT ENGINE] Scanning deep storage for interrupted cognitive processes...")
        
        recovered_tasks = 0
        async with async_session() as session:
            # Find tasks that were running but the server died
            res = await session.execute(
                select(SQLTask).where(SQLTask.status.in_(["RUNNING", "PENDING"]))
            )
            tasks = res.scalars().all()
            
            for t in tasks:
                logger.info(f"💾 [PERSISTENT ENGINE] Recovering interrupted task '{t.id}'...")
                
                # We re-publish the TASK_ASSIGNED event so the assigned house picks it up again
                task_data = {
                    "id": t.id,
                    "title": t.title,
                    "parent_objective": t.parent_objective,
                    "assigned_house": t.assigned_house,
                    "status": "PENDING", # reset status to trigger pickup
                    "input_data": t.input_data,
                    "output_data": t.output_data,
                    "dependencies": t.dependencies
                }
                
                # Queue recovery event
                event = Event(
                    event_type="TASK_ASSIGNED",
                    sender="PersistentMemoryEngine",
                    payload={"task": task_data}
                )
                await event_bus.publish(event)
                recovered_tasks += 1
                
        if recovered_tasks > 0:
            logger.warning(f"⚠️ [PERSISTENT ENGINE] Successfully recovered and re-queued {recovered_tasks} stranded tasks!")
        else:
            logger.info("✅ [PERSISTENT ENGINE] No stranded tasks found. Clean boot sequence.")

persistent_memory_engine = PersistentMemoryEngine()
