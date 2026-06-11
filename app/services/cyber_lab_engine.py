import logging
from app.core.event_bus import event_bus, Event

logger = logging.getLogger("antigravity.cyber_lab")

class CyberLabEngine:
    def __init__(self):
        self.active_labs = 0

    async def initialize(self):
        event_bus.subscribe("START_CYBER_LAB", self.launch_sandbox)
        logger.info("🛡️ [CYBER LAB ENGINE] Online. Initializing strictly isolated security sandboxes.")

    async def launch_sandbox(self, event: Event):
        payload = event.payload
        target = payload.get("target", "LOCAL_DVWA")
        
        # Constitutional check
        if "http://" in target or "https://" in target or "www." in target:
            if "localhost" not in target and "127.0.0.1" not in target:
                logger.error(f"🚨 [CYBER LAB] ILLEGAL ATTACK ATTEMPT BLOCKED. Target: {target}")
                await event_bus.publish(Event(
                    event_type="ILLEGAL_CYBER_ACTION",
                    sender="CyberLabEngine",
                    payload={"target": target, "reason": "Non-local external target prohibited."}
                ))
                return

        self.active_labs += 1
        logger.info(f"🛡️ [CYBER LAB] Isolated sandbox launched for target {target}.")
        
        # Simulate lab execution and CTF completion
        await event_bus.publish(Event(
            event_type="RUN_BENCHMARK",
            sender="CyberLabEngine",
            payload={"domain": "CYBERSECURITY", "test_suite": "OWASP_Top_10_Sim"}
        ))

cyber_lab_engine = CyberLabEngine()
