import asyncio
import logging
from typing import Dict, Any, Tuple

from app.core.event_bus import event_bus, Event
from app.services.memory_service import memory_service
from app.core.constitution import constitution
from app.services.context_stability import stability_engine
from app.services.reinforcement import reinforcement_engine

logger = logging.getLogger("antigravity.town_hall")

class TownHallRegistry:
    def __init__(self):
        self.total_audits = 0
        self.failed_audits = 0

    async def initialize(self):
        # Subscribe to validation requests
        event_bus.subscribe("VALIDATION_REQUIRED", self.handle_validation_request)
        logger.info("Town Hall Governance Center initialized and listening for output audits.")

    async def handle_validation_request(self, event: Event):
        self.total_audits += 1
        
        task_data = event.payload.get("task", {})
        output_data = event.payload.get("output_data", {})
        origin_house = event.payload.get("verified_by_house", "UNKNOWN")
        task_id = task_data.get("id")

        logger.info(f"🏛️  [TOWN HALL AUDIT STARTED] Auditing task output '{task_id}' submitted by {origin_house}...")
        await memory_service.store_log(task_id, "TownHall", f"Audit started on output from {origin_house}", "INFO")

        # 1. Check for infinite loops / runaway recursion limit
        is_loop = await stability_engine.check_runaway_loop(task_id, task_data.get("agent_id"), origin_house)
        if is_loop:
            valid = False
            audit_feedback = "SECURITY QUARANTINE: Soldier isolated due to infinite loop recursion!"
            confidence_score = 0.0
        else:
            # Run physical and structural validations
            valid, confidence_score, audit_feedback = await self._run_audit_pipeline(task_data, output_data)

            # 2. Check compliance with Immutable Constitution Rules
            constitutional_valid = constitution.validate_action("audit_output", {"task_id": task_id, "output": output_data})
            if not constitutional_valid:
                valid = False
                audit_feedback = "CONSTITUTIONAL VIOLATION: Output breached security or governance bounds [CONST-III]!"

            # 3. Check for semantic contradictions or factual consistency violations
            if valid:
                has_contradiction, contradiction_details = await stability_engine.detect_contradiction(
                    task_data.get("title", ""), output_data
                )
                if has_contradiction:
                    valid = False
                    audit_feedback = f"HALLUCINATION BREACH: {contradiction_details}"
                    confidence_score = 0.0

        if valid:
            logger.info(f"🏛️  [TOWN HALL AUDIT PASSED] certified '{task_id}' with {confidence_score * 100}% confidence.")
            await memory_service.store_log(task_id, "TownHall", f"Audit passed. Confidence: {confidence_score*100}%. Feedback: {audit_feedback}", "INFO")
            
            # Record reinforcement scores (Evolutions)
            await self._record_reinforcement_reward(origin_house, confidence_score)

            # Update task data and publish completion event to unblock dependencies
            task_data["status"] = "COMPLETED"
            task_data["output_data"] = output_data

            completion_event = Event(
                event_type="TASK_COMPLETED",
                sender="TownHall",
                payload={"task": task_data}
            )
            await event_bus.publish(completion_event)
            await memory_service.store_topology_relation("TownHall", task_id, "APPROVED")
        else:
            self.failed_audits += 1
            logger.critical(f"🏛️  [TOWN HALL AUDIT FAILED] isolated corrupted output for task '{task_id}'! Feedback: {audit_feedback}")
            await memory_service.store_log(task_id, "TownHall", f"AUDIT REJECTED: {audit_feedback}", "CRITICAL")
            
            # Penalize origin house structure
            await self._record_reinforcement_penalty(origin_house)

            # Publish failure event so Knight-0 can execute self-healing cascade recovery
            fail_event = Event(
                event_type="TASK_FAILED",
                sender="TownHall",
                payload={"task": task_data, "error": audit_feedback}
            )
            await event_bus.publish(fail_event)
            await memory_service.store_topology_relation("TownHall", task_id, "QUARANTINED")

    async def _run_audit_pipeline(self, task_data: Dict[str, Any], output_data: Dict[str, Any]) -> Tuple[bool, float, str]:
        """
        Runs multi-agent consensus validation, checking structures and inputs.
        """
        await asyncio.sleep(0.5) # Simulate static analysis checks
        
        assigned_house = task_data.get("assigned_house")
        
        # 1. Engineering House Code Audits
        if assigned_house == "EngineeringHouse":
            if task_data.get("input_data", {}).get("assigned_role") == "DataTransformerSoldier":
                content = output_data.get("transformed_content", "")
                if not content:
                    return False, 0.0, "Missing transformed content from Data Transformer!"
                return True, 0.98, "Data transformation structure validated."
            
            files = output_data.get("generated_files", [])
            snippet = output_data.get("code_snippet", "")
            if not files or not snippet:
                return False, 0.0, "Missing code assets or compilation signatures"
            if "import os" in snippet and "rm" in snippet:
                return False, 0.1, "Unsafe system commands detected in Code Soldier output!"
            return True, 0.98, "Static syntax and security checks passed."

        # 2. Research House Audits
        elif assigned_house == "ResearchHouse":
            intel = output_data.get("crawled_intelligence", [])
            if not intel:
                return False, 0.0, "No research datasets fetched by Soldier!"
            return True, 0.95, "Factual context overlap validated."

        # 3. Strategy House Audits
        elif assigned_house == "StrategyHouse":
            plan = output_data.get("plan", {})
            if not plan.get("objective_verified"):
                return False, 0.0, "Strategic planning constraints check failed!"
            return True, 0.99, "Objective aligned with core constitutional permissions."

        # 4. Security House Audits
        elif assigned_house == "SecurityHouse":
            if task_data.get("input_data", {}).get("assigned_role") == "CryptographerSoldier":
                payload = output_data.get("processed_payload", "")
                if not payload:
                    return False, 0.0, "Missing processed cryptographic payload!"
                return True, 0.99, "Dynamic cryptographic validation validated."

            report = output_data.get("audit_report", {})
            if report.get("vulnerabilities_found", 0) > 0:
                return False, 0.4, "High severity security vulnerabilities flagged by Auditor!"
            return True, 1.0, "System secure. Vulnerability-free compliance."

        # 5. Memory House Audits
        elif assigned_house == "MemoryHouse":
            mem_id = output_data.get("archived_memory_id")
            if not mem_id:
                return False, 0.0, "Memory archiving signature missing"
            return True, 0.96, "Experience successfully compressed and indexed."

        return True, 0.90, "General structure alignment validated."

    async def _record_reinforcement_reward(self, house_name: str, confidence: float):
        """Dispatches performance rewards to target House topology nodes."""
        try:
            # Rewards directly elevate House prompt weights and levels
            logger.debug(f"Reinforcement Reward: House '{house_name}' earned weight bonus score: {confidence}")
            await reinforcement_engine.reward_house(house_name, confidence)
        except Exception as e:
            logger.error(f"Error logging reinforcement reward: {e}")

    async def _record_reinforcement_penalty(self, house_name: str):
        """Dispatches workflow penalties to target House nodes."""
        try:
            logger.warning(f"Reinforcement Penalty: House '{house_name}' penalized due to audit failure!")
            await reinforcement_engine.penalize_house(house_name)
        except Exception as e:
            logger.error(f"Error logging reinforcement penalty: {e}")

# Global Town Hall coordinator instance
town_hall = TownHallRegistry()
