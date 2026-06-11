import asyncio
import logging
from typing import Dict, Any

from app.core.event_bus import event_bus, Event
from app.agents.factory import agent_factory
from app.services.memory_service import memory_service

logger = logging.getLogger("antigravity.houses")

class BaseHouse:
    def __init__(self, house_name: str, soldier_role: str):
        self.house_name = house_name
        self.soldier_role = soldier_role

    async def initialize(self):
        """Registers the House listener to the Event Bus."""
        event_bus.subscribe("TASK_ASSIGNED", self.on_task_assigned)
        logger.info(f"🏡 [{self.house_name}] Activated and listening for task assignments.")

    async def on_task_assigned(self, event: Event):
        task_data = event.payload.get("task")
        if not task_data:
            return

        assigned_house = task_data.get("assigned_house")
        if assigned_house != self.house_name:
            # Not our department!
            return

        task_id = task_data.get("id")
        logger.info(f"📥 [{self.house_name} ASSIGNED] Undergoing task {task_id}: '{task_data.get('title')}'")
        await memory_service.store_log(task_id, self.house_name, f"House accepting task: {task_data.get('title')}", "INFO")

        # 1. Update task relational state to running
        try:
            # 2. Spawn a specialized disposable Soldier agent
            soldier_role = task_data.get("input_data", {}).get("assigned_role", self.soldier_role)
            soldier = await agent_factory.spawn_soldier(
                role=soldier_role,
                house=self.house_name,
                task_title=task_data.get("title", "")
            )

            # Store the agent_id inside task_data's active context so Town Hall can track it
            task_data["agent_id"] = soldier.agent_id
            task_data["assigned_soldier"] = soldier.agent_id

            # 3. Execute the task logic via the spawned worker Soldier
            output = await soldier.execute(task_data.get("input_data", {}))
            
            # 4. Trigger Town Hall Validation (CONST-III compliance)
            validation_payload = {
                "task": task_data,
                "output_data": output,
                "verified_by_house": self.house_name
            }
            validation_event = Event(
                event_type="VALIDATION_REQUIRED",
                sender=self.house_name,
                payload=validation_payload
            )
            await event_bus.publish(validation_event)
            await memory_service.store_log(task_id, self.house_name, "Task output sent to Town Hall for compliance verification", "INFO")
            
        except Exception as e:
            logger.error(f"❌ [{self.house_name} EXECUTION FAILED] Task {task_id} aborted: {e}")
            await memory_service.store_log(task_id, self.house_name, f"Execution failure: {str(e)}", "ERROR")
            
            # Publish failure event so Knight-0 can handle cascade recovery
            fail_event = Event(
                event_type="TASK_FAILED",
                sender=self.house_name,
                payload={"task": task_data, "error": str(e)}
            )
            await event_bus.publish(fail_event)

# ==========================================
# DOMAIN-SPECIFIC HOUSE IMPLEMENTATIONS
# ==========================================

class StrategyHouse(BaseHouse):
    def __init__(self):
        super().__init__("StrategyHouse", "StrategySoldier")


class ResearchHouse(BaseHouse):
    def __init__(self):
        super().__init__("ResearchHouse", "ResearchSoldier")


class EngineeringHouse(BaseHouse):
    def __init__(self):
        super().__init__("EngineeringHouse", "CodeSoldier")


class SecurityHouse(BaseHouse):
    def __init__(self):
        super().__init__("SecurityHouse", "SecuritySoldier")


class MemoryHouse(BaseHouse):
    def __init__(self):
        super().__init__("MemoryHouse", "MemorySoldier")


class LogicHouse(BaseHouse):
    def __init__(self):
        super().__init__("LogicHouse", "LogicSoldier")


class ChaosHouse(BaseHouse):
    def __init__(self):
        super().__init__("ChaosHouse", "ChaosSoldier")


class SkepticHouse(BaseHouse):
    def __init__(self):
        super().__init__("SkepticHouse", "SkepticSoldier")


class SimulationHouse(BaseHouse):
    def __init__(self):
        super().__init__("SimulationHouse", "SimulationSoldier")


class EconomicHouse(BaseHouse):
    def __init__(self):
        super().__init__("EconomicHouse", "EconomicSoldier")


class EvolutionHouse(BaseHouse):
    def __init__(self):
        super().__init__("EvolutionHouse", "EvolutionSoldier")


class EthicsGovernanceHouse(BaseHouse):
    def __init__(self):
        super().__init__("EthicsGovernanceHouse", "EthicsGovernanceSoldier")


class ScientificDiscoveryHouse(BaseHouse):
    def __init__(self):
        super().__init__("ScientificDiscoveryHouse", "DiscoverySoldier")


class CausalAnalysisHouse(BaseHouse):
    def __init__(self):
        super().__init__("CausalAnalysisHouse", "CausalSoldier")


class SimulationResearchHouse(BaseHouse):
    def __init__(self):
        super().__init__("SimulationResearchHouse", "SimulationResearchSoldier")


class TheoryValidationHouse(BaseHouse):
    def __init__(self):
        super().__init__("TheoryValidationHouse", "TheorySoldier")


class UncertaintyReasoningHouse(BaseHouse):
    def __init__(self):
        super().__init__("UncertaintyReasoningHouse", "UncertaintySoldier")


class InfrastructureScienceHouse(BaseHouse):
    def __init__(self):
        super().__init__("InfrastructureScienceHouse", "InfraScienceSoldier")


class StrategicForecastingHouse(BaseHouse):
    def __init__(self):
        super().__init__("StrategicForecastingHouse", "StrategicForecastingSoldier")


class AbstractionSynthesisHouse(BaseHouse):
    def __init__(self):
        super().__init__("AbstractionSynthesisHouse", "AbstractionSoldier")

# ==========================================
# INITIALIZATION INTERFACE
# ==========================================

# Active House registry
houses_registry: Dict[str, BaseHouse] = {
    "StrategyHouse": StrategyHouse(),
    "ResearchHouse": ResearchHouse(),
    "EngineeringHouse": EngineeringHouse(),
    "SecurityHouse": SecurityHouse(),
    "MemoryHouse": MemoryHouse(),
    "LogicHouse": LogicHouse(),
    "ChaosHouse": ChaosHouse(),
    "SkepticHouse": SkepticHouse(),
    "SimulationHouse": SimulationHouse(),
    "EconomicHouse": EconomicHouse(),
    "EvolutionHouse": EvolutionHouse(),
    "EthicsGovernanceHouse": EthicsGovernanceHouse(),
    "ScientificDiscoveryHouse": ScientificDiscoveryHouse(),
    "CausalAnalysisHouse": CausalAnalysisHouse(),
    "SimulationResearchHouse": SimulationResearchHouse(),
    "TheoryValidationHouse": TheoryValidationHouse(),
    "UncertaintyReasoningHouse": UncertaintyReasoningHouse(),
    "InfrastructureScienceHouse": InfrastructureScienceHouse(),
    "StrategicForecastingHouse": StrategicForecastingHouse(),
    "AbstractionSynthesisHouse": AbstractionSynthesisHouse()
}

async def initialize_houses():
    """Boots all system Houses, connecting event subscribers."""
    for house in houses_registry.values():
        await house.initialize()
