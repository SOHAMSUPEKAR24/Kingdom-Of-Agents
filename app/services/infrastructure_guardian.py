import asyncio
import logging
from typing import Dict, Any

from app.models.schemas import engine
from app.services.memory_service import memory_service
from app.core.config import settings

logger = logging.getLogger("antigravity.guardian")

class InfrastructureGuardian:
    def __init__(self):
        self.health_state = {
            "postgres": "UNKNOWN",
            "redis": "UNKNOWN",
            "qdrant": "UNKNOWN",
            "neo4j": "UNKNOWN",
            "civilization_status": "ONLINE"
        }

    async def verify_infrastructure(self):
        logger.info("🛡️ [INFRA GUARDIAN] Initiating strict reality audit of all persistent infrastructure...")
        
        # 1. Verify Postgres
        try:
            async with engine.begin() as conn:
                from sqlalchemy import text
                await conn.run_sync(lambda sync_conn: sync_conn.execute(text("SELECT 1")))
            self.health_state["postgres"] = "HEALTHY"
        except Exception as e:
            logger.error(f"❌ [INFRA GUARDIAN] PostgreSQL Reality Check Failed: {e}")
            self.health_state["postgres"] = "OFFLINE"

        # 2. Verify Redis (from event_bus)
        from app.core.event_bus import event_bus
        if event_bus.redis:
            try:
                await event_bus.redis.ping()
                self.health_state["redis"] = "HEALTHY"
            except Exception as e:
                logger.error(f"❌ [INFRA GUARDIAN] Redis Reality Check Failed: {e}")
                self.health_state["redis"] = "OFFLINE"
        else:
            self.health_state["redis"] = "OFFLINE"

        # 3. Verify Qdrant
        if memory_service.qdrant_client:
            try:
                memory_service.qdrant_client.get_collections()
                self.health_state["qdrant"] = "HEALTHY"
            except Exception as e:
                logger.error(f"❌ [INFRA GUARDIAN] Qdrant Reality Check Failed: {e}")
                self.health_state["qdrant"] = "OFFLINE"
        else:
            self.health_state["qdrant"] = "OFFLINE"

        # 4. Verify Neo4j
        if memory_service.neo4j_driver:
            try:
                async with memory_service.neo4j_driver.session() as session:
                    await session.run("RETURN 1")
                self.health_state["neo4j"] = "HEALTHY"
            except Exception as e:
                logger.error(f"❌ [INFRA GUARDIAN] Neo4j Reality Check Failed: {e}")
                self.health_state["neo4j"] = "OFFLINE"
        else:
            self.health_state["neo4j"] = "OFFLINE"

        # Evaluate overall status
        if all(v == "HEALTHY" for k, v in self.health_state.items() if k != "civilization_status"):
            self.health_state["civilization_status"] = "ONLINE_AND_STABLE"
            logger.info("🛡️ [INFRA GUARDIAN] All persistent intelligence modules VERIFIED. Civilization is STABLE.")
        else:
            self.health_state["civilization_status"] = "DEGRADED_CRITICAL"
            logger.warning("⚠️ [INFRA GUARDIAN] Phase 11 Directive: Civilization marked DEGRADED due to missing reality infrastructure!")

    async def get_health_report(self) -> Dict[str, Any]:
        await self.verify_infrastructure()
        return self.health_state

infrastructure_guardian = InfrastructureGuardian()
