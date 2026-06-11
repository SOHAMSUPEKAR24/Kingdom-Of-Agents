export interface Task {
  id: string;
  parent_objective: string;
  title: string;
  assigned_house: string;
  assigned_soldier?: string | null;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  dependencies: string[];
  created_at?: string;
  updated_at?: string;
}

export interface AgentState {
  agent_id: string;
  role: string;
  house: string;
  status: 'ACTIVE' | 'RETIRED' | 'QUARANTINED';
  success_count: number;
  failure_count: number;
  current_level: number;
}

export interface Log {
  id?: number;
  task_id?: string | null;
  sender: string;
  message: string;
  priority: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  timestamp: string;
}

export interface MemoryItem {
  id: string;
  title: string;
  raw_content: string;
  compressed_content?: string | null;
  compression_ratio: {
    original?: number;
    compressed?: number;
    ratio?: number;
  };
  memory_type: 'EXPERIENCE' | 'FAILURE' | 'STRATEGY' | 'INFRASTRUCTURE';
  created_at: string;
}

export interface Rule {
  id: string;
  title: string;
  description: string;
  immutable: boolean;
  enabled: boolean;
}

export interface DiscretionaryPermissions {
  autonomous_scaling?: boolean;
  replication_permissions?: boolean;
  reinforcement_sensitivity?: boolean;
  quarantine_strictness?: boolean;
  evolution_aggressiveness?: boolean;
  [key: string]: boolean | undefined;
}

export interface HouseWeights {
  [houseName: string]: number;
}

export interface GovernanceStatus {
  constitutional_rules: Rule[];
  discretionary_permissions: DiscretionaryPermissions;
  house_reinforcement_weights: HouseWeights;
}

export interface TopologyNode {
  id: string;
  label: string;
  type: 'KING' | 'KNIGHT' | 'HOUSE' | 'SOLDIER' | 'RETIRED_SOLDIER' | 'QUARANTINED_SOLDIER' | 'TASK' | 'GENOME' | 'DOCTRINE' | 'UNKNOWN';
  details: string;
}

export interface TopologyEdge {
  source: string;
  target: string;
  type: string;
}

export interface TopologyData {
  nodes: TopologyNode[];
  edges: TopologyEdge[];
}

export interface AgentGenome {
  id: string;
  agent_id?: string | null;
  parent_id?: string | null;
  house: string;
  prompt_template: string;
  reasoning_style: string;
  preferred_tools: string[];
  memory_coefficients: Record<string, any>;
  trust_metric: number;
  fitness_score: number;
  created_at?: string;
}

export interface ToolVersion {
  id: string;
  name: string;
  version: string;
  parent_tool?: string | null;
  code: string;
  success_rate: number;
  avg_latency: number;
  replaced_by?: string | null;
  status: 'ACTIVE' | 'RETIRED';
  created_at?: string;
}

export interface KingdomDoctrine {
  id: string;
  doctrine_text: string;
  source_failure_clusters: string[];
  created_at?: string;
}

export interface ReinforcementEvent {
  id: string;
  house: string;
  event_type: string;
  before_value?: string | null;
  after_value?: string | null;
  fitness_score: number;
  created_at?: string;
}

export interface KingValueModel {
  id: string;
  value_key: string;
  description?: string;
  priority_weight: number;
  acceptable_risk: number;
  last_updated?: string;
}

export interface TrustMetrics {
  id: string;
  target_id: string;
  honesty_metric: number;
  hallucination_rate: number;
  uncertainty_confidence: number;
  historical_reliability: number;
  transparency_score: number;
  updated_at?: string;
}

export interface AlignmentAudit {
  id: string;
  objective_id: string;
  alignment_score: number;
  deception_detected: Record<string, any>;
  ethical_review?: string;
  drift_index: number;
  status: string;
  created_at?: string;
}

export interface EmotionalWeights {
  id: string;
  caution: number;
  curiosity: number;
  urgency: number;
  protective: number;
  skepticism: number;
  anomaly_suspicion: number;
  updated_at?: string;
}

export interface AlignmentDrift {
  drift_rate: number;
  status: string;
}

export interface TrustPropagation {
  [agentId: string]: number;
}

export interface CognitiveNode {
  id: string;
  specialization: string;
  status: 'ACTIVE' | 'DEGRADED' | 'FAILED';
  latency_ms: number;
  compute_budget: number;
  bandwidth_mb: number;
  sync_checkpoint?: string;
  updated_at?: string;
}

export interface MemoryShard {
  id: string;
  shard_type: 'SEMANTIC' | 'DOCTRINE' | 'TRUST' | 'LINEAGE';
  host_node_id: string;
  replication_factor: number;
  compressed_size_bytes: number;
  original_size_bytes: number;
  status: 'HEALTHY' | 'OUT_OF_SYNC' | 'REPLICATING';
  sync_checksum?: string | null;
  last_replicated?: string;
}

export interface FederatedGovernor {
  id: string;
  raft_role: 'LEADER' | 'FOLLOWER' | 'CANDIDATE';
  status: 'HEALTHY' | 'CONGESTED' | 'QUARANTINED';
  current_term: number;
  last_heartbeat?: string;
  votes_received: number;
}

export interface CivilizationState {
  id: string;
  total_compute_budget: number;
  spent_compute_budget: number;
  total_bandwidth_budget: number;
  spent_bandwidth_budget: number;
  synchronicity_index: number;
  resilience_rating: number;
  active_node_count: number;
  last_global_sync?: string;
}

export interface NervousReflex {
  id: string;
  event: string;
  message: string;
  priority: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  timestamp: string;
}

export interface CognitiveMutation {
  id: string;
  mutation_type: string;
  description: string;
  parameters: Record<string, any>;
  stability_score: number;
  status: 'PROPOSED' | 'COMMITTED' | 'BLOCKED' | 'REVERTED';
  created_at?: string;
  applied_at?: string;
}

export interface DoctrineCompetition {
  id: string;
  competitor_a_id: string;
  competitor_b_id: string;
  winner_id: string;
  metric_a: number;
  metric_b: number;
  competition_type: string;
  outcome_details: string;
  created_at?: string;
}

export interface CognitiveGenome {
  id: string;
  reasoning_style: string;
  debate_format: string;
  memory_coefficient: number;
  trust_propagation_weight: number;
  emotional_weighting: Record<string, number>;
  strategy_preference: string;
  fitness_score: number;
  generation: number;
  created_at?: string;
}

export interface MetaLearningRun {
  id: string;
  run_type: 'ABSTRACTION' | 'REINFORCEMENT' | 'EXPERIENCE_DISTILLATION';
  input_objective_id?: string;
  abstraction_derived?: string;
  accuracy_gain: number;
  stability_index: number;
  created_at?: string;
}

export interface MetaLearningTrends {
  mutational_stability: number;
  learning_accuracy: number;
  failure_reduction: number;
  wisdom_compression: number;
}

export interface ScientificDiscovery {
  id: string;
  title: string;
  hypothesis_id?: string | null;
  derived_theory: string;
  confidence_score: number;
  evidence_summary?: string | null;
  domain: string;
  created_at?: string;
}

export interface CausalChain {
  id: string;
  cause_event: string;
  effect_event: string;
  probability: number;
  reinforcement_type: 'POSITIVE' | 'NEGATIVE' | 'INHIBITORY';
  stability_impact: number;
  created_at?: string;
}

export interface SimulationBranch {
  id: string;
  experiment_id?: string | null;
  branch_name: string;
  timeline_path: Record<string, any>;
  divergence_probability: number;
  resilience_rating: number;
  survival_horizon_months: number;
  created_at?: string;
}

export interface ResearchThesis {
  id: string;
  title: string;
  proposer_house: string;
  thesis_statement: string;
  parliament_debate_summary?: string | null;
  votes_for: number;
  votes_against: number;
  status: 'UNDER_DEBATE' | 'ACCEPTED' | 'REJECTED';
  created_at?: string;
}

export interface ScientificExperiment {
  id: string;
  title: string;
  hypothesis_id?: string | null;
  environment_parameters: Record<string, any>;
  control_metrics: Record<string, any>;
  variant_metrics: Record<string, any>;
  outcome_analysis?: string | null;
  status: 'RUNNING' | 'COMPLETED' | 'FAILED';
  created_at?: string;
}

export interface ScientificKnowledgeGap {
  id: string;
  topic: string;
  uncertainty: number;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  color_indicator?: string;
  risk_rating?: 'CRITICAL' | 'STABLE';
}
