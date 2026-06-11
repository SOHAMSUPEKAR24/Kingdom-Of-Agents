import logging
import random
import math
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.models import schemas
from app.models.schemas import SQLReinforcementEvent

logger = logging.getLogger("antigravity.reinforcement")

class ReinforcementEngine:
    def __init__(self):
        # House topological coordinates/routing weights
        self._house_weights = {
            "StrategyHouse": 1.0,
            "ResearchHouse": 1.0,
            "EngineeringHouse": 1.0,
            "SecurityHouse": 1.0,
            "MemoryHouse": 1.0
        }
        self._level_history: List[Dict[str, Any]] = []
        
        # Bayesian Success Probability P(Success|Evidence) initialized to 0.85
        self._bayesian_success_probability = {
            "StrategyHouse": 0.85,
            "ResearchHouse": 0.85,
            "EngineeringHouse": 0.85,
            "SecurityHouse": 0.85,
            "MemoryHouse": 0.85
        }
        
        # Initial prompt blocks for each House
        self._prompts = {
            "StrategyHouse": {
                "template": "Analyze task requirements, check constraints against the Constitution, and formulate the exact routing steps.",
                "version": "1.0",
                "parent_version": "1.0",
                "history": [1.0]
            },
            "ResearchHouse": {
                "template": "Crawl available text contexts, find semantic abstractions, and gather target dataset documentation.",
                "version": "1.0",
                "parent_version": "1.0",
                "history": [1.0]
            },
            "EngineeringHouse": {
                "template": "Write functional, clean, secure python routines that compile without dependencies and avoid complex side-effects.",
                "version": "1.0",
                "parent_version": "1.0",
                "history": [1.0]
            },
            "SecurityHouse": {
                "template": "Audit output snippets statically, filter banned keywords, and verify compliance with Constitutional limits.",
                "version": "1.0",
                "parent_version": "1.0",
                "history": [1.0]
            },
            "MemoryHouse": {
                "template": "Index abstract logs semantically, apply relevance compression ratios, and update topological graph paths.",
                "version": "1.0",
                "parent_version": "1.0",
                "history": [1.0]
            }
        }
        
        # Mutation mutations library
        self._mutations = [
            "Ensure all outputs are fully wrapped in structured JSON layouts.",
            "Verify all border boundaries and explicitly validate extreme empty parameters.",
            "Enforce strict AST safety parameters and reject any non-isolated filesystem write operations.",
            "Minimize memory profile footprint and prioritize fast, cached in-memory index queries.",
            "Embed exhaustive debug diagnostics and include clean error traceback logs.",
            "Abstain from using external API requests and fall back gracefully to local SQLite structures."
        ]

    async def reward_house(self, house: str, score: float):
        """Elevates target House prompt routing weight, updates Bayesian probability, and handles prompt evolution."""
        current = self._house_weights.get(house, 1.0)
        # Increase weight slightly up to max 2.5
        new_weight = min(2.5, current + (score * 0.05))
        self._house_weights[house] = round(new_weight, 3)
        logger.info(f"🧬 [TOPOLOGY WEIGHT ELEVATED] House '{house}' rewarded. Weight: {current} -> {new_weight}")
        
        # Update Bayesian success probability
        p_new = self.update_bayesian_probability(house, success=True)
        
        # Log to Database
        await self.log_reinforcement_event(
            house=house,
            event_type="REWARD",
            before_value=f"weight: {current}, P(Success): {p_new}",
            after_value=f"weight: {new_weight}, P(Success): {p_new}",
            fitness_score=score
        )
        
        # Evolve prompt based on score
        await self.evolve_prompt_for_house(house, score)

    async def penalize_house(self, house: str):
        """Reduces target House prompt weight, updates Bayesian probability, and triggers prompt repair/mutation."""
        current = self._house_weights.get(house, 1.0)
        # Decrease weight down to min 0.5
        new_weight = max(0.5, current - 0.1)
        self._house_weights[house] = round(new_weight, 3)
        logger.warning(f"⚠️ [TOPOLOGY WEIGHT REDUCED] House '{house}' penalized! Weight: {current} -> {new_weight}")
        
        # Update Bayesian success probability
        p_new = self.update_bayesian_probability(house, success=False)
        
        # Log to Database
        await self.log_reinforcement_event(
            house=house,
            event_type="DECAY",
            before_value=f"weight: {current}",
            after_value=f"weight: {new_weight}",
            fitness_score=0.2
        )
        
        # Penalizing triggers prompt repair mutation
        await self.evolve_prompt_for_house(house, 0.2)

    async def get_active_weights(self) -> Dict[str, float]:
        return self._house_weights

    async def get_prompt_for_house(self, house: str) -> Dict[str, Any]:
        return self._prompts.get(house, {
            "template": "Fallback instructions",
            "version": "0.1",
            "parent_version": "0.1",
            "history": []
        })

    async def evolve_prompt_for_house(self, house: str, score: float):
        """
        Applies genetic prompt mutation. If the score is high, marks as parent.
        If score is low, mutates prompt using a random instruction mutation to adapt.
        """
        if house not in self._prompts:
            return
            
        p_info = self._prompts[house]
        p_info["history"].append(score)
        
        # Keep rolling history limit
        if len(p_info["history"]) > 10:
            p_info["history"].pop(0)
            
        avg_score = sum(p_info["history"]) / len(p_info["history"])
        before_template = p_info["template"]
        
        if score >= 0.9:
            # High score, mark this version as a successful parent template
            p_info["parent_version"] = p_info["version"]
            logger.info(f"🧬 [GENETIC PROMPT SUCCESS] House '{house}' prompt {p_info['version']} certified as parent.")
        elif score < 0.7:
            # Low score, trigger prompt mutation (mutation phase)
            curr_ver = float(p_info["version"])
            next_ver = round(curr_ver + 0.1, 2)
            
            # Select random mutation directive that isn't already in prompt
            available_mutations = [m for m in self._mutations if m not in p_info["template"]]
            if not available_mutations:
                # Reset prompt to initial and start fresh
                available_mutations = self._mutations
            
            chosen_mutation = random.choice(available_mutations)
            
            # Formulate mutated prompt: combine base parent pattern with mutated constraint
            p_info["template"] = f"{p_info['template']} Mutated Constraint: {chosen_mutation}"
            p_info["version"] = str(next_ver)
            
            logger.warning(f"🧬 [GENETIC PROMPT MUTATED] House '{house}' prompt underwent mutation! New Version: {p_info['version']}, Added: '{chosen_mutation}'")
            
            await self.log_reinforcement_event(
                house=house,
                event_type="GENETIC_MUTATION",
                before_value=before_template,
                after_value=p_info["template"],
                fitness_score=score
            )
            
        await self.record_evolution_step(house, p_info["version"], score)

    def update_bayesian_probability(self, house: str, success: bool) -> float:
        """
        Updates the probability of successful house execution P(Success|Evidence) following an audit.
        P(Success|Audit) = P(Audit|Success) * P(Success) / P(Audit)
        """
        p_old = self._bayesian_success_probability.get(house, 0.85)
        if success:
            # Likelihood P(SuccessEvent|SuccessHouse) = 0.95, P(SuccessEvent|FailingHouse) = 0.15
            p_success_given_success = 0.95
            p_success_given_failure = 0.15
            numerator = p_old * p_success_given_success
            denominator = numerator + (1.0 - p_old) * p_success_given_failure
        else:
            # Likelihood P(FailureEvent|SuccessHouse) = 0.05, P(FailureEvent|FailingHouse) = 0.85
            p_failure_given_success = 0.05
            p_failure_given_failure = 0.85
            numerator = p_old * p_failure_given_success
            denominator = numerator + (1.0 - p_old) * p_failure_given_failure
            
        p_new = round(numerator / denominator, 4) if denominator > 0 else 0.0
        self._bayesian_success_probability[house] = p_new
        logger.info(f"🧬 [BAYESIAN FITNESS UPDATE] House '{house}' success probability: {p_old} -> {p_new}")
        return p_new

    def calculate_shannon_entropy(self, text: str) -> float:
        """Computes the Shannon entropy of character distributions in the dynamic code output to rank lineage stability."""
        if not text:
            return 0.0
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1
        total = len(text)
        entropy = 0.0
        for count in frequencies.values():
            p = count / total
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    async def log_reinforcement_event(self, house: str, event_type: str, before_value: str, after_value: str, fitness_score: float):
        try:
            async with schemas.async_session() as session:
                event = SQLReinforcementEvent(
                    id=str(uuid.uuid4()),
                    house=house,
                    event_type=event_type,
                    before_value=before_value,
                    after_value=after_value,
                    fitness_score=fitness_score,
                    created_at=datetime.utcnow()
                )
                session.add(event)
                await session.commit()
        except Exception as e:
            logger.error(f"Failed to save reinforcement event: {e}")

    async def record_evolution_step(self, house: str, prompt_ver: str, success_ratio: float):
        self._level_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "house": house,
            "prompt_version": prompt_ver,
            "success_ratio": success_ratio
        })
        # Save reinforcement record to DB as well
        await self.log_reinforcement_event(
            house=house,
            event_type="GENETIC_MUTATION",
            before_value=None,
            after_value=f"Prompt Version: {prompt_ver}",
            fitness_score=success_ratio
        )

reinforcement_engine = ReinforcementEngine()
