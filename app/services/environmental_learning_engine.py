import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EnvironmentalLearningEngine:
    """
    Observes execution environments and adapts civilization parameters to shifts (e.g. rate limits, network latency).
    """

    async def evaluate_environment_shift(self, current_metrics: Dict[str, Any], historical_metrics: Dict[str, Any]) -> dict:
        """
        Compares current environment telemetry against historical norms.
        """
        adaptations = {}
        
        # Detect latency increases
        curr_latency = current_metrics.get("avg_latency_ms", 100)
        hist_latency = historical_metrics.get("avg_latency_ms", 100)
        
        if curr_latency > hist_latency * 1.5:
            adaptations["timeout_multiplier"] = 2.0
            logger.warning("🌍 [ENVIRONMENT] High latency detected. Adapting timeout parameters.")
            
        # Detect rate limiting
        if current_metrics.get("rate_limit_hits", 0) > 0:
            adaptations["concurrency_limit"] = max(1, historical_metrics.get("concurrency_limit", 5) // 2)
            logger.warning("🌍 [ENVIRONMENT] Rate limits detected. Throttling swarm concurrency.")
            
        return adaptations

environmental_learning_engine = EnvironmentalLearningEngine()
