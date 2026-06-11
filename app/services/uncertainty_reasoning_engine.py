class UncertaintyReasoningEngine:
    def __init__(self):
        self.name = "UNCERTAINTY_REASONING_ENGINE"
        self.version = "1.0.0"

    async def calculate_confidence(self, hypothesis: str, evidence: list):
        """
        Calculates a probabilistic confidence score for a given hypothesis
        based on supporting and contradicting evidence.
        """
        if not evidence:
            return {"confidence": 0.0, "uncertainty": 1.0, "reason": "No evidence"}
            
        supporting = sum(1 for e in evidence if e.get('supports_hypothesis', False))
        total = len(evidence)
        confidence = supporting / total
        
        return {
            "confidence": confidence,
            "uncertainty": 1.0 - confidence,
            "reason": f"{supporting}/{total} evidence markers support this."
        }

    async def detect_ambiguity(self, text: str):
        """
        Analyzes a strategic directive or hypothesis for ambiguous language.
        """
        ambiguous_keywords = ["maybe", "might", "possibly", "could", "unknown"]
        score = sum(1 for word in ambiguous_keywords if word in text.lower())
        return {"ambiguity_score": min(1.0, score * 0.2)}

uncertainty_reasoning_engine = UncertaintyReasoningEngine()
