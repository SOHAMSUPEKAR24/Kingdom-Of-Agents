from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import get_db_session, SQLTask
import logging

logger = logging.getLogger(__name__)

class TaskRecoveryEngine:
    """
    On restart, queries for tasks that were RUNNING but never finished,
    and resets them to PENDING so the civilization can resume execution.
    """
    
    @staticmethod
    async def recover_unfinished_tasks(session: AsyncSession = None) -> int:
        """Finds interrupted tasks and requeues them."""
        logger.info("Initializing Task Recovery Engine...")
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            # Find tasks that were RUNNING
            stmt = select(SQLTask).filter_by(status="RUNNING")
            result = await db.execute(stmt)
            interrupted_tasks = result.scalars().all()
            
            count = len(interrupted_tasks)
            if count > 0:
                logger.warning(f"Found {count} interrupted tasks. Requeuing for recovery...")
                for task in interrupted_tasks:
                    task.status = "PENDING"
                
                if not session:
                    await db.commit()
                    
            return count
        except Exception as e:
            logger.error(f"Task recovery failed: {e}")
            raise
        finally:
            if not session:
                await async_gen.aclose()

task_recovery_engine = TaskRecoveryEngine()
