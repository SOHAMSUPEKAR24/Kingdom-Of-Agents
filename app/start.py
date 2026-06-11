import uvicorn
import logging
from app.core.config import settings

logger = logging.getLogger("antigravity.start")

def main():
    logger.info("Booting ANTIGRAVITY Phase 11 Production Runtime...")
    logger.info("StatReload/HotReload is DISABLED to protect cognitive mutations.")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1 # Single worker required to maintain singleton cognitive engine state in memory
    )

if __name__ == "__main__":
    main()
