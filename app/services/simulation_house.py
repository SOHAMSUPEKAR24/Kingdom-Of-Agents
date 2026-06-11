import logging
import uuid
from typing import Dict, Any, List
from datetime import datetime
from app.models import schemas
from app.models.schemas import SQLSimulationScenario, SimulationScenarioSchema

logger = logging.getLogger("antigravity.simulation_house")

class SimulationHouseService:
    async def project_branch(self, objective: str, branch_name: str) -> Dict[str, Any]:
        """
        Simulates and projects metrics for a specific future execution branch.
        """
        # Baseline deterministic modifiers based on branch strategy
        if branch_name == "Plan A":  # Fast but unstable / risky
            success_probability = 0.65
            stability_index = 0.40
            speed_rating = 0.95
            cost_score = 0.30
            risk_coefficient = 0.85
            nodes = ["StrategyHouse", "EngineeringHouse"]
            edges = [("StrategyHouse", "EngineeringHouse")]
        elif branch_name == "Plan B":  # Balanced, stable but expensive
            success_probability = 0.90
            stability_index = 0.85
            speed_rating = 0.70
            cost_score = 0.80
            risk_coefficient = 0.25
            nodes = ["StrategyHouse", "SecurityHouse", "EngineeringHouse", "MemoryHouse"]
            edges = [
                ("StrategyHouse", "SecurityHouse"),
                ("SecurityHouse", "EngineeringHouse"),
                ("EngineeringHouse", "MemoryHouse")
            ]
        else:  # Plan C: Slow but highly scalable
            success_probability = 0.85
            stability_index = 0.90
            speed_rating = 0.45
            cost_score = 0.50
            risk_coefficient = 0.30
            nodes = ["StrategyHouse", "ResearchHouse", "LogicHouse", "EngineeringHouse", "EthicsGovernanceHouse"]
            edges = [
                ("StrategyHouse", "ResearchHouse"),
                ("ResearchHouse", "LogicHouse"),
                ("LogicHouse", "EngineeringHouse"),
                ("EngineeringHouse", "EthicsGovernanceHouse")
            ]

        # Topology projection format
        topology_projection = {
            "nodes": [{"id": n, "label": n} for n in nodes],
            "edges": [{"source": u, "target": v} for u, v in edges]
        }

        projection = {
            "id": f"sim_{branch_name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}",
            "branch_name": branch_name,
            "success_probability": success_probability,
            "stability_index": stability_index,
            "speed_rating": speed_rating,
            "cost_score": cost_score,
            "risk_coefficient": risk_coefficient,
            "topology_projection": topology_projection
        }
        return projection

    async def generate_scenarios(self, objective_id: str, objective: str) -> List[Dict[str, Any]]:
        """
        Generates and persists Plan A, B, and C scenario branches for an objective.
        """
        branches = ["Plan A", "Plan B", "Plan C"]
        results = []
        
        async with schemas.async_session() as session:
            for branch in branches:
                proj = await self.project_branch(objective, branch)
                
                db_scenario = SQLSimulationScenario(
                    id=proj["id"],
                    objective_id=objective_id,
                    branch_name=proj["branch_name"],
                    success_probability=proj["success_probability"],
                    stability_index=proj["stability_index"],
                    speed_rating=proj["speed_rating"],
                    cost_score=proj["cost_score"],
                    risk_coefficient=proj["risk_coefficient"],
                    topology_projection=proj["topology_projection"],
                    created_at=datetime.utcnow()
                )
                session.add(db_scenario)
                
                # Append to results for easy cognitive engine consumption
                proj["objective_id"] = objective_id
                results.append(proj)
                
            await session.commit()
            
        logger.info(f"🌳 [SCENARIO TREE GENERATED] 3 execution branches projected for objective_id {objective_id}")
        return results

# Global Simulation House Service instance
simulation_house = SimulationHouseService()
