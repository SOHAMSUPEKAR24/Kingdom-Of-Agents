import logging
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLExperienceVector, SQLWorkflowAbstraction, SQLCivilizationDoctrine
import uuid

logger = logging.getLogger(__name__)

class ExperienceDistillationEngine:
    """
    Implements the Hot -> Warm -> Cold memory hierarchy.
    Compresses raw experience vectors into workflow abstractions (WARM) 
    and further into doctrines (COLD).
    """

    async def distill_to_warm_memory(self, agent_id: str, session: AsyncSession):
        """
        Takes HOT memory (Experience Vectors) and compresses them into WARM memory (Workflow Abstractions).
        """
        # Fetch highly weighted experience vectors
        result = await session.execute(
            select(SQLExperienceVector)
            .where(SQLExperienceVector.agent_id == agent_id)
            .where(SQLExperienceVector.strategic_weight >= 5.0)
            .order_by(SQLExperienceVector.created_at.desc())
            .limit(10)
        )
        vectors = result.scalars().all()
        
        if not vectors:
            return None
            
        # Distill into a workflow abstraction
        lessons = [l for v in vectors for l in v.extracted_lessons]
        unique_lessons = list(set(lessons))
        
        abstraction = SQLWorkflowAbstraction(
            id=f"wf_{uuid.uuid4().hex[:8]}",
            title=f"Distilled Workflow for {agent_id}",
            trigger_conditions={"agent_id": agent_id, "lesson_count": len(unique_lessons)},
            execution_graph={"optimized_steps": unique_lessons[:5]},
            success_rate=sum(v.success_rating for v in vectors) / len(vectors),
            memory_tier="WARM"
        )
        
        session.add(abstraction)
        await session.flush()
        logger.info(f"🔥->🗂️ [DISTILLATION] Compressed {len(vectors)} experience vectors into WARM memory abstraction.")
        return abstraction

    async def distill_to_cold_memory(self, session: AsyncSession):
        """
        Takes WARM memory (Workflow Abstractions) and compresses them into COLD memory (Doctrines).
        """
        result = await session.execute(
            select(SQLWorkflowAbstraction)
            .where(SQLWorkflowAbstraction.memory_tier == "WARM")
            .where(SQLWorkflowAbstraction.success_rate >= 0.8)
            .limit(5)
        )
        abstractions = result.scalars().all()
        
        if not abstractions:
            return None
            
        philosophy = " ".join([a.title for a in abstractions])
        
        doctrine = SQLCivilizationDoctrine(
            id=f"doc_{uuid.uuid4().hex[:8]}",
            title="Ascended Strategy Pattern",
            philosophy_text=f"Derived from high-success workflows: {philosophy}",
            source_experiences=[a.id for a in abstractions],
            verification_score=sum(a.success_rate for a in abstractions) / len(abstractions)
        )
        
        # Upgrade tier to cold for processed abstractions (or delete them if pruning is aggressive)
        for a in abstractions:
            a.memory_tier = "COLD_PROCESSED"
            
        session.add(doctrine)
        await session.flush()
        logger.info(f"🗂️->🧊 [DISTILLATION] Compressed {len(abstractions)} WARM workflows into COLD Doctrine memory.")
        return doctrine

experience_distillation_engine = ExperienceDistillationEngine()
