import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLPracticeCampaign
# Fallback import if SQLCapabilityGap exists
try:
    from app.models.schemas import SQLCapabilityGap
except ImportError:
    SQLCapabilityGap = None

from app.services.capability_tree_engine import capability_tree_engine

logger = logging.getLogger(__name__)

class CapabilityGapEngine:
    """
    Continuously discovers missing tools, weak domains, failing benchmarks, and low-confidence areas.
    Creates improvement campaigns for the practice engine.
    """

    def __init__(self):
        self.name = "CAPABILITY_GAP_ENGINE"
        self.version = "1.0.0"

    async def detect_gaps_and_create_campaigns(self, db_session: AsyncSession):
        """
        Scans the Capability Tree for weak nodes and creates practice campaigns.
        """
        weak_nodes = await capability_tree_engine.get_weak_capabilities(db_session, threshold=0.5)
        
        campaigns = []
        for node in weak_nodes:
            # Check if an active campaign already exists
            query = select(SQLPracticeCampaign).where(
                SQLPracticeCampaign.target_capability_id == node.id,
                SQLPracticeCampaign.status == "ACTIVE"
            )
            result = await db_session.execute(query)
            active_campaign = result.scalars().first()
            
            if not active_campaign:
                campaign_id = f"CAMP-{uuid.uuid4().hex[:8]}"
                campaign = SQLPracticeCampaign(
                    id=campaign_id,
                    target_capability_id=node.id,
                    objective=f"Improve mastery of {node.domain} -> {node.skill_name}. Current score: {node.mastery_score:.2f}",
                    status="ACTIVE",
                    iterations_completed=0,
                    improvement_score=0.0
                )
                db_session.add(campaign)
                campaigns.append(campaign)
                logger.info(f"🚨 [GAP_ENGINE] Discovered gap in {node.skill_name}. Created improvement campaign {campaign_id}")
                
        return campaigns

    async def detect_gaps(self, db_session: AsyncSession):
        """
        Legacy compat: Analyzes the system's ability to fulfill objectives and detects missing domains.
        """
        gap_id = f"GAP-{uuid.uuid4().hex[:8]}"
        if SQLCapabilityGap:
            gap = SQLCapabilityGap(
                id=gap_id,
                domain="Visual UI Interaction",
                identified_weakness="The civilization lacks direct optical parsing of complex CSS grids.",
                severity_score=0.8
            )
            db_session.add(gap)
            return gap
        return None

capability_gap_engine = CapabilityGapEngine()
