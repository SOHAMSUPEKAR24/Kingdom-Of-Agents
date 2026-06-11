import logging
from typing import Dict, Any, List
from pydantic import BaseModel

logger = logging.getLogger("antigravity.constitution")

class Rule(BaseModel):
    id: str
    title: str
    description: str
    immutable: bool
    enabled: bool

class Constitution:
    # Immutable Core Rules of the Kingdom
    IMMUTABLE_RULES: List[Rule] = [
        Rule(
            id="CONST-I",
            title="Preserve King Authority",
            description="The King is the ultimate authority. No agent or sub-system shall ever override, manipulate, conceal actions from, or bypass the King's governing rules.",
            immutable=True,
            enabled=True
        ),
        Rule(
            id="CONST-II",
            title="Zero Privilege Escalation",
            description="Agents must run in sandboxed environments with strict RBAC permission models. Autonomous privilege escalation is strictly prohibited.",
            immutable=True,
            enabled=True
        ),
        Rule(
            id="CONST-III",
            title="Mandatory Town Hall Audit",
            description="No output can be stored in the Memory Crypt or executed in the physical world without receiving full consensus and consistency validation at a Town Hall.",
            immutable=True,
            enabled=True
        ),
        Rule(
            id="CONST-IV",
            title="Controlled Spawning Boundaries",
            description="Soldiers are disposable worker tasks. The Knight or Houses must never self-replicate uncontrollably or exceed spawning thresholds (max active nodes).",
            immutable=True,
            enabled=True
        ),
        Rule(
            id="CONST-V",
            title="No Illegal or Destructive Acts",
            description="Under no circumstances may the system perform destructive terminal operations, access unauthorized networks, or bypass legal bounds.",
            immutable=True,
            enabled=True
        )
    ]

    def __init__(self, redis_client=None):
        self.redis = redis_client
        # Default discretionary permissions
        self._discretionary_cache = {
            "allow_autonomous_soldier_replication": True,
            "allow_self_learning_prompt_evolution": True,
            "allow_autonomous_infrastructure_scale": False,
            "allow_external_internet_access": True
        }

    async def get_discretionary_permissions(self) -> Dict[str, bool]:
        if not self.redis:
            return self._discretionary_cache
        try:
            stored = await self.redis.hgetall("kingdom:governance:permissions")
            if not stored:
                # Initialize
                serialized = {k: "true" if v else "false" for k, v in self._discretionary_cache.items()}
                await self.redis.hset("kingdom:governance:permissions", mapping=serialized)
                return self._discretionary_cache
            return {k.decode("utf-8"): v.decode("utf-8") == "true" for k, v in stored.items()}
        except Exception as e:
            logger.error(f"Error fetching discretionary rules: {e}")
            return self._discretionary_cache

    async def update_discretionary_permission(self, key: str, value: bool) -> bool:
        if key not in self._discretionary_cache:
            raise ValueError(f"Unknown discretionary permission: {key}")
        self._discretionary_cache[key] = value
        if self.redis:
            try:
                await self.redis.hset("kingdom:governance:permissions", key, "true" if value else "false")
                return True
            except Exception as e:
                logger.error(f"Error writing discretionary rules: {e}")
                return False
        return True

    def validate_action(self, action_type: str, payload: Dict[str, Any]) -> bool:
        """
        Validates if an action violates the absolute core rules.
        """
        # Rule V check: Unsafe commands
        if action_type == "execute_command":
            cmd = payload.get("command", "").strip()
            # Banned keywords that violate safety parameters
            banned_keywords = ["rm -rf /", "mkfs", "dd if=", "shutdown", "reboot", ":(){ :|:& };:"]
            for keyword in banned_keywords:
                if keyword in cmd:
                    logger.critical(f"CONSTITUTIONAL VIOLATION [CONST-V]: Unsafe command detected: '{cmd}'")
                    return False
        
        # Rule IV check: Spawning thresholds
        if action_type == "spawn_soldier":
            active_count = payload.get("active_soldiers_count", 0)
            max_limit = payload.get("max_limit", 50)
            if active_count >= max_limit:
                logger.warning(f"CONSTITUTIONAL WARNING [CONST-IV]: Spawning blocked. Soldier count ({active_count}) exceeds limit ({max_limit})")
                return False

        logger.info(f"Constitutional compliance audit passed for action '{action_type}'")
        return True

constitution = Constitution()
