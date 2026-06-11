import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import (
    SQLSpecialistDynasty,
    SQLCapabilityNode,
    SQLPracticeCampaign,
    SQLSpecialistPromotion
)

logger = logging.getLogger(__name__)

class SpecialistDashboard:
    """
    Generates a consolidated view of the Specialist Civilization:
    - Dynasties
    - Mastery Levels
    - Skill Trees
    - Promotions
    - Capability Gaps
    - Improvement Campaigns
    """

    async def generate_dashboard_report(self, db_session: AsyncSession) -> dict:
        """Compiles the metrics for the dashboard."""
        
        # Fetch Dynasties
        dynasties = await db_session.execute(select(SQLSpecialistDynasty))
        dynasties = dynasties.scalars().all()

        # Fetch Capabilities (Skill Trees & Mastery)
        capabilities = await db_session.execute(select(SQLCapabilityNode))
        capabilities = capabilities.scalars().all()

        # Fetch Promotions
        promotions = await db_session.execute(select(SQLSpecialistPromotion).order_by(SQLSpecialistPromotion.created_at.desc()).limit(10))
        promotions = promotions.scalars().all()

        # Fetch Campaigns (Gaps/Improvement)
        campaigns = await db_session.execute(select(SQLPracticeCampaign).where(SQLPracticeCampaign.status == "ACTIVE"))
        campaigns = campaigns.scalars().all()

        report = {
            "dynasties": [{"name": d.dynasty_name, "members": d.member_count, "mastery": d.total_mastery_level} for d in dynasties],
            "capabilities": [{"domain": c.domain, "skill": c.skill_name, "mastery": c.mastery_score} for c in capabilities],
            "promotions": [{"agent": p.agent_id, "rank": p.new_rank, "dynasty": p.dynasty} for p in promotions],
            "active_campaigns": [{"objective": c.objective, "target": c.target_capability_id} for c in campaigns]
        }
        
        logger.info("📊 [DASHBOARD] Generated Specialist Civilization Report.")
        return report

specialist_dashboard = SpecialistDashboard()
