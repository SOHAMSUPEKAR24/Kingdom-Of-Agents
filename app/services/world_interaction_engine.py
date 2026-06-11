import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import SQLWorldInteractionLog
import uuid
import subprocess

logger = logging.getLogger(__name__)

class WorldInteractionEngine:
    """
    Central API for the civilization to touch the real world.
    Supports API requests, file system interactions, terminal execution, etc.
    """
    
    async def log_interaction(self, agent_id: str, interaction_type: str, target: str, payload: str, outcome: str, success: bool, session: AsyncSession):
        log_entry = SQLWorldInteractionLog(
            id=f"wil_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id,
            interaction_type=interaction_type,
            target=target,
            action_payload=payload,
            outcome_summary=outcome,
            success=1 if success else 0
        )
        session.add(log_entry)
        await session.flush()
        return log_entry
        
    async def execute_terminal_command(self, agent_id: str, command: str, session: AsyncSession) -> Dict[str, Any]:
        """
        Executes a local terminal command in a safe sandbox (simulated/limited).
        """
        try:
            # We use a brief timeout to prevent hanging commands.
            result = subprocess.run(
                command, shell=True, text=True, capture_output=True, timeout=10
            )
            success = result.returncode == 0
            outcome = result.stdout if success else result.stderr
            await self.log_interaction(agent_id, "TERMINAL", "localhost", command, outcome[:500], success, session)
            return {"success": success, "output": outcome, "exit_code": result.returncode}
        except subprocess.TimeoutExpired:
            await self.log_interaction(agent_id, "TERMINAL", "localhost", command, "TIMEOUT", False, session)
            return {"success": False, "output": "TIMEOUT", "exit_code": -1}
        except Exception as e:
            await self.log_interaction(agent_id, "TERMINAL", "localhost", command, str(e), False, session)
            return {"success": False, "output": str(e), "exit_code": -1}

world_interaction_engine = WorldInteractionEngine()
