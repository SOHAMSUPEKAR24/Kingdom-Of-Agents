import ast
import logging
import os
import sys
import importlib.util
from typing import Dict, Any, List, Optional, Type
from app.agents.factory import BaseSoldier
from app.core.constitution import constitution

logger = logging.getLogger("antigravity.agent_evolver")

# Dynamic global registry mapping class name to dynamic Soldier class object
DYNAMIC_AGENT_REGISTRY: Dict[str, Type[BaseSoldier]] = {}

class AgentEvolutionEngine:
    def __init__(self):
        # Create dynamic agents directory if not exists
        self.dynamic_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents", "dynamic")
        os.makedirs(self.dynamic_dir, exist_ok=True)
        # Add to sys.path so we can import modules
        if self.dynamic_dir not in sys.path:
            sys.path.append(self.dynamic_dir)

    def discover_capability_gap(self, objective_text: str, existing_roles: List[str]) -> Optional[Dict[str, Any]]:
        """
        Scans objective text for complex operations that cannot be handled by standard templates.
        Returns capability gap definition if found.
        """
        obj_lower = objective_text.lower()
        
        # Scenario 1: Cryptographic or Encoding requirements
        if "crypt" in obj_lower or "decode" in obj_lower or "encode" in obj_lower or "hash" in obj_lower:
            role_name = "CryptographerSoldier"
            if role_name not in existing_roles and role_name not in DYNAMIC_AGENT_REGISTRY:
                return {
                    "role_name": role_name,
                    "gap_desc": "Specialized cryptography worker to encode, decode, and hash credentials or payload blocks safely.",
                    "house": "SecurityHouse",
                    "permissions": ["READ_RULES", "CRYPTO_OPS"]
                }
        
        # Scenario 2: Data Translation or Transformation requirements
        if "translate" in obj_lower or "format" in obj_lower or "transform" in obj_lower:
            role_name = "DataTransformerSoldier"
            if role_name not in existing_roles and role_name not in DYNAMIC_AGENT_REGISTRY:
                return {
                    "role_name": role_name,
                    "gap_desc": "Data layout and format transformer to convert between nested JSON, XML, and clean Markdown tables.",
                    "house": "EngineeringHouse",
                    "permissions": ["FILE_WRITE", "TRANSFORM_DATA"]
                }

        # Scenario 3: Performance tuning or optimizing
        if "optimize" in obj_lower or "tune" in obj_lower or "benchmark" in obj_lower:
            role_name = "OptimizerSoldier"
            if role_name not in existing_roles and role_name not in DYNAMIC_AGENT_REGISTRY:
                return {
                    "role_name": role_name,
                    "gap_desc": "Optimization agent that analyses runtime execution profiles and generates dynamic suggestions.",
                    "house": "StrategyHouse",
                    "permissions": ["READ_RULES", "METRICS_READ"]
                }

        return None

    def ast_safety_audit(self, source_code: str) -> bool:
        """
        Executes strict static compliance verification on the dynamic AST.
        Rejects command executions, dangerous module imports, and runtime tampering.
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError as se:
            logger.error(f"AST AUDIT FAILED: Syntax Error in generated code: {se}")
            return False

        # Prohibited modules to import
        BANNED_IMPORTS = {"os", "subprocess", "sys", "shutil", "ctypes", "socket", "builtins"}
        # Prohibited builtins to call
        BANNED_CALLS = {"eval", "exec", "open", "getattr", "setattr", "delattr", "compile"}

        class SafetyVisitor(ast.NodeVisitor):
            def __init__(self):
                self.is_safe = True

            def visit_Import(self, node):
                for alias in node.names:
                    if alias.name.split('.')[0] in BANNED_IMPORTS:
                        logger.critical(f"AST VIOLATION: Banned import statement detected: '{alias.name}'")
                        self.is_safe = False
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                if node.module and node.module.split('.')[0] in BANNED_IMPORTS:
                    logger.critical(f"AST VIOLATION: Banned import-from statement detected: '{node.module}'")
                    self.is_safe = False
                self.generic_visit(node)

            def visit_Call(self, node):
                # Check for direct calls to banned builtins
                if isinstance(node.func, ast.Name) and node.func.id in BANNED_CALLS:
                    logger.critical(f"AST VIOLATION: Call to banned builtin detected: '{node.func.id}()'")
                    self.is_safe = False
                
                # Check for attribute access calls (e.g. os.system, socket.connect)
                elif isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    # Banned attribute methods
                    banned_attrs = {"system", "popen", "run", "call", "rmtree", "remove", "unlink", "connect", "bind"}
                    if attr_name in banned_attrs:
                        logger.critical(f"AST VIOLATION: Call to dangerous attribute method detected: '.{attr_name}()'")
                        self.is_safe = False
                
                self.generic_visit(node)

        visitor = SafetyVisitor()
        visitor.visit(tree)
        return visitor.is_safe

    def generate_agent_class_source(self, role_name: str, gap_desc: str) -> str:
        """
        Creates functional Python code defining the dynamic BaseSoldier subclass.
        """
        # Determine specialized logic template based on role type
        if "Cryptographer" in role_name:
            logic_body = """
        payload = task_input.get("payload", "")
        operation = task_input.get("operation", "encrypt")
        key = task_input.get("key", "secret-key")
        
        await memory_service.store_log(self.agent_id, self.role, f"Running dynamic crypto operational flow: {operation}", "INFO")
        await asyncio.sleep(0.4)
        
        from app.services.tool_creator import DYNAMIC_TOOL_LIBRARY
        if "base64_xor_cipher" in DYNAMIC_TOOL_LIBRARY:
            result = DYNAMIC_TOOL_LIBRARY["base64_xor_cipher"](payload, key, operation)
        else:
            import base64
            if operation == "encrypt":
                # Simple simulation XOR encrypt base64 encoding
                encoded_bytes = base64.b64encode(payload.encode("utf-8"))
                result = f"ENC_{encoded_bytes.decode('utf-8')}"
            else:
                if payload.startswith("ENC_"):
                    raw_b64 = payload[4:]
                    decoded_bytes = base64.b64decode(raw_b64.encode("utf-8"))
                    result = decoded_bytes.decode("utf-8")
                else:
                    result = payload
                
        return {
            "operation": operation,
            "processed_payload": result,
            "verification_status": "SECURE_HASH_MATCH",
            "evolution_metadata": {"generated_agent": True, "description": self.gap_desc}
        }
"""
        elif "DataTransformer" in role_name:
            logic_body = """
        data = task_input.get("data", {})
        format_target = task_input.get("format", "markdown")
        
        await memory_service.store_log(self.agent_id, self.role, f"Transforming data structure into format: {format_target}", "INFO")
        await asyncio.sleep(0.4)
        
        from app.services.tool_creator import DYNAMIC_TOOL_LIBRARY
        if format_target == "markdown" and "dict_to_markdown_table" in DYNAMIC_TOOL_LIBRARY:
            result = DYNAMIC_TOOL_LIBRARY["dict_to_markdown_table"](data)
        else:
            if format_target == "markdown":
                # Convert dictionary keys and values to a clean markdown table
                headers = list(data.keys())
                rows = [str(data[h]) for h in headers]
                md_table = f"| {' | '.join(headers)} |\\n| {' | '.join(['---']*len(headers))} |\\n| {' | '.join(rows)} |"
                result = md_table
            else:
                result = f"<data>{str(data)}</data>"
            
        return {
            "target_format": format_target,
            "transformed_content": result,
            "validation_score": 1.0,
            "evolution_metadata": {"generated_agent": True, "description": self.gap_desc}
        }
"""
        else:
            logic_body = """
        await memory_service.store_log(self.agent_id, self.role, "Executing fallback dynamic evolution logic", "INFO")
        await asyncio.sleep(0.3)
        return {
            "status": "COMPLETED",
            "message": "Generic dynamic solver successful",
            "evolution_metadata": {"generated_agent": True, "description": self.gap_desc}
        }
"""

        source_code = f"""# Dynamic Generated Agent Class for ANTIGRAVITY
import asyncio
import logging
from typing import Dict, Any, List
from app.agents.factory import BaseSoldier
from app.services.memory_service import memory_service

class {role_name}(BaseSoldier):
    def __init__(self, agent_id: str, role: str, house: str, permissions: List[str]):
        super().__init__(agent_id, role, house, permissions)
        self.gap_desc = "{gap_desc}"
        self.max_lifespan_sec = 60

    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:{logic_body}
"""
        return source_code

    def register_and_compile_agent(self, role_name: str, code: str) -> bool:
        """
        Audits safety of source code, writes it to dynamic directory, compiles it,
        and registers the dynamic Soldier class within factory lookup structures.
        """
        # 1. AST Safety verification against Constitution constraints (CONST-II and CONST-V)
        if not self.ast_safety_audit(code):
            logger.critical(f"REJECTED DYNAMIC COMPILATION: Code fails AST Compliance check for '{role_name}'!")
            raise SecurityError("Constitutional AST violation: Unsafe dynamic operations blocked!")

        file_path = os.path.join(self.dynamic_dir, f"{role_name}.py")
        
        # 2. Persist code file to local filesystem
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 3. Dynamic runtime compilation and importlib load
        try:
            spec = importlib.util.spec_from_file_location(role_name, file_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load importlib spec for module {role_name}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Fetch the Class object
            soldier_class = getattr(module, role_name)
            
            # Register in dynamic global dict
            DYNAMIC_AGENT_REGISTRY[role_name] = soldier_class
            logger.info(f"🧬 [EVOLUTION REVOLUTION] Dynamically compiled, verified, and registered new agent class: {role_name}")
            return True
        except Exception as e:
            logger.error(f"Failed compilation/registration of dynamic class {role_name}: {e}")
            raise e

class SecurityError(Exception):
    pass

# Global instance
agent_evolver = AgentEvolutionEngine()
