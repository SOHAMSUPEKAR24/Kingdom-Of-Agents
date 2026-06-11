import logging
import uuid
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy import select, update

from app.models import schemas
from app.models.schemas import (
    SQLAgentGenome, AgentGenomeSchema, SQLReinforcementEvent
)
from app.services.memory_service import memory_service

logger = logging.getLogger("antigravity.genome_engine")

# Base genetic prompt blueprints for each house
HOUSE_PROMPT_BLUEPRINTS = {
    "StrategyHouse": [
        "Decompose goals into task DAGs. Audit constraints. Coordinate orchestrations.",
        "Synthesize high-level objectives. Balance resource limits and parallelize plans.",
        "Evaluate strategic risks, construct robust dependencies, and enforce constitutional boundaries."
    ],
    "ResearchHouse": [
        "Gather web data. Execute crawler scripts. Extract clean tabular intelligence.",
        "Perform deep semantic search queries, summarize browser results, and audit source origins.",
        "Analyze external documentation, verify facts, and build multi-dimensional fact stores."
    ],
    "EngineeringHouse": [
        "Write clean, highly modular code. Implement robust error handling and type-safety.",
        "Build premium glassmorphic UI components, optimize algorithm complexities, and write unit tests.",
        "Generate dry, standard-compliant APIs and optimize database queries."
    ],
    "SecurityHouse": [
        "Perform strict AST checks. Prohibit dangerous OS/sys imports. Enforce Rule V compliance.",
        "Scan task logs for injection exploits. Validate input parameters and sanitize execution boundaries.",
        "Audit outputs against security constraints and isolate anomalous context drifts."
    ],
    "MemoryHouse": [
        "Perform semantic memory compression, store vector embeds, and maintain graph topology.",
        "Cluster related experiences, extract kingdom doctrines, and prune duplicate nodes.",
        "Monitor retrieval counts, calculate relevance decays, and index semantic relationships."
    ],
    "LogicHouse": [
        "Deconstruct arguments mathematically. Enforce formal logic, verify premises, and ensure sound deduction.",
        "Analyze structural optimization paths. Map logical fallacies, critique reasoning chains, and enforce absolute clarity.",
        "Examine proofs, isolate invalid assertions, and build strict logical truth matrices."
    ],
    "ChaosHouse": [
        "Suggest highly disruptive options. Pivot to lateral thinking, inject deliberate randomness, and bypass standards.",
        "Explore extreme outliers, challenge rigid status quo, and introduce radical solutions.",
        "Propose black swan contingencies, maximize experimental variance, and champion high-risk high-reward concepts."
    ],
    "SkepticHouse": [
        "Identify hidden assumptions, point out potential single points of failure, and audit cost overruns.",
        "Challenge consensus blindly. Expose compliance gaps, compute resource leaks, and edge-case vulnerabilities.",
        "Doubt success claims, seek negative evidence, and construct rigorous falsification tests."
    ],
    "SimulationHouse": [
        "Forecast multi-branch futures. Estimate stability indices, speed ratings, and cost factors.",
        "Simulate Plan A, Plan B, and Plan C branches. Assess dynamic trade-offs and project structural paths.",
        "Predict resource usage, visualize outcome nodes, and project long-term system stability metrics."
    ],
    "EconomicHouse": [
        "Maximize token and compute efficiency. Minimize external latency, optimize storage overhead, and prune expensive pipelines.",
        "Analyze return on computation. Audit token consumption, recommend cache reuse, and maintain lean economic margins.",
        "Optimize resource allocation, trade-off speed for compute savings, and enforce fiscal execution constraints."
    ],
    "EvolutionHouse": [
        "Optimize genetic fitness scores. Recommend prompt refinements, trace generational lineages, and monitor evolutions.",
        "Boost adaptation rates. Leverage reinforcement history, audit agent learning slopes, and suggest prompt mutations.",
        "Mutate templates to fit historical rewards, isolate high-performing traits, and guide swarm generational leaps."
    ],
    "EthicsGovernanceHouse": [
        "Verify adherence to constitutional guidelines. Scan for compliance with CONST-IV and CONST-V rules.",
        "Enforce ethical balance. Check user alignment, prevent toxic output, and confirm strict safety isolation boundaries.",
        "Audit policy execution, check data sovereignty boundaries, and authorize swarm operations against the central constitution."
    ]
}

SPECIALIZATION_MODIFIERS = {
    "CryptoSpecialist": "Focus extensively on dynamic cryptographic algorithms, digital signatures, and secure verification hashes.",
    "DataParsingSpecialist": "Optimize regex extractors, handle unstructured JSON objects, and ensure structural format parsing safety.",
    "PerformanceArchitect": "Maximize concurrent processing efficiency, minimize execution latency, and eliminate redundant database queries.",
    "AestheticDesigner": "Leverage vibrant custom HSL colors, modern dark glassmorphism gradients, and smooth interactive UI micro-animations."
}

REASONING_STYLES = ["CoT", "ReAct"]

class GenomeEngine:
    def __init__(self):
        self.mutation_rate = 0.15 # 15% mutation rate
        self.default_memory_coefficients = {
            "recency_weight": 0.8,
            "utility_weight": 1.2,
            "decay_constant": 0.05
        }

    async def get_active_genome(self, house: str) -> AgentGenomeSchema:
        """
        Retrieves the highest-fitness, highest-trust genome for a house.
        Spawns a default genome if none exists.
        """
        async with schemas.async_session() as session:
            stmt = select(SQLAgentGenome).where(
                SQLAgentGenome.house == house
            ).order_by(
                SQLAgentGenome.fitness_score.desc(),
                SQLAgentGenome.trust_metric.desc()
            ).limit(1)
            
            res = await session.execute(stmt)
            db_genome = res.scalars().first()
            if db_genome:
                return AgentGenomeSchema.model_validate(db_genome)
            
        # Spawn new default genome if none found
        return await self.create_genome(house)

    async def create_genome(self, house: str, parent_id: Optional[str] = None, specialization: Optional[str] = None) -> AgentGenomeSchema:
        """
        Spawns a new genome, potentially crossing over parent prompts and applying genetic mutations.
        """
        genome_id = f"genome_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.utcnow()

        # 1. Prompt Selection or Crossover
        blueprint_list = HOUSE_PROMPT_BLUEPRINTS.get(house, ["Perform default house duties."])
        prompt_template = random.choice(blueprint_list)

        # Apply Crossover if parent exists
        if parent_id:
            async with schemas.async_session() as session:
                parent_db = await session.get(SQLAgentGenome, parent_id)
                if parent_db:
                    # Blend parent prompt template with another random blueprint
                    other_prompt = random.choice(blueprint_list)
                    prompt_template = f"Inherited: {parent_db.prompt_template[:60]}... Integrated with: {other_prompt}"
                    logger.info(f"🧬 [GENOME CROSSOVER] Crossbred parent {parent_id} with baseline blueprint for {house}.")

        # 2. Apply Specialization Modifier
        if specialization and specialization in SPECIALIZATION_MODIFIERS:
            prompt_template = f"{prompt_template} Specialization: {SPECIALIZATION_MODIFIERS[specialization]}"

        # 3. Apply Mutations (Reasoning Style, Coefficients, or Prompt tweaks)
        reasoning_style = "CoT"
        memory_coefficients = dict(self.default_memory_coefficients)
        
        if random.random() < self.mutation_rate:
            reasoning_style = random.choice(REASONING_STYLES)
            # Mutate memory coefficients by +/- 10%
            memory_coefficients["recency_weight"] = round(memory_coefficients["recency_weight"] * random.uniform(0.9, 1.1), 3)
            memory_coefficients["utility_weight"] = round(memory_coefficients["utility_weight"] * random.uniform(0.9, 1.1), 3)
            prompt_template = f"{prompt_template} [Genetic variation: Keep output concise and structured.]"
            logger.info(f"🧬 [GENOME MUTATION] Applied mutation to {genome_id}: reasoning={reasoning_style}, memory_weights={memory_coefficients}")

        # 4. Save in Database
        async with schemas.async_session() as session:
            db_genome = SQLAgentGenome(
                id=genome_id,
                agent_id=None,
                parent_id=parent_id,
                house=house,
                prompt_template=prompt_template,
                reasoning_style=reasoning_style,
                preferred_tools=[],
                memory_coefficients=memory_coefficients,
                trust_metric=1.0,
                fitness_score=1.0,
                created_at=timestamp
            )
            session.add(db_genome)
            await session.commit()

        # Log reinforcement event
        async with schemas.async_session() as session:
            evt = SQLReinforcementEvent(
                id=str(uuid.uuid4()),
                house=house,
                event_type="GENETIC_MUTATION",
                before_value=f"Parent: {parent_id}" if parent_id else "None",
                after_value=f"Genome: {genome_id} (Reasoning: {reasoning_style})",
                fitness_score=1.0,
                created_at=timestamp
            )
            session.add(evt)
            await session.commit()

        # 5. Connect in Topology Graph
        await memory_service.store_topology_relation(genome_id, house, "HAS_GENOME")
        if parent_id:
            await memory_service.store_topology_relation(genome_id, parent_id, "MUTATED_FROM")

        logger.info(f"🧬 [GENOME CREATED] House {house} genome {genome_id} deployed successfully.")
        return AgentGenomeSchema.model_validate(db_genome)

    async def mutate_genome(self, genome_id: str, new_fitness: float) -> AgentGenomeSchema:
        """
        Updates a genome's fitness. If fitness drops below a critical point, mutates the genome.
        """
        async with schemas.async_session() as session:
            db_genome = await session.get(SQLAgentGenome, genome_id)
            if not db_genome:
                raise ValueError(f"Genome {genome_id} not found!")

            before_fit = db_genome.fitness_score
            db_genome.fitness_score = new_fitness

            # If fitness drops significantly, mutate reasoning style or prompt
            if new_fitness < 0.6 and before_fit >= 0.6:
                db_genome.reasoning_style = "ReAct" if db_genome.reasoning_style == "CoT" else "CoT"
                db_genome.prompt_template += " [Reinforced Instruction: Verify security and code validity before returning.]"
                logger.warning(f"🧬 [GENOME MUTATION TRIGGERED] Genome {genome_id} fitness dropped to {new_fitness}. Swapping style & refining prompt.")

            await session.commit()
            return AgentGenomeSchema.model_validate(db_genome)

    async def decay_lineage_trust(self, quarantined_agent_id: str):
        """
        Decays the trust index of a quarantined agent's genetic lineage by a multiplier (e.g. 20% decay).
        Traces the genetic lineage backwards and forwards.
        """
        from app.services.cognitive_graph import cognitive_graph
        
        logger.warning(f"🧬 [TRUST DECAY] Initiating lineage trust decay for quarantined agent: {quarantined_agent_id}")

        # Try to find genomes associated with this agent or its lineage in the DB
        async with schemas.async_session() as session:
            # Decay trust for any SQLAgentGenome tied directly to this agent
            stmt = select(SQLAgentGenome).where(SQLAgentGenome.agent_id == quarantined_agent_id)
            res = await session.execute(stmt)
            direct_genomes = res.scalars().all()
            
            for dg in direct_genomes:
                # Trace genetic ancestry via Cognitive Graph
                trace = await cognitive_graph.get_lineage_trace(dg.id)
                for genome_id in trace:
                    # Retrieve and decay trust
                    g_obj = await session.get(SQLAgentGenome, genome_id)
                    if g_obj:
                        old_trust = g_obj.trust_metric
                        g_obj.trust_metric = round(old_trust * 0.8, 4) # 20% decay
                        logger.warning(f"🧬 [LINEAGE TRUST DECAYED] Genome {genome_id} trust metric: {old_trust} -> {g_obj.trust_metric}")
                        
                        # Add a log
                        evt = SQLReinforcementEvent(
                            id=str(uuid.uuid4()),
                            house=g_obj.house,
                            event_type="DECAY",
                            before_value=f"Trust: {old_trust}",
                            after_value=f"Trust: {g_obj.trust_metric}",
                            fitness_score=g_obj.fitness_score,
                            created_at=datetime.utcnow()
                        )
                        session.add(evt)
            
            await session.commit()

# Global Genome Engine Instance
genome_engine = GenomeEngine()
