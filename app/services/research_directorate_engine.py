import logging
import uuid
from datetime import datetime
from sqlalchemy import select
from app.models.schemas import async_session, SQLResearchCampaign

logger = logging.getLogger("antigravity.research_directorate")

class ResearchDirectorateEngine:
    def __init__(self):
        self.name = "RESEARCH_DIRECTORATE_ENGINE"
        self.version = "17.95"
        self.capabilities = [
            "FastAPI Development",
            "Browser Automation",
            "Docker Engineering",
            "Security Analysis"
        ]

    async def get_or_create_campaign(self, capability: str) -> SQLResearchCampaign:
        async with async_session() as session:
            # 1. Find active campaign
            stmt = select(SQLResearchCampaign).where(
                SQLResearchCampaign.capability == capability,
                SQLResearchCampaign.status == "ACTIVE"
            )
            result = await session.execute(stmt)
            campaign = result.scalars().first()
            
            if not campaign:
                # 2. Create if none exists
                logger.info(f"🚀 [RESEARCH DIRECTORATE] Spawning new Research Campaign for {capability}")
                campaign = SQLResearchCampaign(
                    id=f"camp_{uuid.uuid4().hex[:8]}",
                    capability=capability,
                    token_budget=100000.0,
                    experiment_budget=50,
                    success_criteria=f"Master {capability} patterns with 0 LLM calls",
                    status="ACTIVE",
                    created_at=datetime.utcnow()
                )
                session.add(campaign)
                await session.commit()
                await session.refresh(campaign)
                
            return campaign

    async def check_campaign_budget(self, campaign_id: str) -> bool:
        async with async_session() as session:
            stmt = select(SQLResearchCampaign).where(SQLResearchCampaign.id == campaign_id)
            result = await session.execute(stmt)
            campaign = result.scalars().first()
            
            if not campaign:
                return False
                
            if campaign.status != "ACTIVE":
                return False
                
            if campaign.experiments_run >= campaign.experiment_budget:
                logger.warning(f"🛑 [RESEARCH DIRECTORATE] Campaign {campaign.id} ({campaign.capability}) reached experiment budget! Marking COMPLETED.")
                campaign.status = "COMPLETED"
                await session.commit()
                return False
                
            return True

    async def record_experiment_run(self, campaign_id: str, tokens: float = 0.0):
        async with async_session() as session:
            stmt = select(SQLResearchCampaign).where(SQLResearchCampaign.id == campaign_id)
            result = await session.execute(stmt)
            campaign = result.scalars().first()
            
            if campaign:
                campaign.experiments_run += 1
                campaign.tokens_spent += tokens
                await session.commit()

    async def propose_research_goal(self, unknown_variable: str):
        """Legacy stub."""
        return {
            "research_goal": f"Determine the exact limit of {unknown_variable}",
            "priority": "HIGH"
        }

research_directorate_engine = ResearchDirectorateEngine()
