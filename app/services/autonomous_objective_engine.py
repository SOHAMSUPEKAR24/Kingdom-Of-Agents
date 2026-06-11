import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import SQLAutonomousObjective

class AutonomousObjectiveEngine:
    def __init__(self):
        self.name = "AUTONOMOUS_OBJECTIVE_ENGINE"
        self.version = "1.0.0"

    async def generate_objective(self, origin_source: str, priority_score: float, db_session: AsyncSession):
        """
        Creates an internal autonomous objective for the civilization to execute.
        """
        obj_id = f"AUTO-OBJ-{uuid.uuid4().hex[:8]}"
        objective = SQLAutonomousObjective(
            id=obj_id,
            title=f"Autonomous Goal from {origin_source}",
            description="Self-generated objective based on discovered strategic needs.",
            priority_score=priority_score,
            origin_source=origin_source,
            status="PROPOSED"
        )
        db_session.add(objective)
        return objective

autonomous_objective_engine = AutonomousObjectiveEngine()
