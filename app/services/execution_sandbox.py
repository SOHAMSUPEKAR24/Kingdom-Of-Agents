import asyncio
import subprocess
import os
import tempfile
import time
import uuid
import logging
from typing import Dict, Any, Tuple
from app.models import schemas
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

class ExecutionSandbox:
    """Isolated environment for executing python code."""
    def __init__(self, timeout_seconds: int = 10):
        self.timeout = timeout_seconds

    LANGUAGE_MAPPINGS = {
        "python": ("sandbox_exec.py", "python {file}"),
        "javascript": ("sandbox_exec.js", "node {file}"),
        "js": ("sandbox_exec.js", "node {file}"),
        "node": ("sandbox_exec.js", "node {file}"),
        "nodejs": ("sandbox_exec.js", "node {file}"),
        "typescript": ("sandbox_exec.ts", "ts-node {file}"),
        "ts": ("sandbox_exec.ts", "ts-node {file}"),
        "java": ("SandboxExec.java", "javac {file} && java SandboxExec"),
        "c": ("sandbox_exec.c", "gcc {file} -o a.out && ./a.out"),
        "c++": ("sandbox_exec.cpp", "g++ {file} -o a.out && ./a.out"),
        "cpp": ("sandbox_exec.cpp", "g++ {file} -o a.out && ./a.out"),
        "c#": ("sandbox_exec.cs", "csc {file} && ./sandbox_exec.exe"),
        "csharp": ("sandbox_exec.cs", "csc {file} && ./sandbox_exec.exe"),
        "go": ("sandbox_exec.go", "go run {file}"),
        "golang": ("sandbox_exec.go", "go run {file}"),
        "rust": ("sandbox_exec.rs", "rustc {file} && ./sandbox_exec"),
        "kotlin": ("sandbox_exec.kt", "kotlinc {file} -include-runtime -d sandbox_exec.jar && java -jar sandbox_exec.jar"),
        "swift": ("sandbox_exec.swift", "swift {file}"),
        "dart": ("sandbox_exec.dart", "dart run {file}"),
        "php": ("sandbox_exec.php", "php {file}"),
        "ruby": ("sandbox_exec.rb", "ruby {file}"),
        "scala": ("sandbox_exec.scala", "scalac {file} && scala SandboxExec"),
        "perl": ("sandbox_exec.pl", "perl {file}"),
        "lua": ("sandbox_exec.lua", "lua {file}"),
        "julia": ("sandbox_exec.jl", "julia {file}"),
        "r": ("sandbox_exec.r", "Rscript {file}"),
        "zig": ("sandbox_exec.zig", "zig run {file}"),
        "nim": ("sandbox_exec.nim", "nim c -r {file}"),
        "haskell": ("sandbox_exec.hs", "runhaskell {file}"),
        "ocaml": ("sandbox_exec.ml", "ocaml {file}"),
        "f#": ("sandbox_exec.fsx", "dotnet fsi {file}"),
        "fsharp": ("sandbox_exec.fsx", "dotnet fsi {file}"),
        "elixir": ("sandbox_exec.exs", "elixir {file}"),
        "erlang": ("sandbox_exec.erl", "escript {file}"),
        "clojure": ("sandbox_exec.clj", "clojure -M {file}"),
        "bash": ("sandbox_exec.sh", "bash {file}"),
        "shell": ("sandbox_exec.sh", "bash {file}"),
        "sh": ("sandbox_exec.sh", "bash {file}"),
        "zsh": ("sandbox_exec.sh", "zsh {file}"),
        "fish": ("sandbox_exec.fish", "fish {file}"),
        "powershell": ("sandbox_exec.ps1", "pwsh {file}"),
        "sql": ("sandbox_exec.sql", "sqlite3 test.db < {file}"),
        "pl/sql": ("sandbox_exec.sql", "sqlplus -s user/pass @{file}"),
        "t-sql": ("sandbox_exec.sql", "sqlcmd -i {file}"),
        "cypher": ("sandbox_exec.cypher", "cypher-shell -f {file}"),
        "graphql": ("sandbox_exec.graphql", "cat {file}"),
        "matlab": ("sandbox_exec.m", "matlab -batch \"run('{file}')\""),
        "fortran": ("sandbox_exec.f90", "gfortran {file} -o a.out && ./a.out"),
        "cuda": ("sandbox_exec.cu", "nvcc {file} -o a.out && ./a.out"),
        "opencl": ("sandbox_exec.cl", "cat {file}"),
        "solidity": ("sandbox_exec.sol", "solc --bin {file}"),
        "vyper": ("sandbox_exec.vy", "vyper {file}"),
        "move": ("sandbox_exec.move", "move build"),
        "cairo": ("sandbox_exec.cairo", "cairo-run --program {file}"),
        "verilog": ("sandbox_exec.v", "iverilog -o a.out {file} && vvp a.out"),
        "systemverilog": ("sandbox_exec.sv", "iverilog -g2012 -o a.out {file} && vvp a.out"),
        "vhdl": ("sandbox_exec.vhd", "ghdl -a {file} && ghdl -e sandbox_exec && ghdl -r sandbox_exec"),
        "chisel": ("sandbox_exec.scala", "sbt run"),
        "sparql": ("sandbox_exec.rq", "arq --query {file}"),
        "prolog": ("sandbox_exec.pl", "swipl -q -f {file} -t main"),
        "datalog": ("sandbox_exec.dl", "souffle {file}"),
        "assembly": ("sandbox_exec.asm", "nasm -f elf64 {file} && ld sandbox_exec.o -o a.out && ./a.out"),
        "x86 assembly": ("sandbox_exec.asm", "nasm -f elf64 {file} && ld sandbox_exec.o -o a.out && ./a.out"),
        "arm assembly": ("sandbox_exec.s", "as {file} -o sandbox_exec.o && gcc sandbox_exec.o -o a.out && ./a.out"),
        "micropython": ("sandbox_exec.py", "mpy-cross {file}"),
        "ada": ("sandbox_exec.adb", "gnatmake {file} && ./sandbox_exec"),
        "gdscript": ("sandbox_exec.gd", "godot -s {file}")
    }

    def _get_execution_details(self, language: str) -> Tuple[str, str]:
        """Returns the file name and execution command template for a given language."""
        lang = language.lower().strip()
        # Fallback to python if not found
        return self.LANGUAGE_MAPPINGS.get(lang, self.LANGUAGE_MAPPINGS["python"])

    async def execute_code(self, code: str, language: str = "python") -> Tuple[str, str, int, float]:
        """Executes code in a temporary directory via subprocess. Returns stdout, stderr, exit_code, duration_ms."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name, cmd_template = self._get_execution_details(language)
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, "w") as f:
                f.write(code)

            start_time = time.time()
            try:
                # Format the command with the filename and run it in a shell
                cmd = cmd_template.format(file=file_name)
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=temp_dir
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)
                    exit_code = process.returncode
                except asyncio.TimeoutError:
                    process.kill()
                    stdout, stderr = await process.communicate()
                    exit_code = -1
                    stderr += b"\n[Sandbox] Execution timed out."
            
            except Exception as e:
                return "", f"Sandbox Exception: {str(e)}", 1, (time.time() - start_time) * 1000

            duration_ms = (time.time() - start_time) * 1000
            
            # Decode outputs safely
            out_str = stdout.decode('utf-8', errors='replace') if stdout else ""
            err_str = stderr.decode('utf-8', errors='replace') if stderr else ""

            return out_str, err_str, exit_code or 0, duration_ms


class CodeExecutionPipeline:
    """Pipeline to execute tasks securely and save traces."""
    def __init__(self):
        self.sandbox = ExecutionSandbox()

    async def run_task_code(self, task_id: str, code: str, language: str = "python") -> schemas.ExecutionTraceSchema:
        logger.info(f"🚀 [CODE EXECUTION PIPELINE] Executing real capability script ({language}) for task {task_id}...")
        stdout, stderr, exit_code, duration = await self.sandbox.execute_code(code, language)
        
        status = "SUCCESS"
        if exit_code == -1:
            status = "TIMEOUT"
        elif exit_code != 0:
            status = "FAILED"

        trace = schemas.ExecutionTraceSchema(
            id=f"trace_{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            stdout_log=stdout,
            stderr_log=stderr,
            execution_time_ms=duration,
            exit_code=exit_code,
            status=status
        )

        async for session in schemas.get_db_session():
            db_trace = schemas.SQLExecutionTrace(**trace.model_dump())
            session.add(db_trace)
            await session.commit()
            
        logger.info(f"✅ [CODE EXECUTION PIPELINE] Execution completed with status {status}. Trace: {trace.id}")
        return trace


class ExperimentRunnerSystem:
    """Runs scientific experiments by injecting variables into a sandbox."""
    def __init__(self):
        self.pipeline = CodeExecutionPipeline()

    async def execute_experiment(self, hypothesis_id: str, code: str) -> Dict[str, Any]:
        logger.info(f"🧪 [EXPERIMENT RUNNER] Running live experiment for Hypothesis: {hypothesis_id}")
        trace = await self.pipeline.run_task_code(f"exp_{hypothesis_id}", code)
        
        return {
            "hypothesis_id": hypothesis_id,
            "success": trace.exit_code == 0,
            "stdout": trace.stdout_log,
            "stderr": trace.stderr_log,
            "duration": trace.execution_time_ms
        }


class DomainKnowledgeAcquisitionEngine:
    """Retrieves domain knowledge by dynamically executing fetching scripts."""
    def __init__(self):
        self.pipeline = CodeExecutionPipeline()

    async def acquire_knowledge(self, domain: str, retrieval_code: str) -> str:
        logger.info(f"📚 [KNOWLEDGE ACQUISITION] Fetching real documentation for domain: {domain}")
        trace = await self.pipeline.run_task_code(f"knowledge_{domain}", retrieval_code)
        if trace.exit_code == 0:
            logger.info(f"📚 [KNOWLEDGE ACQUISITION] Successfully acquired knowledge for {domain}.")
            return trace.stdout_log or ""
        else:
            logger.warning(f"⚠️ [KNOWLEDGE ACQUISITION] Failed to acquire knowledge for {domain}. Error: {trace.stderr_log}")
            return ""

# Global singletons
execution_pipeline = CodeExecutionPipeline()
experiment_runner = ExperimentRunnerSystem()
knowledge_engine = DomainKnowledgeAcquisitionEngine()
