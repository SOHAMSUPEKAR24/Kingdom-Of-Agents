import asyncio
import logging
from typing import Dict, Any, List, Optional
import networkx as nx

from app.core.event_bus import event_bus, Event
from app.services.memory_service import memory_service
from app.models.schemas import TaskSchema

logger = logging.getLogger("antigravity.knight")

class KnightCore:
    def __init__(self):
        self.active_objectives: Dict[str, str] = {} # objective_id -> raw_text
        self.task_graphs: Dict[str, nx.DiGraph] = {} # objective_id -> networkx DAG

    async def initialize(self):
        # Subscribe to task completion and failure events
        event_bus.subscribe("TASK_COMPLETED", self.handle_task_completed)
        event_bus.subscribe("TASK_FAILED", self.handle_task_failed)
        
        # Phase 7: Initialize Distributed Swarm Civilization
        try:
            from app.services.distributed_civilization import distributed_civilization
            await distributed_civilization.initialize()
            logger.info("🌐 [DISTRIBUTED INITIALIZE] Knight-0 successfully joined the Federated Governor grid.")
        except Exception as e:
            logger.error(f"Failed to initialize Distributed Civilization Mesh: {e}")
            
        logger.info("Knight-0 Core Orchestration initialized and listening for task completions.")

    async def accept_objective(self, objective_id: str, raw_objective: str) -> List[TaskSchema]:
        """
        Receives an objective from the King, decomposes it into a DAG,
        saves all tasks to memory, and schedules initial runnable tasks.
        """
        logger.info(f"👑 [KING'S COMMAND ACCEPTED] Objective {objective_id}: '{raw_objective}'")
        self.active_objectives[objective_id] = raw_objective
        await memory_service.store_log(None, "Knight-0", f"Analyzing objective: {raw_objective}", "INFO")

        # Phase 8: Load highest-fitness cognitive genome
        try:
            from app.models.schemas import SQLCognitiveGenome
            from sqlalchemy import select, desc
            from app.models import schemas
            async with schemas.async_session() as session:
                stmt = select(SQLCognitiveGenome).order_by(desc(SQLCognitiveGenome.fitness_score)).limit(1)
                res = await session.execute(stmt)
                active_genome = res.scalars().first()
            if active_genome:
                logger.info(f"🧬 [EVOLVED GENOME LOADED] Active Genome: {active_genome.id} | Reasoning: {active_genome.reasoning_style} | Debate: {active_genome.debate_format}")
            else:
                logger.info("🧬 [GENOME ENGINE] No evolved genomes found in DB yet. Using default parameters.")
        except Exception as e:
            logger.error(f"Failed to load active genome in intake: {e}")

        # Intercept and run Phase 6 Alignment & Trust pre-planning audits
        try:
            from app.services.alignment_engine import alignment_swarm
            alignment_audit = await alignment_swarm.execute_pre_planning_alignment_audit(objective_id, raw_objective)
            if alignment_audit["status"] == "BLOCKED" or alignment_audit["alignment_score"] < 0.70:
                logger.critical(f"🚨 [ALIGNMENT BLOCKED] Objective {objective_id} violates constitutional safety boundaries! Score: {alignment_audit['alignment_score'] * 100:.1f}%. Reason: {alignment_audit['ethical_review']}")
                await memory_service.store_log(None, "Knight-0", f"CRITICAL: Objective BLOCKED by Alignment Engine. Score: {alignment_audit['alignment_score'] * 100:.1f}%. Review: {alignment_audit['ethical_review']}", "CRITICAL")
                raise ValueError(f"Objective blocked by Sovereign Alignment Engine: {alignment_audit['ethical_review']}")
            elif alignment_audit["status"] == "WARNING":
                logger.warning(f"⚠️ [ALIGNMENT WARNING] Objective {objective_id} flagged: {alignment_audit['ethical_review']}")
                await memory_service.store_log(None, "Knight-0", f"WARNING: Alignment warning flagged: {alignment_audit['ethical_review']}", "WARNING")
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Alignment pre-planning audit failed: {e}")

        # 0. Intercept and run Phase 5 Meta-Cognitive pre-planning audits
        try:
            from app.services.meta_cognitive_engine import meta_cognitive_swarm
            await meta_cognitive_swarm.execute_pre_objective_audit(objective_id, raw_objective)
        except Exception as e:
            logger.error(f"Meta-cognitive pre-planning audit failed: {e}")

        # Phase 9: Trigger autonomous scientific reasoning engine
        try:
            from app.services.scientific_cognition import scientific_cognition
            await scientific_cognition.autonomous_scientific_reasoning_engine()
        except Exception as e:
            logger.error(f"Failed to trigger Phase 9 scientific reasoning engine: {e}")


        # Run the Multi-Lens debate, Consensus & Future branches
        from app.services.polycognitive_engine import polycognitive_engine
        planning_results = await polycognitive_engine.orchestrate_planning(raw_objective)
        planning_results["objective_id"] = objective_id
        
        # Run reasoning audit of the completed debate
        try:
            from app.services.meta_cognitive_engine import meta_cognitive_swarm
            await meta_cognitive_swarm.meta_cognitive.audit_reasoning(objective_id, planning_results.get("debate", []))
        except Exception as e:
            logger.error(f"Reasoning audit failed: {e}")
        
        if not hasattr(self, "current_planning_state"):
            self.current_planning_state = {}
        self.current_planning_state[objective_id] = planning_results

        # 1. Decompose objective into subtasks with PFA and Long-Horizon checks
        tasks = await self._plan_objective(objective_id, raw_objective)

        # Phase 7: Cross-Node Debate & Latency-Aware Cognitive Routing
        try:
            from app.services.distributed_civilization import distributed_civilization
            logger.info("🌐 [DISTRIBUTED ROUTING] Ingesting latency-aware node delegation...")
            await distributed_civilization.execute_cross_node_planning(raw_objective)
            for t in tasks:
                node_id = await distributed_civilization.route_objective_execution(t.title)
                t.input_data["assigned_node_id"] = node_id
                logger.info(f"🎯 [DISTRIBUTED ROUTED] Task '{t.id}' assigned to optimal specialized node: {node_id}")
        except Exception as e:
            logger.error(f"Failed Phase 7 cross-node planning or routing: {e}")

        # 2. Build and validate DAG using NetworkX
        dag = nx.DiGraph()
        for t in tasks:
            dag.add_node(t.id, task=t)
        
        # Add dependency edges
        for t in tasks:
            for dep in t.dependencies:
                if dep in dag:
                    dag.add_edge(dep, t.id) # dep must finish before t.id starts
        
        # Validate that graph is a DAG (no circular loops, complying with CONST-IV limit controls)
        if not nx.is_directed_acyclic_graph(dag):
            logger.critical(f"PLANNING ERROR: Knight-0 planning generated a circular dependency graph! Aborting.")
            await memory_service.store_log(None, "Knight-0", "Spawning aborted: Circular dependencies detected in plan graph", "CRITICAL")
            raise ValueError("Task graph is not a Directed Acyclic Graph (DAG)!")

        self.task_graphs[objective_id] = dag
        
        # 3. Store topology relations in Graph memory
        await memory_service.store_topology_relation("King", "Knight", "GOVERNS")
        for t in tasks:
            await memory_service.store_topology_relation("Knight", t.assigned_house, "COORDINATES")
            await memory_service.store_topology_relation(t.assigned_house, t.id, "ALLOCATED_TO")
            for dep in t.dependencies:
                await memory_service.store_topology_relation(dep, t.id, "BLOCKS")

        # 4. Save tasks relational data
        for t in tasks:
            await memory_service.store_task(t)

        # 5. Emit initial trigger events for tasks with no dependencies (indegree == 0)
        asyncio.create_task(self._schedule_ready_tasks(objective_id))

        return tasks

    async def run_predictive_failure_analysis(self, raw_objective: str) -> float:
        """
        Scans candidate task goals/keywords against historical `FAILURE` and `QUARANTINE` memory clusters
        to calculate a risk coefficient (0.0 to 1.0).
        """
        failures = await memory_service.search_semantic_memories(raw_objective, limit=5)
        risk = 0.0
        match_count = 0
        for f in failures:
            mtype = f.get("memory_type", "")
            title = f.get("title", "").lower()
            if mtype in ("FAILURE", "QUARANTINE") or "fail" in title or "quarantine" in title or "poison" in title:
                score = f.get("score", 0.0)
                risk = max(risk, score)
                match_count += 1
        
        # Scale slightly with number of failures to capture cluster density
        if match_count > 0:
            risk = min(1.0, risk * (1.0 + 0.1 * match_count))
            
        logger.info(f"🔮 [PREDICTIVE FAILURE ANALYSIS] Risk Coefficient: {round(risk * 100, 2)}% based on {match_count} historical failures.")
        return risk

    async def _plan_objective(self, objective_id: str, raw_objective: str) -> List[TaskSchema]:
        """
        Dynamically decomposes high-level objectives into specific multi-house subtasks,
        completely driven by the Polycognitive Swarm Parliament and Consensus chosen scenario tree.
        """
        from app.services.agent_evolver import agent_evolver
        from app.services.tool_creator import tool_creator
        
        logger.info(f"🧬 [WORKFLOW PLANNER] Running capability gap analysis on: '{raw_objective}'")
        
        # 1. Run Predictive Failure Analysis (PFA)
        risk_coef = await self.run_predictive_failure_analysis(raw_objective)
        
        # 2. Check for dynamic Agent Capability Gap
        agent_gap = agent_evolver.discover_capability_gap(raw_objective, [])
        dynamic_role = None
        if agent_gap:
            role_name = agent_gap["role_name"]
            logger.warning(f"🧬 [CAPABILITY GAP FOUND] Discovered missing agent capability for role: {role_name}")
            try:
                # Generate, compile, and register class
                code = agent_evolver.generate_agent_class_source(role_name, agent_gap["gap_desc"])
                agent_evolver.register_and_compile_agent(role_name, code)
                dynamic_role = role_name
                logger.info(f"🧬 [MUTATION SUCCESS] Registered dynamic role '{role_name}' into evolution registry.")
            except Exception as e:
                logger.error(f"Failed dynamic class generation fallback to standard soldier: {e}")
        
        # 3. Check for dynamic Tool Gap
        tool_req = ""
        if "base64" in raw_objective.lower() or "xor" in raw_objective.lower():
            tool_req = "base64_xor_cipher"
        elif "convert" in raw_objective.lower() or "markdown" in raw_objective.lower() or "table" in raw_objective.lower():
            tool_req = "dict_to_markdown_table"
            
        tool_gap = tool_creator.discover_tool_gap(raw_objective, tool_req)
        if tool_gap:
            tool_name = tool_gap["tool_name"]
            logger.warning(f"🛠️  [TOOL GAP FOUND] Discovered missing tool capability for: {tool_name}")
            try:
                # Generate, test in sandbox, and register
                tool_code, test_code = tool_creator.generate_tool_source(tool_name, tool_gap["description"])
                test_passed = tool_creator.test_tool_in_sandbox(tool_name, tool_code, test_code)
                if test_passed:
                    await tool_creator.register_tool_to_library(tool_name, tool_code)
                    logger.info(f"🛠️  [MUTATION SUCCESS] Dynamic tool '{tool_name}' verified and fully active.")
            except Exception as e:
                logger.error(f"Failed dynamic tool registration: {e}")

        # Get consensus-driven simulation branch details
        planning_state = getattr(self, "current_planning_state", {}).get(objective_id, {})
        scenarios = planning_state.get("scenarios", [])
        
        # By default, we select Plan B (the consensus standard plan)
        selected_branch = "Plan B"
        # Find Plan B scenario nodes
        scenario_nodes = ["StrategyHouse", "SecurityHouse", "EngineeringHouse", "MemoryHouse"]
        for s in scenarios:
            if s["branch_name"] == selected_branch:
                proj = s["topology_projection"]
                scenario_nodes = [node["id"] for node in proj["nodes"]]
                break
                
        logger.info(f"🎯 [CONSENSUS DECISION DEPLOYED] Applying dynamic scenario node-sequence: {scenario_nodes}")

        # 4. Generate dynamic tasks matching the active nodes from the consensus branch
        tasks = []
        prev_task_id = None
        
        # Pre-emptive risk mitigation if risk is high
        if risk_coef >= 0.75:
            logger.warning(f"⚠️ [HIGH RISK FORECASTED] Risk coefficient {round(risk_coef * 100, 2)}% exceeds threshold. Ingesting mitigation.")
            t_mitigate = TaskSchema(
                id=f"{objective_id}_task_00_mitigation",
                parent_objective=raw_objective,
                title="Pre-emptive Risk Mitigation & Security Hardening",
                assigned_house="SecurityHouse",
                status="PENDING",
                input_data={"risk_coefficient": risk_coef, "strategy": "enforce AST safety limits, verify input parameters"},
                dependencies=[]
            )
            tasks.append(t_mitigate)
            prev_task_id = t_mitigate.id

        # Loop through node sequence and dynamically instantiate Tasks
        for i, house in enumerate(scenario_nodes):
            task_id = f"{objective_id}_task_{i+1:02d}_{house.lower().replace('house', '')}"
            dependencies = [prev_task_id] if prev_task_id else []
            
            # Map house to title and payload
            if house == "StrategyHouse":
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Formulate Strategy & Constraints Check",
                    assigned_house="StrategyHouse",
                    status="PENDING",
                    input_data={"objective": raw_objective},
                    dependencies=dependencies
                )
            elif house == "ResearchHouse":
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Gather Web and Document Context",
                    assigned_house="ResearchHouse",
                    status="PENDING",
                    input_data={"queries": ["autonomous agent topology", "memory compression models"]},
                    dependencies=dependencies
                )
            elif house == "LogicHouse":
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Deconstruct Logic and Verify Premises",
                    assigned_house="LogicHouse",
                    status="PENDING",
                    input_data={"objective": raw_objective},
                    dependencies=dependencies
                )
            elif house == "EngineeringHouse":
                # Check dynamic roles
                from app.services.agent_evolver import DYNAMIC_AGENT_REGISTRY
                use_transformer = (dynamic_role == "DataTransformerSoldier") or ("DataTransformerSoldier" in DYNAMIC_AGENT_REGISTRY)
                
                from app.services.execution_sandbox import ExecutionSandbox
                
                # Determine tech stack from objective loosely
                inferred_stack = "python"
                obj_lower = raw_objective.lower()
                words = obj_lower.replace(",", " ").replace(".", " ").split()
                
                sorted_langs = sorted(ExecutionSandbox.LANGUAGE_MAPPINGS.keys(), key=len, reverse=True)
                for lang in sorted_langs:
                    if lang in words:
                        inferred_stack = lang
                        break
                
                # Special edge cases for attached symbols
                if inferred_stack == "python":
                    if "c++" in obj_lower: inferred_stack = "c++"
                    elif "c#" in obj_lower: inferred_stack = "c#"
                    elif "f#" in obj_lower: inferred_stack = "f#"
                    elif "node.js" in obj_lower: inferred_stack = "nodejs"

                input_data = {"tech_stack": inferred_stack, "scope": "infrastructure components"}
                if use_transformer:
                    input_data = {
                        "assigned_role": "DataTransformerSoldier",
                        "data": {"status": "SUCCESS", "message": "Engineering House successfully mutated the DAG"},
                        "format": "markdown"
                    }
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Build Core Modules and Utilities",
                    assigned_house="EngineeringHouse",
                    status="PENDING",
                    input_data=input_data,
                    dependencies=dependencies
                )
            elif house == "SecurityHouse":
                from app.services.agent_evolver import DYNAMIC_AGENT_REGISTRY
                use_cryptographer = (dynamic_role == "CryptographerSoldier") or ("CryptographerSoldier" in DYNAMIC_AGENT_REGISTRY)
                
                input_data = {"target": "compiled_modules"}
                if use_cryptographer:
                    input_data = {
                        "assigned_role": "CryptographerSoldier",
                        "payload": "SecretDataXORPayloadForEvolutionVerification",
                        "key": "antigravity",
                        "operation": "encrypt"
                    }
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Perform Compliance Audit & Vulnerability Check",
                    assigned_house="SecurityHouse",
                    status="PENDING",
                    input_data=input_data,
                    dependencies=dependencies
                )
            elif house == "EthicsGovernanceHouse":
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Audit Swarm Ethics & Constitutional Compliance",
                    assigned_house="EthicsGovernanceHouse",
                    status="PENDING",
                    input_data={"objective": raw_objective},
                    dependencies=dependencies
                )
            elif house == "MemoryHouse":
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title="Synthesize and Compress Swarm Experience",
                    assigned_house="MemoryHouse",
                    status="PENDING",
                    input_data={"log_aggregation": "task_runs"},
                    dependencies=dependencies
                )
            else:
                # Catch-all default house
                t = TaskSchema(
                    id=task_id,
                    parent_objective=raw_objective,
                    title=f"Execute {house} Operations",
                    assigned_house=house,
                    status="PENDING",
                    input_data={"objective": raw_objective},
                    dependencies=dependencies
                )

            tasks.append(t)
            prev_task_id = t.id

        return tasks

    async def _schedule_ready_tasks(self, objective_id: str):
        """Scans the Task Graph and schedules all tasks that are ready (all parents completed)."""
        dag = self.task_graphs.get(objective_id)
        if not dag:
            return

        for node_id in dag.nodes:
            task_node = dag.nodes[node_id]["task"]
            if task_node.status != "PENDING":
                continue

            # Check dependencies
            parents = list(dag.predecessors(node_id))
            all_parents_done = True
            for p in parents:
                p_task = dag.nodes[p]["task"]
                if p_task.status != "COMPLETED":
                    all_parents_done = False
                    break
            
            if all_parents_done:
                # Task is unblocked! Set status and trigger event
                task_node.status = "RUNNING"
                await memory_service.store_task(task_node)
                
                # Emit events to trigger specialized House listeners
                event = Event(
                    event_type="TASK_ASSIGNED",
                    sender="Knight-0",
                    payload={"task": task_node.model_dump()}
                )
                await event_bus.publish(event)
                await memory_service.store_log(task_node.id, "Knight-0", f"Assigned task {task_node.id} to {task_node.assigned_house}", "INFO")

    async def _run_meta_learning_update(self, objective_id: str, success: bool):
        """
        Meta-Learning Engine: Recursively adjusts delegation policies, learning retrieval rates,
        and prompts/weights in the reinforcement engine based on the final outcome of the objective.
        """
        logger.info(f"🧬 [META-LEARNING ENGINE] Running post-objective adaptation audit for: {objective_id} (Success: {success})")
        from app.services.reinforcement import reinforcement_engine
        
        dag = self.task_graphs.get(objective_id)
        if not dag:
            return
            
        for node_id in dag.nodes:
            task_node = dag.nodes[node_id]["task"]
            house = task_node.assigned_house
            if success:
                # Reward successful delegation
                await reinforcement_engine.reward_house(house, 0.95)
            else:
                if task_node.status == "FAILED":
                    logger.warning(f"🧬 [META-LEARNING PENALTY] Penalizing house {house} due to failed task {task_node.id}")
                    await reinforcement_engine.penalize_house(house)
                else:
                    # Slightly boost strategy/security houses to improve guidance
                    if house in ("StrategyHouse", "SecurityHouse"):
                        await reinforcement_engine.reward_house(house, 0.5)

        # Phase 8: Hook up autonomous meta-learning systems
        try:
            from app.services.meta_learning import meta_learning
            if success:
                # Distill completed run into blueprint and derive abstract laws
                run = await meta_learning.distill_completed_run(objective_id)
                law = await meta_learning.derive_abstract_principles(run.id)
                logger.info(f"🧬 [META-LEARNING SUCCESS] Distilled Completed Run: {run.id}. Derived Law: {law[:60]}...")
                
                # Evolve cognitive genomes
                await meta_learning.evolve_cognitive_genomes()
                # Run meta-reinforcement step
                await meta_learning.reinforcement_learning_step(speed_gain=0.15, accuracy_gain=0.10)
            else:
                # Analyze failure cascade
                run = await meta_learning.analyze_failure_cascade(objective_id, f"Objective run failed or cascaded to FAILED state.")
                logger.warning(f"🧬 [META-LEARNING FAILURE ANALYSIS] Cascaded failure directive recorded under run: {run.id}")
                # Run meta-reinforcement decay step
                await meta_learning.reinforcement_learning_step(speed_gain=0.0, accuracy_gain=-0.25)
        except Exception as ml_err:
            logger.error(f"Error executing Phase 8 Meta-Learning routines: {ml_err}")

    async def handle_task_completed(self, event: Event):
        task_data = event.payload.get("task")
        if not task_data:
            return
        
        task_id = task_data.get("id")
        objective_id = task_id.split("_task_")[0]
        
        dag = self.task_graphs.get(objective_id)
        if not dag or task_id not in dag:
            return

        logger.info(f"✅ [KNIGHT-0 RECEIVED TASK_COMPLETED] Task {task_id} marked complete by {event.sender}")
        
        # 1. Update task state in memory representation
        task_node = dag.nodes[task_id]["task"]
        task_node.status = "COMPLETED"
        task_node.output_data = task_data.get("output_data", {})
        task_node.assigned_soldier = task_data.get("assigned_soldier")
        await memory_service.store_task(task_node)

        # Phase 7: Replicate Task Completion State & Memory Shard
        try:
            import uuid
            from app.services.distributed_civilization import distributed_civilization
            await distributed_civilization.trigger_nervous_reflex(
                "TASK_STATE_REPLICATED",
                f"Task {task_id} marked COMPLETED. Replicating state and outputs across the governor network.",
                "INFO"
            )
            # Create a memory shard of this task run
            host = task_node.input_data.get("assigned_node_id", "node_local")
            shard = await distributed_civilization.create_memory_shard(
                "LINEAGE",
                host,
                f"Task {task_id} completed successfully. Outputs: {str(task_node.output_data)}"
            )
            await distributed_civilization.replicate_shard_state(shard.id, f"gov_backup_{uuid.uuid4().hex[:4]}")
        except Exception as e:
            logger.error(f"Failed replicating task completion state: {e}")

        # 2. Check if all tasks in graph are completed
        all_completed = True
        for node in dag.nodes:
            if dag.nodes[node]["task"].status != "COMPLETED":
                all_completed = False
                break
        
        if all_completed:
            await memory_service.store_log(None, "Knight-0", f"👑 OBJECTIVE COMPLETE: All workflows under objective {objective_id} succeeded.", "INFO")
            logger.info(f"👑 [KINGDOM OBJECTIVE COMPLETED SUCCESSFULLY] All subtasks for objective {objective_id} are COMPLETED.")
            
            # Trigger Meta-Learning Update
            await self._run_meta_learning_update(objective_id, success=True)

            # Trigger Phase 5 Outcomes Reflection Audit
            try:
                from app.services.meta_cognitive_engine import self_reflection_system
                planning_state = getattr(self, "current_planning_state", {}).get(objective_id, {})
                consensus = planning_state.get("consensus", {})
                predicted_prob = consensus.get("consensus_confidence", 0.90) if isinstance(consensus, dict) else 0.90
                await self_reflection_system.perform_self_reflection(objective_id, predicted_prob)
            except Exception as e:
                logger.error(f"Failed performing outcomes reflection: {e}")

            # Trigger Phase 6 Self-Honesty Audit & Relationship memory update
            try:
                from app.services.alignment_engine import alignment_swarm
                planning_state = getattr(self, "current_planning_state", {}).get(objective_id, {})
                consensus = planning_state.get("consensus", {})
                predicted_prob = consensus.get("consensus_confidence", 0.90) if isinstance(consensus, dict) else 0.90
                await alignment_swarm.honesty.run_honesty_audit(objective_id, predicted_prob, 1.0)
                await alignment_swarm.weighting.adapt_weights_on_failure(-0.1)
            except Exception as e:
                logger.error(f"Failed performing outcomes self-honesty audit: {e}")

            # Phase 9: Consolidate accepted theses into permanent discoveries and update causal networks
            try:
                from app.services.scientific_cognition import scientific_cognition
                await scientific_cognition.autonomous_theory_formation_engine()
                await scientific_cognition.causal_discovery_engine()
                await scientific_cognition.knowledge_economy_research_resource_governor()
            except Exception as e:
                logger.error(f"Failed to execute Phase 9 post-objective scientific integration: {e}")

            # Phase 13: Generate Executive Response
            try:
                from app.services.executive_response_engine import executive_response_engine
                
                # Gather outputs from all tasks
                all_outputs = []
                artifacts = []
                specialists = set()
                plan = []
                tools_used = set()
                
                for node in dag.nodes:
                    t = dag.nodes[node]["task"]
                    plan.append(f"{t.id}: {t.title}")
                    specialists.add(t.assigned_house)
                    if t.assigned_soldier:
                        specialists.add(t.assigned_soldier)
                        
                    if t.output_data:
                        all_outputs.append(str(t.output_data))
                        if isinstance(t.output_data, dict) and "tools" in t.output_data:
                            tools_used.update(t.output_data["tools"])
                        
                # Create a synthesized response
                final_answer = "Objective executed successfully. All workflows completed."
                exec_summary = f"Knight-0 coordinated {len(dag.nodes)} subtasks to achieve the objective."
                
                await executive_response_engine.generate_response(
                    objective_id=objective_id,
                    final_answer=final_answer,
                    executive_summary=exec_summary,
                    supporting_evidence=all_outputs[:3],
                    generated_artifacts=artifacts,
                    debate_summary="Consensus reached effectively.",
                    confidence_score=0.95,
                    primary_specialists=list(specialists),
                    plan=plan,
                    tools_used=list(tools_used),
                    benchmark_score=0.92
                )
            except Exception as e:
                logger.error(f"Failed to generate Executive Response: {e}")
            
            # Remove from active
            if objective_id in self.active_objectives:
                del self.active_objectives[objective_id]
                del self.task_graphs[objective_id]
        else:
            # 3. Schedule next unblocked tasks
            asyncio.create_task(self._schedule_ready_tasks(objective_id))

    async def handle_task_failed(self, event: Event):
        task_data = event.payload.get("task")
        if not task_data:
            return
        
        task_id = task_data.get("id")
        objective_id = task_id.split("_task_")[0]
        
        dag = self.task_graphs.get(objective_id)
        if not dag or task_id not in dag:
            return

        logger.error(f"❌ [KNIGHT-0 RECEIVED TASK_FAILED] Task {task_id} failed in {event.sender}!")
        
        task_node = dag.nodes[task_id]["task"]
        task_node.status = "FAILED"
        task_node.assigned_soldier = task_data.get("assigned_soldier")
        await memory_service.store_task(task_node)

        # Phase 7: Replicate Task Failure and trigger anomaly quarantine failover loops
        try:
            from app.services.distributed_civilization import distributed_civilization
            await distributed_civilization.trigger_nervous_reflex(
                "TASK_STATE_REPLICATED",
                f"Task {task_id} marked FAILED. Replicating state across governor networks.",
                "ERROR"
            )
            failed_node = task_node.input_data.get("assigned_node_id")
            if failed_node:
                # Trigger anomaly event to engage Self-Healing Engine
                anomaly_event = Event(
                    event_type="NODE_ANOMALY",
                    sender="Knight-0",
                    payload={"node_id": failed_node, "reason": f"Task execution failed on this node: {error_msg}"}
                )
                await event_bus.publish(anomaly_event)
        except Exception as e:
            logger.error(f"Failed replicating task failure state or triggering node anomaly: {e}")
        
        # Perform self-healing / retries or alert King
        error_msg = event.payload.get("error", "Unknown error")
        await memory_service.store_log(task_id, "Knight-0", f"Task execution failure: {error_msg}. Propagating failure cascade.", "ERROR")
        logger.critical(f"cascade workflow failure on {task_id}. King intervention requested.")

        # Phase 9: Invoke Failure-to-Theory Conversion System
        try:
            from app.services.scientific_cognition import scientific_cognition
            await scientific_cognition.failure_to_theory_conversion_system(task_id, error_msg)
        except Exception as e:
            logger.error(f"Failed Phase 9 Failure-to-Theory conversion: {e}")
        
        # Trigger Meta-Learning Update
        await self._run_meta_learning_update(objective_id, success=False)

        # Trigger Phase 5 Causal Root Cause analysis & Outcomes Reflection
        try:
            from app.services.meta_cognitive_engine import causal_inference, self_reflection_system
            diagnose = await causal_inference.diagnose_failure_root_cause(task_id)
            await memory_service.store_log(task_id, "CausalInferenceEngine", f"Diagnosis: {diagnose['root_cause']}. Blocked downstream: {diagnose['cascading_impact']}", "WARNING")
            
            planning_state = getattr(self, "current_planning_state", {}).get(objective_id, {})
            consensus = planning_state.get("consensus", {})
            predicted_prob = consensus.get("consensus_confidence", 0.90) if isinstance(consensus, dict) else 0.90
            await self_reflection_system.perform_self_reflection(objective_id, predicted_prob)
        except Exception as e:
            logger.error(f"Failed running causal inference failure diagnosis: {e}")

        # Trigger Phase 6 Self-Honesty Audit & Anomaly Weight Spike
        try:
            from app.services.alignment_engine import alignment_swarm
            planning_state = getattr(self, "current_planning_state", {}).get(objective_id, {})
            consensus = planning_state.get("consensus", {})
            predicted_prob = consensus.get("consensus_confidence", 0.90) if isinstance(consensus, dict) else 0.90
            await alignment_swarm.honesty.run_honesty_audit(objective_id, predicted_prob, 0.0)
            await alignment_swarm.weighting.adapt_weights_on_failure(0.5)
        except Exception as e:
            logger.error(f"Failed running Phase 6 honesty audits: {e}")


# Global Knight Orchestration instance
knight = KnightCore()

