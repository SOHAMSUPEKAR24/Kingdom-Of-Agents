import ast
import logging
import os
import sys
import importlib.util
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime
from sqlalchemy import select, update

from app.models import schemas
from app.models.schemas import SQLToolVersion, ToolVersionSchema
from app.services.memory_service import memory_service

logger = logging.getLogger("antigravity.tool_creator")

# Global register for dynamically created tools
DYNAMIC_TOOL_LIBRARY: Dict[str, Callable] = {}

class ToolCreatorEngine:
    def __init__(self):
        # Create dynamic tools directory if not exists
        self.tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "dynamic_tools")
        os.makedirs(self.tools_dir, exist_ok=True)
        if self.tools_dir not in sys.path:
            sys.path.append(self.tools_dir)

    def discover_tool_gap(self, task_title: str, required_tool: str) -> Optional[Dict[str, Any]]:
        """
        Identifies if a task needs a tool that is currently missing from the library.
        """
        req_lower = required_tool.lower()
        if "base64" in req_lower or "xor" in req_lower:
            return {
                "tool_name": "base64_xor_cipher",
                "description": "XOR crypt and base64 encodes/decodes text with a key.",
                "params": ["payload", "key", "operation"]
            }
        elif "convert" in req_lower or "markdown" in req_lower:
            return {
                "tool_name": "dict_to_markdown_table",
                "description": "Converts dictionaries or nested JSON items to beautiful markdown table syntax.",
                "params": ["data"]
            }
        return None

    def ast_safety_audit(self, source_code: str) -> bool:
        """
        Audits tool code to prevent side effects, unauthorized file access, or command shell injections.
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError as se:
            logger.error(f"TOOL AST AUDIT FAILED: Syntax error: {se}")
            return False

        BANNED_IMPORTS = {"os", "subprocess", "sys", "shutil", "ctypes", "socket", "builtins"}
        BANNED_CALLS = {"eval", "exec", "open", "getattr", "setattr", "compile"}

        class ToolSafetyVisitor(ast.NodeVisitor):
            def __init__(self):
                self.is_safe = True

            def visit_Import(self, node):
                for alias in node.names:
                    if alias.name.split('.')[0] in BANNED_IMPORTS:
                        logger.critical(f"TOOL AST VIOLATION: Dangerous import '{alias.name}' blocked.")
                        self.is_safe = False
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                if node.module and node.module.split('.')[0] in BANNED_IMPORTS:
                    logger.critical(f"TOOL AST VIOLATION: Dangerous import-from '{node.module}' blocked.")
                    self.is_safe = False
                self.generic_visit(node)

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id in BANNED_CALLS:
                    logger.critical(f"TOOL AST VIOLATION: Builtin call '{node.func.id}()' blocked.")
                    self.is_safe = False
                self.generic_visit(node)

        visitor = ToolSafetyVisitor()
        visitor.visit(tree)
        return visitor.is_safe

    def generate_tool_source(self, tool_name: str, description: str) -> Tuple[str, str]:
        """
        Generates Python code for the function and a test script to validate its behavior.
        """
        if tool_name == "base64_xor_cipher":
            tool_code = """def base64_xor_cipher(payload: str, key: str = "key", operation: str = "encrypt") -> str:
    import base64
    # Simple XOR mapping
    key_bytes = key.encode('utf-8')
    payload_bytes = payload.encode('utf-8')
    xor_bytes = bytearray(len(payload_bytes))
    for i in range(len(payload_bytes)):
        xor_bytes[i] = payload_bytes[i] ^ key_bytes[i % len(key_bytes)]
        
    if operation == "encrypt":
        return base64.b64encode(xor_bytes).decode('utf-8')
    else:
        # Base64 decode, then decrypt (XOR is symmetric)
        decoded = base64.b64decode(payload.encode('utf-8'))
        decrypted_bytes = bytearray(len(decoded))
        for i in range(len(decoded)):
            decrypted_bytes[i] = decoded[i] ^ key_bytes[i % len(key_bytes)]
        return decrypted_bytes.decode('utf-8')
"""
            test_code = """def run_test():
    import base64
    secret = "KingdomOfBots_Verification"
    encrypted = base64_xor_cipher(secret, "antigravity", "encrypt")
    decrypted = base64_xor_cipher(encrypted, "antigravity", "decrypt")
    assert secret == decrypted, f"Decryption failed! Expected {secret}, got {decrypted}"
    return True
"""
        elif tool_name == "dict_to_markdown_table":
            tool_code = """def dict_to_markdown_table(data: dict) -> str:
    if not data:
        return ""
    headers = list(data.keys())
    values = [str(data[h]) for h in headers]
    
    header_row = "| " + " | ".join(headers) + " |\\n"
    divider_row = "| " + " | ".join(["---"] * len(headers)) + " |\\n"
    value_row = "| " + " | ".join(values) + " |"
    
    return header_row + divider_row + value_row
"""
            test_code = """def run_test():
    sample = {"A": 1, "B": 2}
    result = dict_to_markdown_table(sample)
    assert "| A | B |" in result, "Header check failed"
    assert "| 1 | 2 |" in result, "Values check failed"
    return True
"""
        else:
            tool_code = """def dynamic_fallback_tool(*args, **kwargs):
    return "SUCCESS"
"""
            test_code = """def run_test():
    assert dynamic_fallback_tool() == "SUCCESS"
    return True
"""
        return tool_code, test_code

    def test_tool_in_sandbox(self, tool_name: str, tool_code: str, test_code: str) -> bool:
        """
        Compiles the tool function and executes its unit test inside a safe in-memory scope.
        """
        # Audit tool safety first
        if not self.ast_safety_audit(tool_code) or not self.ast_safety_audit(test_code):
            logger.error("Sandbox Test Blocked: Safety violations detected in code AST.")
            return False

        try:
            # 1. Prepare sandboxed execution local workspace scope
            local_scope: Dict[str, Any] = {}
            # Compile tool code in local scope
            exec(tool_code, local_scope)
            
            # Fetch compiled function
            tool_fn = local_scope.get(tool_name)
            if not tool_fn:
                logger.error(f"Compilation failed: Function {tool_name} was not created.")
                return False

            # 2. Inject function into test workspace
            test_scope = {tool_name: tool_fn}
            # Compile test code
            exec(test_code, test_scope)
            
            # Run the test function
            run_test_fn = test_scope.get("run_test")
            if not run_test_fn:
                logger.error("Compilation failed: Test function 'run_test()' was not created.")
                return False
                
            test_success = run_test_fn()
            if test_success:
                logger.info(f"🧪 [SANDBOX TEST PASSED] Dynamic tool '{tool_name}' verified successfully.")
                return True
            return False
        except Exception as e:
            logger.critical(f"Sandbox test suite failed for {tool_name}: {e}")
            return False

    async def register_tool_to_library(self, tool_name: str, tool_code: str, parent_tool: Optional[str] = None, avg_latency: float = 0.0) -> bool:
        """
        Saves tool to dynamic folder, registers it in the relational table (with versioning),
        compiles it, and inserts it into DYNAMIC_TOOL_LIBRARY.
        """
        # 1. Determine next version number from previous database records
        version = "1.0"
        async with schemas.async_session() as session:
            stmt = select(SQLToolVersion).where(
                SQLToolVersion.name == tool_name
            ).order_by(SQLToolVersion.created_at.desc()).limit(1)
            
            res = await session.execute(stmt)
            latest = res.scalars().first()
            if latest:
                try:
                    v_float = float(latest.version)
                    version = f"{v_float + 0.1:.1f}"
                except ValueError:
                    version = "1.1"

        tool_version_id = f"{tool_name}_v{version}"
        version_suffix = version.replace(".", "_")

        # 2. Save both main code file and versioned file to the filesystem
        file_path_main = os.path.join(self.tools_dir, f"{tool_name}.py")
        file_path_ver = os.path.join(self.tools_dir, f"{tool_name}_v{version_suffix}.py")

        with open(file_path_main, "w", encoding="utf-8") as f:
            f.write(tool_code)
        with open(file_path_ver, "w", encoding="utf-8") as f:
            f.write(tool_code)

        # 3. Add record to SQL database
        async with schemas.async_session() as session:
            # First, retire previous versions of this tool
            stmt_retire = update(SQLToolVersion).where(
                SQLToolVersion.name == tool_name,
                SQLToolVersion.status == "ACTIVE"
            ).values(
                status="RETIRED",
                replaced_by=tool_version_id
            )
            await session.execute(stmt_retire)

            db_tool = SQLToolVersion(
                id=tool_version_id,
                name=tool_name,
                version=version,
                parent_tool=parent_tool,
                code=tool_code,
                success_rate=100.0,
                avg_latency=avg_latency,
                replaced_by=None,
                status="ACTIVE",
                created_at=datetime.utcnow()
            )
            session.add(db_tool)
            await session.commit()

        # 4. Import and compile dynamically
        try:
            spec = importlib.util.spec_from_file_location(tool_name, file_path_main)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load spec for dynamic tool: {tool_name}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            tool_fn = getattr(module, tool_name)
            
            # Save in global register
            DYNAMIC_TOOL_LIBRARY[tool_name] = tool_fn
            
            # 5. Record relationship paths in the topology graph
            await memory_service.store_topology_relation(tool_version_id, "InfrastructureHouse", "HAS_TOOL_VERSION")
            if parent_tool:
                await memory_service.store_topology_relation(tool_version_id, parent_tool, "REPLACES")
                await memory_service.store_topology_relation(tool_version_id, parent_tool, "MUTATED_FROM")

            logger.info(f"🛠️  [TOOL EVOLUTION REGISTERED] Versioned active tool: {tool_version_id}")
            return True
        except Exception as e:
            logger.error(f"Failed dynamic tool compile & registration: {e}")
            return False

    async def benchmark_and_evolve_tool(self, tool_name: str, new_code: str, test_code: str) -> Optional[str]:
        """
        Validates a new tool candidate: benchmarks success rate and execution latency.
        Only promotes and replaces if candidate is at least 20% faster than the current active one.
        """
        logger.info(f"🛠️  [TOOL BENCHMARK] Benchmarking evolution candidate for tool '{tool_name}'...")
        
        # 1. Verify safety of candidate code
        if not self.ast_safety_audit(new_code) or not self.ast_safety_audit(test_code):
            logger.error("Candidate failed safety AST audits!")
            return None
            
        # 2. Compile candidate function in clean scopes
        local_scope: Dict[str, Any] = {}
        try:
            exec(new_code, local_scope)
            candidate_fn = local_scope.get(tool_name)
            if not candidate_fn:
                return None
        except Exception as e:
            logger.error(f"Failed compiling candidate function: {e}")
            return None
            
        test_scope = {tool_name: candidate_fn}
        try:
            exec(test_code, test_scope)
            run_test_fn = test_scope.get("run_test")
            if not run_test_fn:
                return None
        except Exception as e:
            logger.error(f"Failed compiling candidate test script: {e}")
            return None

        # 3. Perform Latency and Success Telemetry Check
        iterations = 10
        start_time = time.perf_counter()
        successes = 0
        for _ in range(iterations):
            try:
                if run_test_fn():
                    successes += 1
            except Exception:
                pass
        end_time = time.perf_counter()
        
        if successes < iterations:
            logger.warning(f"Candidate rejected: failed verification tests ({successes}/{iterations} successes).")
            return None
            
        new_latency_ms = ((end_time - start_time) / iterations) * 1000.0
        logger.info(f"🛠️  [BENCHMARK] Candidate tool avg latency: {new_latency_ms:.3f}ms")

        # 4. Check for active current version and run comparison
        old_tool_fn = DYNAMIC_TOOL_LIBRARY.get(tool_name)
        parent_id = None
        
        if old_tool_fn:
            # Look up active db record for parent ID
            async with schemas.async_session() as session:
                stmt = select(SQLToolVersion).where(
                    SQLToolVersion.name == tool_name,
                    SQLToolVersion.status == "ACTIVE"
                ).order_by(SQLToolVersion.created_at.desc()).limit(1)
                res = await session.execute(stmt)
                old_db = res.scalars().first()
                if old_db:
                    parent_id = old_db.id

            # Benchmark current tool
            old_test_scope = {tool_name: old_tool_fn}
            try:
                exec(test_code, old_test_scope)
                old_test_fn = old_test_scope.get("run_test")
                if old_test_fn:
                    start_old = time.perf_counter()
                    for _ in range(iterations):
                        try:
                            old_test_fn()
                        except Exception:
                            pass
                    end_old = time.perf_counter()
                    old_latency_ms = ((end_old - start_old) / iterations) * 1000.0
                    logger.info(f"🛠️  [BENCHMARK] Current active tool latency: {old_latency_ms:.3f}ms")
                    
                    # Target 20%+ efficiency gain
                    efficiency_ratio = new_latency_ms / old_latency_ms if old_latency_ms > 0 else 1.0
                    if efficiency_ratio > 0.8:
                        logger.info(f"🛠️  [EVOLUTION ABORTED] Efficiency gain ({((1.0 - efficiency_ratio)*100):.1f}%) is below evolution threshold (20%).")
                        return None
                    else:
                        logger.info(f"🎉 [EVOLUTION APPROVED] Speedup achieved: {((1.0 - efficiency_ratio)*100):.1f}% speed improvement!")
            except Exception as ex:
                logger.warning(f"Could not benchmark old version: {ex}. Promoting candidate by default.")

        # 5. Promotes and Registers
        success = await self.register_tool_to_library(tool_name, new_code, parent_tool=parent_id, avg_latency=new_latency_ms)
        if success:
            return tool_name
        return None

# Global instance
tool_creator = ToolCreatorEngine()
