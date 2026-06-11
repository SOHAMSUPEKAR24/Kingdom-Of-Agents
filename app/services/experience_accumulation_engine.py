import logging
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import SQLExperienceVector
import uuid

logger = logging.getLogger(__name__)

class ExperienceAccumulationEngine:
    """
    Accumulates real experience from execution telemetry.
    Applies Experience Priority Weighting (high for rare failures, expensive mistakes, discoveries).
    """

    def _calculate_priority_weight(self, success: bool, outcome_summary: str) -> float:
        """
        Weights experience heavily if it contains critical errors, rare timeouts, or massive success.
        """
        weight = 1.0
        summary = outcome_summary.lower() if outcome_summary else ""
        
        if not success:
            if "timeout" in summary:
                weight = 5.0 # High value for learning limits
            elif "syntaxerror" in summary or "typeerror" in summary:
                weight = 3.0 # Standard mistake
            else:
                weight = 8.0 # Unknown/rare failure, highly valuable to learn from
        else:
            if "success" in summary and "benchmark" in summary:
                weight = 10.0 # Benchmark jumps are the most valuable
            elif "discovered" in summary or "novel" in summary:
                weight = 7.0
                
        return weight

    async def accumulate_experience(self, agent_id: str, task_id: str, telemetry: List[Dict[str, Any]], session: AsyncSession) -> SQLExperienceVector:
        """
        Processes raw telemetry and extracts a weighted experience vector.
        """
        success_count = sum(1 for t in telemetry if t.get("success"))
        total = len(telemetry) or 1
        success_rating = success_count / total
        
        failure_severity = 0.0
        lessons = []
        max_weight = 1.0
        
        for t in telemetry:
            weight = self._calculate_priority_weight(t.get("success", False), t.get("outcome_summary", ""))
            max_weight = max(max_weight, weight)
            
            if not t.get("success"):
                failure_severity += weight
                lessons.append(f"Failed {t.get('interaction_type')} on {t.get('target')}: {t.get('outcome_summary')[:50]}")
                
        # Normalize failure severity
        failure_severity = min(1.0, failure_severity / (total * 10.0))
        
        vector = SQLExperienceVector(
            id=f"exp_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id,
            task_id=task_id,
            success_rating=success_rating,
            failure_severity=failure_severity,
            extracted_lessons=list(set(lessons))[:5], # Keep top 5 unique lessons
            strategic_weight=max_weight
        )
        
        session.add(vector)
        await session.flush()
        
        logger.info(f"🧠 [EXPERIENCE ENGINE] Accumulated experience for {agent_id}. Weight: {max_weight}")
        return vector

experience_accumulation_engine = ExperienceAccumulationEngine()
