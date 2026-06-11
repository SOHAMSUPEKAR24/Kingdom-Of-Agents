import uuid
import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLCapabilityNode

logger = logging.getLogger(__name__)

class CapabilityTreeEngine:
    """
    Manages the hierarchical capability tree and mastery progression independently.
    Tracks expertise across domains, sub-domains, and specific skills.
    """

    def __init__(self):
        self.name = "CAPABILITY_TREE_ENGINE"
        self.version = "1.0.0"

    async def seed_initial_trees(self, db_session: AsyncSession):
        """Seeds the database with initial capability trees if empty."""
        result = await db_session.execute(select(SQLCapabilityNode).limit(1))
        if result.scalars().first():
            return  # Already seeded

        initial_capabilities = [
            ("Software Engineering", "Python", "FastAPI"),
            ("Software Engineering", "Python", "Testing"),
            ("Software Engineering", "Infrastructure", "Docker"),
            ("Software Engineering", "Infrastructure", "Kubernetes"),
            ("Cybersecurity", "Offensive", "Linux"),
            ("Cybersecurity", "Offensive", "Web Security"),
            ("Cybersecurity", "Defensive", "Network Security"),
            ("Cybersecurity", "Analysis", "Malware Analysis"),
            ("Data Science", "Machine Learning", "PyTorch"),
            ("Data Science", "Data Processing", "Pandas")
        ]

        for domain, sub_domain, skill in initial_capabilities:
            node_id = f"CAP-{uuid.uuid4().hex[:8]}"
            node = SQLCapabilityNode(
                id=node_id,
                domain=domain,
                sub_domain=sub_domain,
                skill_name=skill,
                mastery_score=0.0,
                last_benchmark_score=0.0
            )
            db_session.add(node)
        
        await db_session.commit()
        logger.info("🌱 [CAPABILITY_TREE] Initial capability trees seeded.")

    async def update_mastery(self, db_session: AsyncSession, domain: str, skill_name: str, new_benchmark_score: float) -> Optional[SQLCapabilityNode]:
        """
        Updates the mastery score of a specific skill based on a new benchmark result.
        The mastery score is a moving average or weighted progression of benchmarks.
        """
        query = select(SQLCapabilityNode).where(
            SQLCapabilityNode.domain == domain,
            SQLCapabilityNode.skill_name == skill_name
        )
        result = await db_session.execute(query)
        node = result.scalars().first()

        if not node:
            logger.warning(f"⚠️ [CAPABILITY_TREE] Capability Node {domain} -> {skill_name} not found.")
            return None

        # Reality enforcement: Calculate real measurable improvement
        # A simple weighted average for mastery progression
        node.last_benchmark_score = new_benchmark_score
        node.mastery_score = (node.mastery_score * 0.7) + (new_benchmark_score * 0.3)
        
        logger.info(f"📈 [CAPABILITY_TREE] Mastery for {skill_name} updated to {node.mastery_score:.2f}")
        return node

    async def get_weak_capabilities(self, db_session: AsyncSession, threshold: float = 0.5) -> List[SQLCapabilityNode]:
        """Returns capabilities with a mastery score below the specified threshold."""
        query = select(SQLCapabilityNode).where(SQLCapabilityNode.mastery_score < threshold)
        result = await db_session.execute(query)
        return list(result.scalars().all())

capability_tree_engine = CapabilityTreeEngine()
