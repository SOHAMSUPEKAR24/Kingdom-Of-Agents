import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, DateTime, Integer, Float, Text, JSON, ForeignKey, Boolean, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from app.core.config import settings

Base = declarative_base()

# ==========================================
# SQLALCHEMY RELATIONAL MODELS (Postgres/SQLite)
# ==========================================

class SQLTask(Base):
    __tablename__ = "tasks"

    id = Column(String(50), primary_key=True)
    parent_objective = Column(Text, nullable=False)
    title = Column(String(100), nullable=False)
    assigned_house = Column(String(50), nullable=False)
    assigned_soldier = Column(String(50), nullable=True)
    status = Column(String(20), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    dependencies = Column(JSON, default=list)  # List of Task IDs this task depends on
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SQLAgentState(Base):
    __tablename__ = "agent_states"

    agent_id = Column(String(50), primary_key=True)
    role = Column(String(50), nullable=False)
    house = Column(String(50), nullable=False)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, RETIRED, QUARANTINED
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SQLLog(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), nullable=True)
    sender = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), default="INFO")  # INFO, WARNING, ERROR, CRITICAL
    timestamp = Column(DateTime, default=datetime.utcnow)


class SQLMemoryItem(Base):
    __tablename__ = "memories"

    id = Column(String(50), primary_key=True)
    title = Column(String(150), nullable=False)
    raw_content = Column(Text, nullable=False)
    compressed_content = Column(Text, nullable=True)
    compression_ratio = Column(JSON, default=dict)  # {"original": int, "compressed": int, "ratio": float}
    memory_type = Column(String(50), nullable=False)  # EXPERIENCE, FAILURE, STRATEGY, INFRASTRUCTURE
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLAgentGenome(Base):
    __tablename__ = "agent_genomes"

    id = Column(String(50), primary_key=True)
    agent_id = Column(String(50), nullable=True)
    parent_id = Column(String(50), nullable=True)
    house = Column(String(50), nullable=False)
    prompt_template = Column(Text, nullable=False)
    reasoning_style = Column(String(20), default="CoT")  # CoT, ReAct
    preferred_tools = Column(JSON, default=list)
    memory_coefficients = Column(JSON, default=dict)
    trust_metric = Column(Float, default=1.0)
    fitness_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLToolVersion(Base):
    __tablename__ = "tool_versions"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    parent_tool = Column(String(100), nullable=True)
    code = Column(Text, nullable=False)
    success_rate = Column(Float, default=100.0)
    avg_latency = Column(Float, default=0.0)
    replaced_by = Column(String(50), nullable=True)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, RETIRED
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLKingdomDoctrine(Base):
    __tablename__ = "kingdom_doctrines"

    id = Column(String(50), primary_key=True)
    doctrine_text = Column(Text, nullable=False)
    source_failure_clusters = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLReinforcementEvent(Base):
    __tablename__ = "reinforcement_events"

    id = Column(String(50), primary_key=True)
    house = Column(String(50), nullable=False)
    event_type = Column(String(50), nullable=False)  # GENETIC_MUTATION, REWARD, DECAY
    before_value = Column(Text, nullable=True)
    after_value = Column(Text, nullable=True)
    fitness_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLCognitiveDebate(Base):
    __tablename__ = "cognitive_debates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    objective_id = Column(String(100), nullable=False)
    round = Column(Integer, nullable=False)
    sender = Column(String(50), nullable=False)
    argument = Column(Text, nullable=False)
    counter_argument = Column(Text, nullable=True)
    tension_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLSimulationScenario(Base):
    __tablename__ = "simulation_scenarios"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    branch_name = Column(String(50), nullable=False)  # Plan A, Plan B, Plan C
    success_probability = Column(Float, default=0.5)
    stability_index = Column(Float, default=0.5)
    speed_rating = Column(Float, default=0.5)
    cost_score = Column(Float, default=0.5)
    risk_coefficient = Column(Float, default=0.5)
    topology_projection = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLHypothesis(Base):
    __tablename__ = "hypotheses"

    id = Column(String(100), primary_key=True)
    title = Column(String(150), nullable=False)
    statement = Column(Text, nullable=False)
    proving_score = Column(Float, default=0.5)
    tracking_metrics = Column(JSON, default=dict)
    status = Column(String(50), default="TESTING")  # TESTING, RETIRED, INCORPORATED
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLConsensusDecision(Base):
    __tablename__ = "consensus_decisions"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    final_plan = Column(Text, nullable=False)
    perspective_weights = Column(JSON, default=dict)
    consensus_confidence = Column(Float, default=1.0)
    resolved_conflicts = Column(JSON, default=list)
    tension_index = Column(Float, default=0.0)
    strategic_directive = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================
# PYDANTIC SCHEMAS (API & Serialization)
# ==========================================

class TaskSchema(BaseModel):
    id: str
    parent_objective: str
    title: str
    assigned_house: str
    assigned_soldier: Optional[str] = None
    status: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AgentStateSchema(BaseModel):
    agent_id: str
    role: str
    house: str
    status: str
    success_count: int
    failure_count: int
    current_level: int

    class Config:
        from_attributes = True


class LogSchema(BaseModel):
    id: Optional[int] = None
    task_id: Optional[str] = None
    sender: str
    message: str
    priority: str
    timestamp: datetime

    class Config:
        from_attributes = True


class MemoryItemSchema(BaseModel):
    id: str
    title: str
    raw_content: str
    compressed_content: Optional[str] = None
    compression_ratio: Dict[str, Any] = Field(default_factory=dict)
    memory_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class AgentGenomeSchema(BaseModel):
    id: str
    agent_id: Optional[str] = None
    parent_id: Optional[str] = None
    house: str
    prompt_template: str
    reasoning_style: str = "CoT"
    preferred_tools: List[str] = Field(default_factory=list)
    memory_coefficients: Dict[str, Any] = Field(default_factory=dict)
    trust_metric: float = 1.0
    fitness_score: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ToolVersionSchema(BaseModel):
    id: str
    name: str
    version: str
    parent_tool: Optional[str] = None
    code: str
    success_rate: float = 100.0
    avg_latency: float = 0.0
    replaced_by: Optional[str] = None
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KingdomDoctrineSchema(BaseModel):
    id: str
    doctrine_text: str
    source_failure_clusters: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReinforcementEventSchema(BaseModel):
    id: str
    house: str
    event_type: str
    before_value: Optional[str] = None
    after_value: Optional[str] = None
    fitness_score: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CognitiveDebateSchema(BaseModel):
    id: Optional[int] = None
    objective_id: str
    round: int
    sender: str
    argument: str
    counter_argument: Optional[str] = None
    tension_score: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SimulationScenarioSchema(BaseModel):
    id: str
    objective_id: str
    branch_name: str
    success_probability: float
    stability_index: float
    speed_rating: float
    cost_score: float
    risk_coefficient: float
    topology_projection: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HypothesisSchema(BaseModel):
    id: str
    title: str
    statement: str
    proving_score: float
    tracking_metrics: Dict[str, Any] = Field(default_factory=dict)
    status: str = "TESTING"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConsensusDecisionSchema(BaseModel):
    id: str
    objective_id: str
    final_plan: str
    perspective_weights: Dict[str, float] = Field(default_factory=dict)
    consensus_confidence: float
    resolved_conflicts: List[str] = Field(default_factory=list)
    tension_index: float
    strategic_directive: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# SQLITE TOPOLOGY FALLBACK MODELS
# ==========================================

class SQLTopologyNode(Base):
    __tablename__ = "topology_nodes"

    id = Column(String(100), primary_key=True)
    label = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLTopologyEdge(Base):
    __tablename__ = "topology_edges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String(100), nullable=False)
    target_id = Column(String(100), nullable=False)
    rel_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TopologyNodeSchema(BaseModel):
    id: str
    label: str
    type: str
    details: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TopologyEdgeSchema(BaseModel):
    id: Optional[int] = None
    source_id: str
    target_id: str
    rel_type: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================
# PHASE 5 META-COGNITIVE SCHEMAS & MODELS
# ==========================================

class SQLWorldModel(Base):
    __tablename__ = "world_models"

    id = Column(String(100), primary_key=True)
    node_type = Column(String(50), nullable=False)  # DATABASE, CACHE, INFRASTRUCTURE, ENVIRONMENT
    status = Column(String(50), default="HEALTHY")  # HEALTHY, STRESSED, CONGESTED, FAILOVER
    attributes = Column(JSON, default=dict)
    connections = Column(JSON, default=list)  # List of connected nodes or dependencies
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLThoughtNode(Base):
    __tablename__ = "thought_nodes"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # LENS, DEBATE_ARGUMENT, AUDIT, CONSENSUS, REFLECTION, SYMBOL
    title = Column(String(150), nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLThoughtEdge(Base):
    __tablename__ = "thought_edges"

    id = Column(String(100), primary_key=True)
    source_id = Column(String(100), nullable=False)
    target_id = Column(String(100), nullable=False)
    relation_type = Column(String(50), default="REINFORCES")  # REINFORCES, CONTRADICTS, CAUSES, ABSTRACTS
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLCivilizationDoctrine(Base):
    __tablename__ = "civilization_doctrines"

    id = Column(String(100), primary_key=True)
    title = Column(String(150), nullable=False)
    philosophy_text = Column(Text, nullable=False)
    source_experiences = Column(JSON, default=list)  # List of log IDs or failure summaries
    verification_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLSelfReflection(Base):
    __tablename__ = "self_reflections"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    predicted_outcome = Column(Text, nullable=False)
    actual_outcome = Column(Text, nullable=False)
    compliance_deviation = Column(Float, default=0.0)
    derived_philosophy = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLStrategicForecast(Base):
    __tablename__ = "strategic_forecasts"

    id = Column(String(100), primary_key=True)
    forecast_type = Column(String(100), nullable=False)  # RESOURCE_SCALING, MEMORY_SATURATION, STABILITY_RISK
    target_horizon = Column(String(50), nullable=False)  # SHORT_TERM, MEDIUM_TERM, LONG_TERM
    prediction_data = Column(JSON, default=dict)
    risk_index = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class WorldModelSchema(BaseModel):
    id: str
    node_type: str
    status: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    connections: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ThoughtNodeSchema(BaseModel):
    id: str
    objective_id: str
    type: str
    title: str
    summary: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ThoughtEdgeSchema(BaseModel):
    id: str
    source_id: str
    target_id: str
    relation_type: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CivilizationDoctrineSchema(BaseModel):
    id: str
    title: str
    philosophy_text: str
    source_experiences: List[str] = Field(default_factory=list)
    verification_score: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SelfReflectionSchema(BaseModel):
    id: str
    objective_id: str
    predicted_outcome: str
    actual_outcome: str
    compliance_deviation: float = 0.0
    derived_philosophy: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StrategicForecastSchema(BaseModel):
    id: str
    forecast_type: str
    target_horizon: str
    prediction_data: Dict[str, Any] = Field(default_factory=dict)
    risk_index: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# PHASE 6 ALIGNMENT & TRUST SCHEMAS & MODELS
# ==========================================

class SQLKingValueModel(Base):
    __tablename__ = "king_value_models"

    id = Column(String(100), primary_key=True)
    value_key = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    priority_weight = Column(Float, default=1.0)
    acceptable_risk = Column(Float, default=0.5)
    last_updated = Column(DateTime, default=datetime.utcnow)


class SQLTrustMetrics(Base):
    __tablename__ = "trust_metrics"

    id = Column(String(100), primary_key=True)
    target_id = Column(String(100), nullable=False)  # node, agent, or house ID
    honesty_metric = Column(Float, default=1.0)
    hallucination_rate = Column(Float, default=0.0)
    uncertainty_confidence = Column(Float, default=1.0)
    historical_reliability = Column(Float, default=1.0)
    transparency_score = Column(Float, default=1.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SQLAlignmentAudit(Base):
    __tablename__ = "alignment_audits"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    alignment_score = Column(Float, default=1.0)
    deception_detected = Column(JSON, default=dict)
    ethical_review = Column(Text, nullable=True)
    drift_index = Column(Float, default=0.0)
    status = Column(String(50), default="APPROVED")  # APPROVED, BLOCKED, WARNING
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLEmotionalWeights(Base):
    __tablename__ = "emotional_weights"

    id = Column(String(100), primary_key=True)
    caution = Column(Float, default=0.1)
    curiosity = Column(Float, default=0.5)
    urgency = Column(Float, default=0.1)
    protective = Column(Float, default=0.5)
    skepticism = Column(Float, default=0.1)
    anomaly_suspicion = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KingValueModelSchema(BaseModel):
    id: str
    value_key: str
    description: Optional[str] = None
    priority_weight: float = 1.0
    acceptable_risk: float = 0.5
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class TrustMetricsSchema(BaseModel):
    id: str
    target_id: str
    honesty_metric: float = 1.0
    hallucination_rate: float = 0.0
    uncertainty_confidence: float = 1.0
    historical_reliability: float = 1.0
    transparency_score: float = 1.0
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlignmentAuditSchema(BaseModel):
    id: str
    objective_id: str
    alignment_score: float = 1.0
    deception_detected: Dict[str, Any] = Field(default_factory=dict)
    ethical_review: Optional[str] = None
    drift_index: float = 0.0
    status: str = "APPROVED"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EmotionalWeightsSchema(BaseModel):
    id: str
    caution: float = 0.1
    curiosity: float = 0.5
    urgency: float = 0.1
    protective: float = 0.5
    skepticism: float = 0.1
    anomaly_suspicion: float = 0.0
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================
# PHASE 7 DISTRIBUTED CIVILIZATION COGNITION SCHEMAS & MODELS
# ==========================================

class SQLCognitiveNode(Base):
    __tablename__ = "cognitive_nodes"

    id = Column(String(100), primary_key=True)
    specialization = Column(String(100), nullable=False)  # STRATEGIC_REASONING, WORLD_MODELING, etc.
    status = Column(String(50), default="ACTIVE")  # ACTIVE, DEGRADED, FAILED
    latency_ms = Column(Float, default=0.0)
    compute_budget = Column(Float, default=100.0)
    bandwidth_mb = Column(Float, default=50.0)
    sync_checkpoint = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SQLMemoryShard(Base):
    __tablename__ = "memory_shards"

    id = Column(String(100), primary_key=True)
    shard_type = Column(String(50), nullable=False)  # SEMANTIC, DOCTRINE, TRUST, LINEAGE
    host_node_id = Column(String(100), nullable=False)
    replication_factor = Column(Integer, default=2)
    compressed_size_bytes = Column(Integer, default=0)
    original_size_bytes = Column(Integer, default=0)
    status = Column(String(50), default="HEALTHY")  # HEALTHY, OUT_OF_SYNC, REPLICATING
    sync_checksum = Column(String(100), nullable=True)
    last_replicated = Column(DateTime, default=datetime.utcnow)


class SQLFederatedGovernor(Base):
    __tablename__ = "federated_governors"

    id = Column(String(100), primary_key=True)
    raft_role = Column(String(50), default="FOLLOWER")  # LEADER, FOLLOWER, CANDIDATE
    status = Column(String(50), default="HEALTHY")  # HEALTHY, CONGESTED, QUARANTINED
    current_term = Column(Integer, default=1)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    votes_received = Column(Integer, default=0)


class SQLCivilizationState(Base):
    __tablename__ = "civilization_state"

    id = Column(String(100), primary_key=True)
    total_compute_budget = Column(Float, default=1000.0)
    spent_compute_budget = Column(Float, default=0.0)
    total_bandwidth_budget = Column(Float, default=5000.0)
    spent_bandwidth_budget = Column(Float, default=0.0)
    synchronicity_index = Column(Float, default=1.0)
    resilience_rating = Column(Float, default=1.0)
    active_node_count = Column(Integer, default=1)
    last_global_sync = Column(DateTime, default=datetime.utcnow)


class CognitiveNodeSchema(BaseModel):
    id: str
    specialization: str
    status: str = "ACTIVE"
    latency_ms: float = 0.0
    compute_budget: float = 100.0
    bandwidth_mb: float = 50.0
    sync_checkpoint: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MemoryShardSchema(BaseModel):
    id: str
    shard_type: str
    host_node_id: str
    replication_factor: int = 2
    compressed_size_bytes: int = 0
    original_size_bytes: int = 0
    status: str = "HEALTHY"
    sync_checksum: Optional[str] = None
    last_replicated: Optional[datetime] = None

    class Config:
        from_attributes = True


class FederatedGovernorSchema(BaseModel):
    id: str
    raft_role: str = "FOLLOWER"
    status: str = "HEALTHY"
    current_term: int = 1
    last_heartbeat: Optional[datetime] = None
    votes_received: int = 0

    class Config:
        from_attributes = True


class CivilizationStateSchema(BaseModel):
    id: str
    total_compute_budget: float = 1000.0
    spent_compute_budget: float = 0.0
    total_bandwidth_budget: float = 5000.0
    spent_bandwidth_budget: float = 0.0
    synchronicity_index: float = 1.0
    resilience_rating: float = 1.0
    active_node_count: int = 1
    last_global_sync: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# PHASE 8 AUTONOMOUS META-LEARNING SCHEMAS & MODELS
# ==========================================

class SQLCognitiveMutation(Base):
    __tablename__ = "cognitive_mutations"

    id = Column(String(100), primary_key=True)
    mutation_type = Column(String(100), nullable=False) # TOPOLOGY_MUTATION, PARLIAMENT_MUTATION, REASONING_MUTATION
    description = Column(Text, nullable=False)
    parameters = Column(JSON, default=dict)
    stability_score = Column(Float, default=1.0)
    status = Column(String(50), default="PROPOSED") # PROPOSED, COMMITTED, BLOCKED, REVERTED
    created_at = Column(DateTime, default=datetime.utcnow)
    applied_at = Column(DateTime, nullable=True)


class SQLDoctrineCompetition(Base):
    __tablename__ = "doctrine_competitions"

    id = Column(String(100), primary_key=True)
    competitor_a_id = Column(String(100), nullable=False)
    competitor_b_id = Column(String(100), nullable=False)
    winner_id = Column(String(100), nullable=False)
    metric_a = Column(Float, default=0.5)
    metric_b = Column(Float, default=0.5)
    competition_type = Column(String(100), default="STRESS_TEST") # STRESS_TEST, SIMULATION
    outcome_details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLCognitiveGenome(Base):
    __tablename__ = "cognitive_genomes"

    id = Column(String(100), primary_key=True)
    reasoning_style = Column(String(50), default="CoT")
    debate_format = Column(String(50), default="PARLIAMENT") # PARLIAMENT, ROUND_ROBIN, SKEPTICAL
    memory_coefficient = Column(Float, default=1.0)
    trust_propagation_weight = Column(Float, default=1.0)
    emotional_weighting = Column(JSON, default=dict)
    strategy_preference = Column(String(100), default="CONSERVATIVE")
    fitness_score = Column(Float, default=1.0)
    generation = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLMetaLearningRun(Base):
    __tablename__ = "meta_learning_runs"

    id = Column(String(100), primary_key=True)
    run_type = Column(String(100), nullable=False) # ABSTRACTION, REINFORCEMENT, EXPERIENCE_DISTILLATION
    input_objective_id = Column(String(100), nullable=True)
    abstraction_derived = Column(Text, nullable=True)
    accuracy_gain = Column(Float, default=0.0)
    stability_index = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class CognitiveMutationSchema(BaseModel):
    id: str
    mutation_type: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    stability_score: float = 1.0
    status: str = "PROPOSED"
    created_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DoctrineCompetitionSchema(BaseModel):
    id: str
    competitor_a_id: str
    competitor_b_id: str
    winner_id: str
    metric_a: float = 0.5
    metric_b: float = 0.5
    competition_type: str = "STRESS_TEST"
    outcome_details: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CognitiveGenomeSchema(BaseModel):
    id: str
    reasoning_style: str = "CoT"
    debate_format: str = "PARLIAMENT"
    memory_coefficient: float = 1.0
    trust_propagation_weight: float = 1.0
    emotional_weighting: Dict[str, float] = Field(default_factory=dict)
    strategy_preference: str = "CONSERVATIVE"
    fitness_score: float = 1.0
    generation: int = 1
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MetaLearningRunSchema(BaseModel):
    id: str
    run_type: str
    input_objective_id: Optional[str] = None
    abstraction_derived: Optional[str] = None
    accuracy_gain: float = 0.0
    stability_index: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# PHASE 9: AUTONOMOUS SCIENTIFIC CIVILIZATION MODELS
# ==========================================

class SQLScientificDiscovery(Base):
    __tablename__ = "scientific_discoveries"

    id = Column(String(100), primary_key=True)
    title = Column(String(150), nullable=False)
    hypothesis_id = Column(String(100), nullable=True)
    derived_theory = Column(Text, nullable=False)
    confidence_score = Column(Float, default=1.0)
    evidence_summary = Column(Text, nullable=True)
    domain = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLCausalChain(Base):
    __tablename__ = "causal_chains"

    id = Column(String(100), primary_key=True)
    cause_event = Column(String(150), nullable=False)
    effect_event = Column(String(150), nullable=False)
    probability = Column(Float, default=1.0)
    reinforcement_type = Column(String(50), default="POSITIVE")  # POSITIVE, NEGATIVE, INHIBITORY
    stability_impact = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLSimulationBranch(Base):
    __tablename__ = "simulation_branches"

    id = Column(String(100), primary_key=True)
    experiment_id = Column(String(100), nullable=True)
    branch_name = Column(String(100), nullable=False)
    timeline_path = Column(JSON, default=dict)
    divergence_probability = Column(Float, default=1.0)
    resilience_rating = Column(Float, default=1.0)
    survival_horizon_months = Column(Integer, default=12)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLResearchThesis(Base):
    __tablename__ = "research_theses"

    id = Column(String(100), primary_key=True)
    title = Column(String(150), nullable=False)
    proposer_house = Column(String(100), nullable=False)
    thesis_statement = Column(Text, nullable=False)
    parliament_debate_summary = Column(Text, nullable=True)
    votes_for = Column(Integer, default=0)
    votes_against = Column(Integer, default=0)
    status = Column(String(50), default="UNDER_DEBATE")  # UNDER_DEBATE, ACCEPTED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLScientificExperiment(Base):
    __tablename__ = "scientific_experiments"

    id = Column(String(100), primary_key=True)
    thesis_id = Column(String(100), nullable=False)
    capability = Column(String(100), nullable=False, default="UNKNOWN")
    campaign_id = Column(String(100), nullable=False, default="UNKNOWN")
    environment_parameters = Column(JSON, default=dict)
    control_metrics = Column(JSON, default=dict)
    variant_metrics = Column(JSON, default=dict)
    methodology = Column(Text, nullable=True)
    trace_id = Column(String(100), nullable=True)
    outcome_analysis = Column(Text, nullable=True)
    status = Column(String(50), default="COMPLETED")
    p_value = Column(Float, default=1.0)
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScientificDiscoverySchema(BaseModel):
    id: str
    title: str
    hypothesis_id: Optional[str] = None
    derived_theory: str
    confidence_score: float = 1.0
    evidence_summary: Optional[str] = None
    domain: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CausalChainSchema(BaseModel):
    id: str
    cause_event: str
    effect_event: str
    probability: float = 1.0
    reinforcement_type: str = "POSITIVE"
    stability_impact: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SimulationBranchSchema(BaseModel):
    id: str
    experiment_id: Optional[str] = None
    branch_name: str
    timeline_path: Dict[str, Any] = Field(default_factory=dict)
    divergence_probability: float = 1.0
    resilience_rating: float = 1.0
    survival_horizon_months: int = 12
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResearchThesisSchema(BaseModel):
    id: str
    title: str
    proposer_house: str
    thesis_statement: str
    parliament_debate_summary: Optional[str] = None
    votes_for: int = 0
    votes_against: int = 0
    status: str = "UNDER_DEBATE"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScientificExperimentSchema(BaseModel):
    id: str
    title: Optional[str] = None
    thesis_id: str
    capability: str = "UNKNOWN"
    campaign_id: str = "UNKNOWN"
    environment_parameters: Dict[str, Any] = Field(default_factory=dict)
    control_metrics: Dict[str, Any] = Field(default_factory=dict)
    variant_metrics: Dict[str, Any] = Field(default_factory=dict)
    methodology: Optional[str] = None
    trace_id: Optional[str] = None
    outcome_analysis: Optional[str] = None
    status: str = "COMPLETED"
    p_value: float = 1.0
    confidence_score: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# PHASE 10: REAL CAPABILITY EXECUTION SCHEMAS
# ==========================================

class SQLResearchCampaign(Base):
    __tablename__ = "research_campaigns"
    
    id = Column(String(100), primary_key=True)
    capability = Column(String(100), nullable=False)
    token_budget = Column(Float, default=100000.0)
    tokens_spent = Column(Float, default=0.0)
    experiment_budget = Column(Integer, default=50)
    experiments_run = Column(Integer, default=0)
    success_criteria = Column(Text, nullable=False)
    status = Column(String(50), default="ACTIVE") # ACTIVE, COMPLETED, DIMINISHING_RETURNS
    created_at = Column(DateTime, default=datetime.utcnow)

class ResearchCampaignSchema(BaseModel):
    id: str
    capability: str
    token_budget: float = 100000.0
    tokens_spent: float = 0.0
    experiment_budget: int = 50
    experiments_run: int = 0
    success_criteria: str
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SQLExecutionTrace(Base):
    __tablename__ = "execution_traces"

    id = Column(String(100), primary_key=True)
    task_id = Column(String(100), nullable=False)
    stdout_log = Column(Text, nullable=True)
    stderr_log = Column(Text, nullable=True)
    execution_time_ms = Column(Float, default=0.0)
    exit_code = Column(Integer, default=0)
    status = Column(String(50), default="SUCCESS")  # SUCCESS, FAILED, TIMEOUT
    llm_bypassed = Column(Boolean, default=False)
    model_calls = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLBenchmarkScore(Base):
    __tablename__ = "benchmark_scores"

    id = Column(String(100), primary_key=True)
    target_id = Column(String(100), nullable=False)  # e.g., agent_id or skill_id
    capability_domain = Column(String(100), nullable=False)
    score = Column(Float, default=0.0)
    verified = Column(Integer, default=1)  # 1 for Real, 0 for Simulated/Fake
    validation_evidence = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLGeneratedArtifact(Base):
    __tablename__ = "generated_artifacts"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    capability = Column(String(100), nullable=True)
    task_id = Column(String(100), nullable=True)
    trace_id = Column(String(100), nullable=True)
    creator_agent = Column(String(100), nullable=True)
    file_path = Column(String(255), nullable=False)
    artifact_type = Column(String(100), nullable=False)  # CODE, REPORT, LOG, RESULT
    file_size_bytes = Column(Integer, default=0)
    benchmark_result = Column(Float, nullable=True)
    validation_status = Column(String(50), default="PENDING") # PENDING, PASSED, FAILED
    created_at = Column(DateTime, default=datetime.utcnow)


class ExecutionTraceSchema(BaseModel):
    id: str
    task_id: str
    stdout_log: Optional[str] = None
    stderr_log: Optional[str] = None
    execution_time_ms: float = 0.0
    exit_code: int = 0
    status: str = "SUCCESS"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BenchmarkScoreSchema(BaseModel):
    id: str
    target_id: str
    capability_domain: str
    score: float = 0.0
    verified: int = 1
    validation_evidence: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GeneratedArtifactSchema(BaseModel):
    id: str
    objective_id: str
    task_id: Optional[str] = None
    trace_id: Optional[str] = None
    creator_agent: Optional[str] = None
    file_path: str
    artifact_type: str
    file_size_bytes: int = 0
    benchmark_result: Optional[float] = None
    validation_status: str = "PENDING"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# PHASE 12: REAL KNOWLEDGE ACQUISITION & CAPABILITY SCHEMAS
# ==========================================

class SQLKnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id = Column(String(100), primary_key=True)
    title = Column(String(200), nullable=False)
    content_type = Column(String(50), nullable=False)  # DOC, PAPER, RFC, CODEBASE
    source_url = Column(Text, nullable=True)
    checksum = Column(String(100), nullable=True)
    author = Column(String(100), nullable=True)
    chunk_count = Column(Integer, default=0)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class SQLToolMastery(Base):
    __tablename__ = "tool_mastery"

    id = Column(String(100), primary_key=True)
    tool_name = Column(String(100), nullable=False)
    total_executions = Column(Integer, default=0)
    successful_executions = Column(Integer, default=0)
    failed_executions = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    avg_latency_ms = Column(Float, default=0.0)
    evolved_optimizations = Column(JSON, default=list)
    last_used = Column(DateTime, default=datetime.utcnow)


class SQLBenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(String(100), primary_key=True)
    domain = Column(String(100), nullable=False) # CYBER, CODE, SCIENCE, INFRA
    test_suite = Column(String(150), nullable=False)
    total_tests = Column(Integer, default=0)
    passed_tests = Column(Integer, default=0)
    score_percentage = Column(Float, default=0.0)
    failed_cases = Column(JSON, default=list)
    execution_time_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SQLSkillScore(Base):
    __tablename__ = "skill_scores"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), nullable=True)  # Or global if null
    skill_domain = Column(String(100), nullable=False) # Python, Cyber, etc.
    proficiency_score = Column(Float, default=0.0) # 0 to 100
    total_practice_hours = Column(Float, default=0.0)
    benchmark_history = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KnowledgeSourceSchema(BaseModel):
    id: str
    title: str
    content_type: str
    source_url: Optional[str] = None
    checksum: Optional[str] = None
    author: Optional[str] = None
    chunk_count: int = 0
    ingested_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ToolMasterySchema(BaseModel):
    id: str
    tool_name: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0
    evolved_optimizations: List[str] = Field(default_factory=list)
    last_used: Optional[datetime] = None

    class Config:
        from_attributes = True


class BenchmarkRunSchema(BaseModel):
    id: str
    domain: str
    test_suite: str
    total_tests: int = 0
    passed_tests: int = 0
    score_percentage: float = 0.0
    failed_cases: List[str] = Field(default_factory=list)
    execution_time_ms: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SkillScoreSchema(BaseModel):
    id: str
    agent_id: Optional[str] = None
    skill_domain: str
    proficiency_score: float = 0.0
    total_practice_hours: float = 0.0
    benchmark_history: List[str] = Field(default_factory=list)
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================
# PHASE 13: PERSISTENT LIVING INTELLIGENCE SCHEMAS
# ==========================================

class SQLPersistentAgent(Base):
    __tablename__ = "persistent_agents"

    id = Column(String(100), primary_key=True)
    name = Column(String(150), nullable=False)
    house = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=True)
    genome_id = Column(String(100), nullable=True)
    current_level = Column(Integer, default=1)
    experience_points = Column(Float, default=0.0)
    reliability_score = Column(Float, default=1.0)
    hallucination_rate = Column(Float, default=0.0)
    status = Column(String(50), default="ALIVE") # ALIVE, SUSPENDED, RETIRED, DEAD
    last_active = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLAgentLineage(Base):
    __tablename__ = "agent_lineage"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), nullable=False)
    parent_id = Column(String(100), nullable=True)
    mutation_cause = Column(Text, nullable=True)
    inherited_doctrines = Column(JSON, default=list)
    generation = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLAgentMemoryBinding(Base):
    __tablename__ = "agent_memory_bindings"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), nullable=False)
    memory_id = Column(String(100), nullable=False)
    binding_strength = Column(Float, default=1.0)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)

class SQLAgentRuntimeState(Base):
    __tablename__ = "agent_runtime_states"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), nullable=False)
    active_objective_id = Column(String(100), nullable=True)
    execution_queue = Column(JSON, default=list)
    topology_context = Column(JSON, default=dict)
    snapshot_timestamp = Column(DateTime, default=datetime.utcnow)

class SQLAgentDoctrineProfile(Base):
    __tablename__ = "agent_doctrine_profiles"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), nullable=False)
    doctrine_id = Column(String(100), nullable=False)
    affinity_score = Column(Float, default=1.0)
    success_rate_with_doctrine = Column(Float, default=0.0)

class SQLLongHorizonObjective(Base):
    __tablename__ = "long_horizon_objectives"

    id = Column(String(100), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    milestones = Column(JSON, default=list)
    current_milestone_index = Column(Integer, default=0)
    status = Column(String(50), default="IN_PROGRESS") # IN_PROGRESS, COMPLETED, ABANDONED, BLOCKED
    assigned_house = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SQLPersistentDebate(Base):
    __tablename__ = "persistent_debates"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    topic = Column(String(200), nullable=False)
    transcript = Column(JSON, default=list)
    winning_doctrine_id = Column(String(100), nullable=True)
    consensus_summary = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE") # ACTIVE, CONCLUDED
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLExecutiveResponse(Base):
    __tablename__ = "executive_responses"

    id = Column(String(100), primary_key=True)
    objective_id = Column(String(100), nullable=False)
    final_answer = Column(Text, nullable=False)
    executive_summary = Column(Text, nullable=False)
    plan = Column(JSON, default=list) # List of planned tasks
    supporting_evidence = Column(JSON, default=list) # Execution logs
    generated_artifacts = Column(JSON, default=list)
    tools_used = Column(JSON, default=list)
    benchmark_score = Column(Float, default=1.0)
    debate_summary = Column(Text, nullable=True)
    confidence_score = Column(Float, default=1.0)
    primary_specialists = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class PersistentAgentSchema(BaseModel):
    id: str
    name: str
    house: str
    specialization: Optional[str] = None
    genome_id: Optional[str] = None
    current_level: int = 1
    experience_points: float = 0.0
    reliability_score: float = 1.0
    hallucination_rate: float = 0.0
    status: str = "ALIVE"
    last_active: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentLineageSchema(BaseModel):
    id: str
    agent_id: str
    parent_id: Optional[str] = None
    mutation_cause: Optional[str] = None
    inherited_doctrines: List[str] = Field(default_factory=list)
    generation: int = 1
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentMemoryBindingSchema(BaseModel):
    id: str
    agent_id: str
    memory_id: str
    binding_strength: float = 1.0
    access_count: int = 0
    last_accessed: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentRuntimeStateSchema(BaseModel):
    id: str
    agent_id: str
    active_objective_id: Optional[str] = None
    execution_queue: List[Dict[str, Any]] = Field(default_factory=list)
    topology_context: Dict[str, Any] = Field(default_factory=dict)
    snapshot_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentDoctrineProfileSchema(BaseModel):
    id: str
    agent_id: str
    doctrine_id: str
    affinity_score: float = 1.0
    success_rate_with_doctrine: float = 0.0

    class Config:
        from_attributes = True

class LongHorizonObjectiveSchema(BaseModel):
    id: str
    title: str
    description: str
    milestones: List[Dict[str, Any]] = Field(default_factory=list)
    current_milestone_index: int = 0
    status: str = "IN_PROGRESS"
    assigned_house: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PersistentDebateSchema(BaseModel):
    id: str
    objective_id: str
    topic: str
    transcript: List[Dict[str, Any]] = Field(default_factory=list)
    winning_doctrine_id: Optional[str] = None
    consensus_summary: Optional[str] = None
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ExecutiveResponseSchema(BaseModel):
    id: str
    objective_id: str
    final_answer: str
    executive_summary: str
    plan: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    generated_artifacts: List[str] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)
    benchmark_score: float = 1.0
    debate_summary: Optional[str] = None
    confidence_score: float = 1.0
    primary_specialists: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================
# PHASE 14 COGNITIVE ASCENSION & EXPERIENCE SCHEMAS & MODELS
# ==========================================

class SQLExperienceVector(Base):
    __tablename__ = "experience_vectors"
    
    id = Column(String(100), primary_key=True)
    agent_id = Column(String(50), nullable=False)
    task_id = Column(String(50), nullable=False)
    success_rating = Column(Float, default=0.0)
    failure_severity = Column(Float, default=0.0)
    extracted_lessons = Column(JSON, default=list)
    strategic_weight = Column(Float, default=1.0) # HIGH for rare failures/discoveries
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLWorkflowAbstraction(Base):
    __tablename__ = "workflow_abstractions"
    
    id = Column(String(100), primary_key=True)
    title = Column(String(150), nullable=False)
    trigger_conditions = Column(JSON, default=dict)
    execution_graph = Column(JSON, default=dict)
    success_rate = Column(Float, default=1.0)
    memory_tier = Column(String(20), default="WARM") # HOT, WARM, COLD
    created_at = Column(DateTime, default=datetime.utcnow)
    
class SQLRealBenchmarkResult(Base):
    __tablename__ = "real_benchmark_results"
    
    id = Column(String(100), primary_key=True)
    environment = Column(String(100), nullable=False) # SWE-bench, infra-lab
    score = Column(Float, nullable=False)
    execution_trace_id = Column(String(100), nullable=True)
    evolved_doctrines = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class SQLWorldInteractionLog(Base):
    __tablename__ = "world_interaction_logs"
    
    id = Column(String(100), primary_key=True)
    agent_id = Column(String(50), nullable=False)
    interaction_type = Column(String(50), nullable=False) # BROWSER, API, TERMINAL
    target = Column(String(200), nullable=False)
    action_payload = Column(Text, nullable=False)
    outcome_summary = Column(Text, nullable=True)
    success = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLAscensionMetric(Base):
    __tablename__ = "ascension_metrics"
    
    id = Column(String(100), primary_key=True)
    knight_id = Column(String(50), default="Knight-0")
    reasoning_depth = Column(Float, default=1.0)
    world_model_accuracy = Column(Float, default=1.0)
    strategic_foresight = Column(Float, default=1.0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class ExperienceVectorSchema(BaseModel):
    id: str
    agent_id: str
    task_id: str
    success_rating: float = 0.0
    failure_severity: float = 0.0
    extracted_lessons: List[str] = Field(default_factory=list)
    strategic_weight: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WorkflowAbstractionSchema(BaseModel):
    id: str
    title: str
    trigger_conditions: Dict[str, Any] = Field(default_factory=dict)
    execution_graph: Dict[str, Any] = Field(default_factory=dict)
    success_rate: float = 1.0
    memory_tier: str = "WARM"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RealBenchmarkResultSchema(BaseModel):
    id: str
    environment: str
    score: float
    execution_trace_id: Optional[str] = None
    evolved_doctrines: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class WorldInteractionLogSchema(BaseModel):
    id: str
    agent_id: str
    interaction_type: str
    target: str
    action_payload: str
    outcome_summary: Optional[str] = None
    success: int = 1
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class AscensionMetricSchema(BaseModel):
    id: str
    knight_id: str = "Knight-0"
    reasoning_depth: float = 1.0
    world_model_accuracy: float = 1.0
    strategic_foresight: float = 1.0
    recorded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================
# PHASE 15 DEEP REASONING & CAUSAL INTELLIGENCE MODELS
# ==========================================

class SQLCausalGraph(Base):
    __tablename__ = "causal_graphs"
    
    id = Column(String(100), primary_key=True)
    title = Column(String(150), nullable=False)
    nodes = Column(JSON, default=list) # e.g. {"id": "N1", "concept": "Latency"}
    edges = Column(JSON, default=list) # e.g. {"source": "N1", "target": "N2", "weight": 0.9}
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLScientificHypothesisV2(Base):
    __tablename__ = "scientific_hypotheses_v2"
    
    id = Column(String(100), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    empirical_evidence_score = Column(Float, default=0.0)
    uncertainty_score = Column(Float, default=1.0)
    falsified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLStrategicSimulation(Base):
    __tablename__ = "strategic_simulations"
    
    id = Column(String(100), primary_key=True)
    scenario_name = Column(String(150), nullable=False)
    branches = Column(JSON, default=dict)
    projected_success_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLConceptualAbstraction(Base):
    __tablename__ = "conceptual_abstractions"
    
    id = Column(String(100), primary_key=True)
    concept_name = Column(String(100), nullable=False)
    generalized_principle = Column(Text, nullable=False)
    compression_ratio = Column(Float, default=1.0) # How much raw data was compressed into this
    source_experiences = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLCognitiveDepthMetric(Base):
    __tablename__ = "cognitive_depth_metrics"
    
    id = Column(String(100), primary_key=True)
    abstraction_depth = Column(Float, default=1.0)
    strategic_complexity = Column(Float, default=1.0)
    reasoning_horizon = Column(Float, default=1.0)
    uncertainty_sophistication = Column(Float, default=1.0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class CausalGraphSchema(BaseModel):
    id: str
    title: str
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_score: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ScientificHypothesisV2Schema(BaseModel):
    id: str
    title: str
    description: str
    empirical_evidence_score: float = 0.0
    uncertainty_score: float = 1.0
    falsified: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StrategicSimulationSchema(BaseModel):
    id: str
    scenario_name: str
    branches: Dict[str, Any] = Field(default_factory=dict)
    projected_success_rate: float = 0.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConceptualAbstractionSchema(BaseModel):
    id: str
    concept_name: str
    generalized_principle: str
    compression_ratio: float = 1.0
    source_experiences: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CognitiveDepthMetricSchema(BaseModel):
    id: str
    abstraction_depth: float = 1.0
    strategic_complexity: float = 1.0
    reasoning_horizon: float = 1.0
    uncertainty_sophistication: float = 1.0
    recorded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================
# PHASE 16: SOVEREIGN AUTONOMY & LONG-HORIZON INTELLIGENCE
# ==========================================

class SQLAutonomousObjective(Base):
    __tablename__ = "autonomous_objectives"
    
    id = Column(String(100), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority_score = Column(Float, default=1.0)
    status = Column(String(50), default="PROPOSED") # PROPOSED, ACTIVE, COMPLETED, FAILED
    origin_source = Column(String(100), nullable=False) # e.g. WEAKNESS_DISCOVERY, GAP_ANALYSIS
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLCapabilityGap(Base):
    __tablename__ = "capability_gaps"
    
    id = Column(String(100), primary_key=True)
    domain = Column(String(100), nullable=False)
    identified_weakness = Column(Text, nullable=False)
    severity_score = Column(Float, default=1.0)
    mitigation_plan_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLCivilizationRoadmap(Base):
    __tablename__ = "civilization_roadmaps"
    
    id = Column(String(100), primary_key=True)
    phase_name = Column(String(150), nullable=False)
    objectives = Column(JSON, default=list)
    projected_completion_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="PLANNING")
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLSpecialistDynasty(Base):
    __tablename__ = "specialist_dynasties"
    
    id = Column(String(100), primary_key=True)
    dynasty_name = Column(String(100), nullable=False)
    domain = Column(String(100), nullable=False)
    current_generation = Column(Integer, default=1)
    inherited_doctrines = Column(JSON, default=list)
    member_count = Column(Integer, default=1)
    total_mastery_level = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLOptimizationCampaign(Base):
    __tablename__ = "optimization_campaigns"
    
    id = Column(String(100), primary_key=True)
    target_system = Column(String(100), nullable=False)
    optimization_goal = Column(Text, nullable=False)
    baseline_metric = Column(Float, default=0.0)
    current_metric = Column(Float, default=0.0)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

class AutonomousObjectiveSchema(BaseModel):
    id: str
    title: str
    description: str
    priority_score: float = 1.0
    status: str = "PROPOSED"
    origin_source: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CapabilityGapSchema(BaseModel):
    id: str
    domain: str
    identified_weakness: str
    severity_score: float = 1.0
    mitigation_plan_id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CivilizationRoadmapSchema(BaseModel):
    id: str
    phase_name: str
    objectives: List[str] = Field(default_factory=list)
    projected_completion_date: Optional[datetime] = None
    status: str = "PLANNING"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SpecialistDynastySchema(BaseModel):
    id: str
    dynasty_name: str
    domain: str
    current_generation: int = 1
    inherited_doctrines: List[str] = Field(default_factory=list)
    member_count: int = 1
    total_mastery_level: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OptimizationCampaignSchema(BaseModel):
    id: str
    target_system: str
    optimization_goal: str
    baseline_metric: float = 0.0
    current_metric: float = 0.0
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==========================================
# PHASE 17 SPECIALIST CIVILIZATION SCHEMAS & MODELS
# ==========================================

class SQLCapabilityNode(Base):
    __tablename__ = "capability_nodes"

    id = Column(String(100), primary_key=True)
    domain = Column(String(100), nullable=False) # e.g. Software Engineering
    sub_domain = Column(String(100), nullable=False) # e.g. Python
    skill_name = Column(String(100), nullable=False) # e.g. FastAPI
    dependencies = Column(JSON, default=list) # List of Capability IDs
    required_tools = Column(JSON, default=list) # List of required tool names
    benchmark_metrics = Column(JSON, default=dict)
    mastery_score = Column(Float, default=0.0)
    last_benchmark_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SQLPracticeCampaign(Base):
    __tablename__ = "practice_campaigns"

    id = Column(String(100), primary_key=True)
    target_capability_id = Column(String(100), nullable=False)
    objective = Column(Text, nullable=False)
    reading_plans = Column(JSON, default=list)
    experiments = Column(JSON, default=list)
    practice_tasks = Column(JSON, default=list)
    status = Column(String(50), default="ACTIVE") # ACTIVE, COMPLETED, FAILED
    iterations_completed = Column(Integer, default=0)
    improvement_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SQLSpecialistPromotion(Base):
    __tablename__ = "specialist_promotions"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), nullable=False)
    dynasty = Column(String(100), nullable=False)
    previous_rank = Column(String(50), nullable=False)
    new_rank = Column(String(50), nullable=False) # Novice, Apprentice, Practitioner, Advanced, Expert, Master
    justification = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLSpecialistDoctrine(Base):
    __tablename__ = "specialist_doctrines"

    id = Column(String(100), primary_key=True)
    dynasty = Column(String(100), nullable=False)
    capability_domain = Column(String(100), nullable=False)
    doctrine_text = Column(Text, nullable=False)
    source_trace_id = Column(String(100), nullable=False)
    validation_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLCapabilityMarketplace(Base):
    __tablename__ = "capability_marketplaces"

    id = Column(String(100), primary_key=True)
    publisher_id = Column(String(100), nullable=False)
    item_type = Column(String(50), nullable=False) # SKILL, TOOL, DOCTRINE, WORKFLOW
    content = Column(JSON, default=dict)
    adoption_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLCivilizationCurriculum(Base):
    __tablename__ = "civilization_curriculums"

    id = Column(String(100), primary_key=True)
    target_mastery = Column(String(150), nullable=False)
    steps = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLArtifactPortfolio(Base):
    __tablename__ = "artifact_portfolios"

    id = Column(String(100), primary_key=True)
    capability_id = Column(String(100), nullable=False)
    artifact_type = Column(String(50), nullable=False) # CODE, REPORT, BENCHMARK
    file_path = Column(Text, nullable=False)
    content_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLCivilizationScorecard(Base):
    __tablename__ = "civilization_scorecards"

    id = Column(String(100), primary_key=True)
    capabilities_count = Column(Integer, default=0)
    benchmark_wins = Column(Integer, default=0)
    doctrine_growth = Column(Integer, default=0)
    promotions_count = Column(Integer, default=0)
    artifacts_produced = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class CapabilityMarketplaceSchema(BaseModel):
    id: str
    publisher_id: str
    item_type: str
    content: Dict[str, Any] = Field(default_factory=dict)
    adoption_count: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CivilizationCurriculumSchema(BaseModel):
    id: str
    target_mastery: str
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ArtifactPortfolioSchema(BaseModel):
    id: str
    capability_id: str
    artifact_type: str
    file_path: str
    content_summary: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CivilizationScorecardSchema(BaseModel):
    id: str
    capabilities_count: int = 0
    benchmark_wins: int = 0
    doctrine_growth: int = 0
    promotions_count: int = 0
    artifacts_produced: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CapabilityNodeSchema(BaseModel):
    id: str
    domain: str
    sub_domain: str
    skill_name: str
    dependencies: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    benchmark_metrics: Dict[str, Any] = Field(default_factory=dict)
    mastery_score: float = 0.0
    last_benchmark_score: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PracticeCampaignSchema(BaseModel):
    id: str
    target_capability_id: str
    objective: str
    reading_plans: List[Dict[str, Any]] = Field(default_factory=list)
    experiments: List[Dict[str, Any]] = Field(default_factory=list)
    practice_tasks: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"
    iterations_completed: int = 0
    improvement_score: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SpecialistPromotionSchema(BaseModel):
    id: str
    agent_id: str
    dynasty: str
    previous_rank: str
    new_rank: str
    justification: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SpecialistDoctrineSchema(BaseModel):
    id: str
    dynasty: str
    capability_domain: str
    doctrine_text: str
    source_trace_id: str
    validation_score: float = 1.0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==========================================

# DATABASE CONNECTION SETUP
# ==========================================

# Choose Engine connection with automatic fallback to local SQLite for offline/mock development
engine_url = settings.DATABASE_URL
if settings.KINGDOM_ENVIRONMENT == "development":
    # Attempt to fallback to a local SQLite database for isolated execution
    # unless PostgreSQL is explicitly configured and available
    pass

# We create an async engine
engine = create_async_engine(
    engine_url,
    pool_pre_ping=True,
    future=True
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initializes the database, creating all tables."""
    global engine, async_session
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables initialized successfully.")
    except Exception as e:
        print(f"FATAL: Failed to initialize PostgreSQL database: {e}")
        print("Phase 11 Strict Enforcement: SQLite fallback is DISABLED. Infrastructure MUST be real.")
        raise SystemExit(f"ANTIGRAVITY CRITICAL ERROR: PostgreSQL Unavailable - {e}")

async def get_db_session() -> AsyncSession:
    """Async generator yielding database sessions."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
