import os
import uuid
import json
import logging
import asyncio
import subprocess
from datetime import datetime
from typing import Dict, Any, List

from app.core.llm_provider import LLMFactory
from app.services.memory_service import memory_service
from app.models.schemas import get_db_session, SQLGeneratedArtifact, SQLExecutionTrace

logger = logging.getLogger(__name__)

class AutonomousExecutionEngine:
    def __init__(self):
        self.artifacts_dir = os.path.join(os.path.abspath('.'), "artifacts")
        os.makedirs(self.artifacts_dir, exist_ok=True)

    async def execute_generative_task(self, task_id: str, objective: str, agent_id: str, capability: str = "UNKNOWN") -> Dict[str, Any]:
        """
        Executes an end-to-end task by prompting the LLM, writing files, and validating.
        """
        provider = LLMFactory.get_provider()
        
        # 0. Experience Reuse - Search for previous doctrines
        llm_bypassed = False
        model_calls = 1
        written_files = []
        data = {}
        
        task_dir = os.path.join(self.artifacts_dir, task_id)
        os.makedirs(task_dir, exist_ok=True)
        
        try:
            semantic_context = await memory_service.search_semantic_memories(objective, limit=3, capability=capability)
            
            for m in semantic_context:
                if m.get("score", 0) > 0.9 and m.get("artifact_path") and os.path.exists(m["artifact_path"]):
                    logger.info(f"[EXECUTION ENGINE] High confidence doctrine found (score: {m['score']}). Bypassing LLM...")
                    llm_bypassed = True
                    model_calls = 0
                    
                    with open(m["artifact_path"], "r") as f:
                        content = f.read()
                        
                    file_name = os.path.basename(m["artifact_path"])
                    file_path = os.path.join(task_dir, file_name)
                    with open(file_path, "w") as f:
                        f.write(content)
                        
                    written_files.append(file_path)
                    break
                    
            if not llm_bypassed:
                context_str = "\n".join([f"- {m['memory_type']}: {m['content']}" for m in semantic_context])
            else:
                context_str = "Bypassed."
        except Exception as e:
            logger.warning(f"Semantic search failed: {e}")
            context_str = "No prior semantic context available."
        
        try:
            if not llm_bypassed:
                system_prompt = (
                    "You are an autonomous AI executing a software development task. "
                    f"Here is inherited knowledge from previous executions:\n{context_str}\n\n"
                    "You MUST output ONLY a valid JSON object. No markdown formatting outside the JSON, no explanations. "
                    "The JSON should match this schema:\n"
                    "{\n"
                    "  'files': [ { 'path': 'relative/path/to/file.py', 'content': 'raw string of file contents' } ],\n"
                    "  'knowledge_distillation': {\n"
                    "      'extracted_facts': ['fact 1'],\n"
                    "      'workflow_improvements': ['improvement 1'],\n"
                    "      'doctrines_derived': ['doctrine 1']\n"
                    "  }\n"
                    "}"
                )
                
                user_prompt = f"Complete the following objective: {objective}\nInclude unit tests if appropriate."

                # 1. Generate code via LLM
                logger.info(f"[EXECUTION ENGINE] Invoking LLM for task {task_id}")
                response_text = await provider.generate(user_prompt, system_prompt)
                
                # Clean up markdown if the LLM leaked it
                if response_text.startswith("```json"):
                    response_text = response_text[7:-3].strip()
                elif response_text.startswith("```"):
                    response_text = response_text[3:-3].strip()
                    
                data = json.loads(response_text)
                
                # 2. Write artifacts to disk
                for file_obj in data.get("files", []):
                    file_path = os.path.join(task_dir, file_obj["path"])
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, "w") as f:
                        f.write(file_obj["content"])
                    written_files.append(file_path)
                    
                logger.info(f"[EXECUTION ENGINE] Generated {len(written_files)} files at {task_dir}")
            else:
                logger.info(f"[EXECUTION ENGINE] Loaded {len(written_files)} files directly from memory.")
            
            # 3. Run Sandbox Validation
            trace_stdout, trace_stderr, exit_code, time_ms = await self.run_sandbox_validation(task_dir)
            
            # 4. Reality Enforcement
            validation_status = "PASSED" if exit_code == 0 else "FAILED"
            benchmark_result = 1.0 if exit_code == 0 else 0.0
            
            if exit_code != 0:
                logger.error(f"[EXECUTION ENGINE] Validation FAILED for task {task_id}. Sandbox returned code {exit_code}")
                # We enforce reality by failing the task entirely if tests fail
                raise RuntimeError(f"Sandbox Validation Failed: {trace_stderr or trace_stdout}")

            # 5. Store Traces and Artifacts in DB
            trace_id = f"trace_{uuid.uuid4().hex[:8]}"
            await self._store_trace(trace_id, task_id, trace_stdout, trace_stderr, time_ms, exit_code, validation_status, llm_bypassed, model_calls)
            
            for file_path in written_files:
                await self._store_artifact(
                    objective_id=objective,
                    task_id=task_id,
                    trace_id=trace_id,
                    creator_agent=agent_id,
                    file_path=file_path,
                    artifact_type="CODE",
                    file_size=os.path.getsize(file_path),
                    benchmark_result=benchmark_result,
                    validation_status=validation_status,
                    capability=capability
                )
                
            # 6. Distill Knowledge if task passed
            if exit_code == 0 and not llm_bypassed:
                knowledge = data.get("knowledge_distillation", {})
                
                # Pick the first artifact as representative for bypass tracking
                artifact_path = written_files[0] if written_files else None
                
                for doc in knowledge.get("doctrines_derived", []):
                    try:
                        mem_id = f"doc_{uuid.uuid4().hex[:8]}"
                        await memory_service.store_semantic_memory(
                            title=f"Doctrine from {task_id}",
                            raw_content=doc,
                            memory_type="DOCTRINE",
                            capability=capability,
                            artifact_path=artifact_path
                        )
                        await memory_service.store_topology_relation(agent_id, mem_id, "GENERATED_DOCTRINE")
                    except Exception as e:
                        logger.warning(f"Failed to store doctrine: {e}")
                        
                for wf in knowledge.get("workflow_improvements", []):
                    try:
                        mem_id = f"wf_{uuid.uuid4().hex[:8]}"
                        await memory_service.store_semantic_memory(
                            title=f"Workflow Improvement from {task_id}",
                            raw_content=wf,
                            memory_type="WORKFLOW",
                            capability=capability,
                            artifact_path=artifact_path
                        )
                        await memory_service.store_topology_relation(agent_id, mem_id, "GENERATED_WORKFLOW")
                    except Exception as e:
                        logger.warning(f"Failed to store workflow: {e}")
            else:
                # Failure Memory
                try:
                    mem_id = f"fail_{uuid.uuid4().hex[:8]}"
                    await memory_service.store_semantic_memory(
                        title=f"Failure Memory from {task_id}",
                        raw_content=f"Validation failed for objective: {objective}. Error: {trace_stderr}",
                        memory_type="FAILURE_MEMORY",
                        capability=capability
                    )
                except Exception:
                    pass

            return {
                "status": validation_status,
                "trace_id": trace_id,
                "artifacts": written_files,
                "stdout": trace_stdout,
                "llm_bypassed": llm_bypassed,
                "model_calls": model_calls
            }
            
        except Exception as e:
            logger.error(f"[EXECUTION ENGINE] Task {task_id} failed: {e}")
            raise e

    async def run_sandbox_validation(self, task_dir: str) -> tuple[str, str, int, float]:
        """
        Executes pytest in the task directory if tests exist, else runs a basic python check.
        """
        start_time = datetime.utcnow()
        
        # Check if pytest is applicable
        test_files = [f for f in os.listdir(task_dir) if f.startswith("test_")]
        
        try:
            if test_files:
                process = await asyncio.create_subprocess_shell(
                    f"python3 -m pytest {task_dir}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=task_dir
                )
            else:
                # Just dry run python files to ensure they compile
                py_files = [f for f in os.listdir(task_dir) if f.endswith(".py")]
                cmd = f"python3 -m py_compile {' '.join(py_files)}" if py_files else "echo 'No tests or code found.'"
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=task_dir
                )
                
            stdout, stderr = await process.communicate()
            end_time = datetime.utcnow()
            time_ms = (end_time - start_time).total_seconds() * 1000
            
            return stdout.decode(), stderr.decode(), process.returncode, time_ms
            
        except Exception as e:
            return "", str(e), 1, 0.0

    async def _store_trace(self, trace_id, task_id, stdout, stderr, time_ms, exit_code, status, llm_bypassed, model_calls):
        async for session in get_db_session():
            trace = SQLExecutionTrace(
                id=trace_id,
                task_id=task_id,
                stdout_log=stdout,
                stderr_log=stderr,
                execution_time_ms=time_ms,
                exit_code=exit_code,
                status=status,
                llm_bypassed=llm_bypassed,
                model_calls=model_calls,
                created_at=datetime.utcnow()
            )
            session.add(trace)
            await session.commit()
            break

    async def _store_artifact(self, objective_id, task_id, trace_id, creator_agent, file_path, artifact_type, file_size, benchmark_result, validation_status, capability):
        async for session in get_db_session():
            artifact = SQLGeneratedArtifact(
                id=f"art_{uuid.uuid4().hex[:8]}",
                objective_id=objective_id,
                task_id=task_id,
                trace_id=trace_id,
                creator_agent=creator_agent,
                file_path=file_path,
                artifact_type=artifact_type,
                file_size_bytes=file_size,
                benchmark_result=benchmark_result,
                validation_status=validation_status,
                capability=capability,
                created_at=datetime.utcnow()
            )
            session.add(artifact)
            await session.commit()
            break

autonomous_execution_engine = AutonomousExecutionEngine()
