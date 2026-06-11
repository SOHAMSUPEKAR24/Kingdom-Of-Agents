import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schemas import SQLExperienceVector

logger = logging.getLogger(__name__)

class ExperienceReasoningEngine:
    """
    Augments standard LLM reasoning by injecting historical success rates and past experience abstractions.
    """

    async def augment_prompt_with_experience(self, base_prompt: str, task_id: str, session: AsyncSession) -> str:
        """
        Injects highly weighted past lessons into the prompt to prevent repeated failures.
        """
        # Fetch relevant heavy experiences
        result = await session.execute(
            select(SQLExperienceVector)
            .where(SQLExperienceVector.strategic_weight >= 5.0)
            .order_by(SQLExperienceVector.created_at.desc())
            .limit(3)
        )
        experiences = result.scalars().all()
        
        if not experiences:
            return base_prompt
            
        lessons_context = "\n".join([f"- {l}" for exp in experiences for l in exp.extracted_lessons])
        
        augmented_prompt = f"""
{base_prompt}

[EXPERIENCE WEIGHTED REASONING INJECTION]
CRITICAL PAST LESSONS TO HEED:
{lessons_context}
"""
        logger.info("🧠 [EXPERIENCE REASONING] Augmented prompt with past heavy experiences.")
        return augmented_prompt

experience_reasoning_engine = ExperienceReasoningEngine()
