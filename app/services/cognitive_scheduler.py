import asyncio
import logging
from typing import Callable, Coroutine, Any

logger = logging.getLogger("antigravity.scheduler")

class CognitiveScheduler:
    def __init__(self):
        self.tasks = []

    def schedule_background_loop(self, name: str, func: Callable[[], Coroutine[Any, Any, Any]], interval_sec: float) -> asyncio.Task:
        """
        Throttles a background task to run at fixed intervals safely,
        preventing CPU starvation from tight 'while True' loops.
        """
        async def loop():
            logger.info(f"⏱️ [SCHEDULER] Booted background cognitive loop: {name}")
            try:
                while True:
                    await asyncio.sleep(interval_sec)
                    try:
                        await func()
                    except Exception as loop_e:
                        logger.error(f"⚠️ [SCHEDULER] Inner exception in {name}: {loop_e}")
            except asyncio.CancelledError:
                logger.warning(f"🛑 [SCHEDULER] Background loop '{name}' cancelled/terminated.")
            except Exception as e:
                logger.error(f"🚨 [SCHEDULER] Background loop '{name}' crashed critically: {e}")
        
        task = asyncio.create_task(loop())
        self.tasks.append(task)
        return task

    async def shutdown_all(self):
        for t in self.tasks:
            t.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()

cognitive_scheduler = CognitiveScheduler()
