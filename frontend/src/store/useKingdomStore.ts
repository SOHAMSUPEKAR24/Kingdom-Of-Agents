import { create } from 'zustand';
import { api } from '../utils/api';
import { 
  Task, MemoryItem, Rule, DiscretionaryPermissions, HouseWeights, TopologyData, Log,
  AgentGenome, ToolVersion, KingdomDoctrine, ReinforcementEvent,
  KingValueModel, TrustMetrics, AlignmentAudit, EmotionalWeights, AlignmentDrift, TrustPropagation,
  CognitiveNode, MemoryShard, FederatedGovernor, CivilizationState, NervousReflex,
  CognitiveMutation, DoctrineCompetition, CognitiveGenome, MetaLearningRun, MetaLearningTrends,
  ScientificDiscovery, CausalChain, SimulationBranch, ResearchThesis, ScientificExperiment, ScientificKnowledgeGap
} from '../types';

const getWsUrl = () => {
  if (typeof window !== 'undefined') {
    // Dynamic matching of the current hostname (e.g. localhost or 127.0.0.1)
    let hostname = window.location.hostname;
    if (hostname === 'localhost') hostname = '127.0.0.1';
    const apiBase = process.env.NEXT_PUBLIC_API_URL || `http://${hostname}:8000/api/v1`;
    return apiBase.replace(/^http/, 'ws') + '/stream/cognitive';
  }
  const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';
  return apiBase.replace(/^http/, 'ws') + '/stream/cognitive';
};

interface KingdomStore {
  // State
  tasks: Task[];
  memories: MemoryItem[];
  topology: TopologyData;
  constitutionalRules: Rule[];
  discretionaryPermissions: DiscretionaryPermissions;
  houseWeights: HouseWeights;
  logs: Log[];
  activeObjective: string | null;
  loading: boolean;
  error: string | null;
  isPolling: boolean;
  pollIntervalId: NodeJS.Timeout | null;

  // Phase 3 Cognitive States
  genomes: AgentGenome[];
  tools: ToolVersion[];
  doctrines: KingdomDoctrine[];
  reinforcements: ReinforcementEvent[];
  bayesianFitness: Record<string, number>;
  centrality: Record<string, number>;
  ws: WebSocket | null;

  // Phase 4 Polycognitive States
  debates: any[];
  scenarios: any[];
  hypotheses: any[];
  consensus: any[];

  // Phase 5 Meta-Cognitive States
  worldState: any[];
  thoughtNodes: any[];
  thoughtEdges: any[];
  civilizationDoctrines: any[];
  reflections: any[];
  forecasts: any[];
  stabilityMetrics: any;

  // Phase 6 Alignment & Trust States
  kingValues: KingValueModel[];
  trustMetrics: TrustMetrics[];
  alignmentAudits: AlignmentAudit[];
  emotionalWeights: EmotionalWeights | null;
  alignmentDrift: AlignmentDrift | null;
  trustPropagation: TrustPropagation;

  // Phase 7 Distributed Mesh States
  cognitiveNodes: CognitiveNode[];
  memoryShards: MemoryShard[];
  federatedGovernors: FederatedGovernor[];
  civilizationState: CivilizationState | null;
  nervousReflexes: NervousReflex[];

  // Phase 8: Autonomous Meta-Learning
  cognitiveMutations: CognitiveMutation[];
  doctrineCompetitions: DoctrineCompetition[];
  cognitiveGenomes: CognitiveGenome[];
  metaLearningRuns: MetaLearningRun[];
  metaLearningTrends: MetaLearningTrends;

  // Phase 9: Scientific Cognition
  scientificDiscoveries: ScientificDiscovery[];
  scientificCausalChains: CausalChain[];
  scientificSimulationBranches: SimulationBranch[];
  scientificTheses: ResearchThesis[];
  scientificExperiments: ScientificExperiment[];
  scientificKnowledgeGaps: ScientificKnowledgeGap[];
  scientificComputeBudget: number;

  // Phase 11: Real Infrastructure & Execution Health
  systemHealth: any;

  // Actions
  fetchTasks: () => Promise<void>;
  fetchMemories: (query?: string) => Promise<void>;
  fetchGovernance: () => Promise<void>;
  fetchTopology: () => Promise<void>;
  fetchLogs: () => Promise<void>;
  fetchAllData: () => Promise<void>;
  submitObjective: (objective: string) => Promise<void>;
  togglePermission: (key: string, value: boolean) => Promise<void>;
  startPolling: () => void;
  stopPolling: () => void;
  clearError: () => void;
  connectWebSocket: () => void;
  disconnectWebSocket: () => void;
  triggerRaftElection: () => Promise<void>;
  scaleSwarmNode: (specialization: string) => Promise<void>;
  triggerSimulatedAnomaly: (node_id: string, reason: string) => Promise<void>;
  proposeMutation: (type: string, desc: string, params: Record<string, any>) => Promise<void>;
  triggerTournament: (compA: string, compB: string) => Promise<void>;
  fetchMetaHistory: () => Promise<void>;
  fetchScientificState: () => Promise<void>;
  generateScientificHypotheses: () => Promise<void>;
  triggerScientificExperiment: (hypothesis_id?: string) => Promise<void>;
  voteOnThesis: (thesis_id: string, vote_for?: boolean) => Promise<void>;
}

export const useKingdomStore = create<KingdomStore>((set, get) => ({
  // Initial State
  tasks: [],
  memories: [],
  topology: { nodes: [], edges: [] },
  constitutionalRules: [],
  discretionaryPermissions: {},
  houseWeights: {},
  logs: [],
  activeObjective: null,
  loading: false,
  error: null,
  isPolling: false,
  pollIntervalId: null,

  // Phase 3 Cognitive States
  genomes: [],
  tools: [],
  doctrines: [],
  reinforcements: [],
  bayesianFitness: {},
  centrality: {},
  ws: null,

  // Phase 4 Polycognitive States
  debates: [],
  scenarios: [],
  hypotheses: [],
  consensus: [],

  // Phase 5 Meta-Cognitive States
  worldState: [],
  thoughtNodes: [],
  thoughtEdges: [],
  civilizationDoctrines: [],
  reflections: [],
  forecasts: [],
  stabilityMetrics: { sanity_index: 1.0, contradiction_saturation: 0.0, memory_saturation: 0.0, status: 'STABLE' },

  // Phase 6 Alignment & Trust States
  kingValues: [],
  trustMetrics: [],
  alignmentAudits: [],
  emotionalWeights: null,
  alignmentDrift: null,
  trustPropagation: {},

  // Phase 7 Distributed Mesh States
  cognitiveNodes: [],
  memoryShards: [],
  federatedGovernors: [],
  civilizationState: null,
  nervousReflexes: [],

  // Phase 8: Autonomous Meta-Learning
  cognitiveMutations: [],
  doctrineCompetitions: [],
  cognitiveGenomes: [],
  metaLearningRuns: [],
  metaLearningTrends: { mutational_stability: 1.0, learning_accuracy: 1.0, failure_reduction: 0.0, wisdom_compression: 1.0 },

  // Phase 9: Scientific Cognition
  scientificDiscoveries: [],
  scientificCausalChains: [],
  scientificSimulationBranches: [],
  scientificTheses: [],
  scientificExperiments: [],
  scientificKnowledgeGaps: [],
  scientificComputeBudget: 1000.0,

  // Phase 11
  systemHealth: null,

  // Actions
  fetchTasks: async () => {
    try {
      const tasks = await api.getTasks();
      set({ tasks });
    } catch (err: any) {
      set({ error: `Tasks fetch failed: ${err.message}` });
    }
  },

  fetchMemories: async (query?: string) => {
    try {
      const memories = await api.getMemories(query);
      set({ memories });
    } catch (err: any) {
      set({ error: `Memories query failed: ${err.message}` });
    }
  },

  fetchGovernance: async () => {
    try {
      const gov = await api.getGovernance();
      set({
        constitutionalRules: gov.constitutional_rules,
        discretionaryPermissions: gov.discretionary_permissions,
        houseWeights: gov.house_reinforcement_weights,
      });
    } catch (err: any) {
      set({ error: `Governance state fetch failed: ${err.message}` });
    }
  },

  fetchTopology: async () => {
    try {
      const topology = await api.getTopology();
      set({ topology });
    } catch (err: any) {
      set({ error: `Topology graph fetch failed: ${err.message}` });
    }
  },

  fetchLogs: async () => {
    try {
      const logs = await api.getLogs();
      set({ logs });
    } catch (err: any) {
      set({ error: `Logs stream fetch failed: ${err.message}` });
    }
  },

  fetchAllData: async () => {
    set({ loading: true, error: null });
    try {
      const [tasks, topology, gov, logs, memories, mlData, scientificData, healthData] = await Promise.all([
        api.getTasks(),
        api.getTopology(),
        api.getGovernance(),
        api.getLogs(),
        api.getMemories(),
        api.getMetaHistory().catch(() => ({})),
        api.getScientificState().catch(() => ({ discoveries: [], causal_chains: [], simulation_branches: [], theses: [], experiments: [], knowledge_gaps: [], compute_budget: 1000.0 })),
        api.getSystemHealth().catch(() => null),
      ]);
      set({
        tasks,
        topology,
        constitutionalRules: gov.constitutional_rules,
        discretionaryPermissions: gov.discretionary_permissions,
        houseWeights: gov.house_reinforcement_weights,
        logs,
        memories,
        cognitiveMutations: mlData.mutations || [],
        doctrineCompetitions: mlData.tournaments || [],
        cognitiveGenomes: mlData.genomes || [],
        metaLearningRuns: mlData.runs || [],
        metaLearningTrends: mlData.trends || { mutational_stability: 1.0, learning_accuracy: 1.0, failure_reduction: 0.0, wisdom_compression: 1.0 },
        scientificDiscoveries: scientificData.discoveries || [],
        scientificCausalChains: scientificData.causal_chains || [],
        scientificSimulationBranches: scientificData.simulation_branches || [],
        scientificTheses: scientificData.theses || [],
        scientificExperiments: scientificData.experiments || [],
        scientificKnowledgeGaps: scientificData.knowledge_gaps || [],
        scientificComputeBudget: scientificData.compute_budget || 1000.0,
        systemHealth: healthData,
        loading: false,
      });
    } catch (err: any) {
      set({ error: `System initial load failed: ${err.message}`, loading: false });
    }
  },

  submitObjective: async (objective: string) => {
    set({ loading: true, error: null });
    try {
      // 1. Send the objective to the Knight orchestrator
      const newTasks = await api.submitObjective(objective);
      
      // 2. Fetch everything instantly to capture updated state
      const [tasks, topology, logs] = await Promise.all([
        api.getTasks(),
        api.getTopology(),
        api.getLogs(),
      ]);

      set({
        tasks,
        topology,
        logs,
        activeObjective: objective,
        loading: false,
      });
    } catch (err: any) {
      set({ error: `Objective execution plan failed: ${err.message}`, loading: false });
      throw err;
    }
  },

  togglePermission: async (key: string, value: boolean) => {
    // Save current permission for absolute safety in case of rollback
    const originalPermissions = { ...get().discretionaryPermissions };
    
    // 1. Optimistic Update in UI
    set({
      discretionaryPermissions: {
        ...originalPermissions,
        [key]: value,
      },
    });

    try {
      // 2. Send API Call
      const res = await api.updatePermission(key, value);
      if (!res.success) {
        throw new Error(res.message);
      }
      
      // Refresh logs to capture KingAuthority action log
      const logs = await api.getLogs();
      set({ logs });
    } catch (err: any) {
      // 3. Rollback on Failure
      set({
        discretionaryPermissions: originalPermissions,
        error: `Permission modification failed: ${err.message}. Reverting settings.`,
      });
    }
  },

  startPolling: () => {
    const { isPolling, pollIntervalId } = get();
    if (isPolling || pollIntervalId) return;

    set({ isPolling: true });
    
    // Poll updates every 2 seconds
    const intervalId = setInterval(async () => {
      try {
        const [tasks, topology, logs, gov, healthData] = await Promise.all([
          api.getTasks(),
          api.getTopology(),
          api.getLogs(),
          api.getGovernance(),
          api.getSystemHealth().catch(() => null),
        ]);
        set({
          tasks,
          topology,
          logs,
          constitutionalRules: gov.constitutional_rules,
          discretionaryPermissions: gov.discretionary_permissions,
          houseWeights: gov.house_reinforcement_weights,
          systemHealth: healthData,
        });
      } catch (err) {
        // Silently capture errors during background polling to avoid interrupting UI
        console.warn('Background polling update failed:', err);
      }
    }, 10000);

    set({ pollIntervalId: intervalId });
  },

  stopPolling: () => {
    const { pollIntervalId } = get();
    if (pollIntervalId) {
      clearInterval(pollIntervalId);
    }
    set({ isPolling: false, pollIntervalId: null });
  },

  clearError: () => set({ error: null }),

  connectWebSocket: () => {
    const { ws } = get();
    if (ws) return;

    const wsUrl = getWsUrl();
    console.log(`Connecting to WebSocket stream at: ${wsUrl}`);
    const socket = new WebSocket(wsUrl);

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === 'COGNITIVE_UPDATE') {
          const { 
            genomes, tools, doctrines, reinforcements, house_weights, bayesian_fitness, centrality, topology, 
            debates, scenarios, hypotheses, consensus, 
            world_state, thought_nodes, thought_edges, civilization_doctrines, reflections, forecasts, stability_metrics,
            king_values, trust_metrics, alignment_audits, emotional_weights, alignment_drift, trust_propagation,
            cognitive_nodes, memory_shards, federated_governors, civilization_state, nervous_reflexes,
            cognitive_mutations, doctrine_competitions, cognitive_genomes, meta_learning_runs, meta_learning_trends,
            scientific_discoveries, scientific_causal_chains, scientific_simulation_branches, scientific_theses, scientific_experiments, scientific_knowledge_gaps, scientific_compute_budget
          } = payload.data;
          set({
            genomes,
            tools,
            doctrines,
            reinforcements,
            houseWeights: house_weights,
            bayesianFitness: bayesian_fitness,
            centrality,
            topology,
            debates: debates || [],
            scenarios: scenarios || [],
            hypotheses: hypotheses || [],
            consensus: consensus || [],
            
            // Phase 5
            worldState: world_state || [],
            thoughtNodes: thought_nodes || [],
            thoughtEdges: thought_edges || [],
            civilizationDoctrines: civilization_doctrines || [],
            reflections: reflections || [],
            forecasts: forecasts || [],
            stabilityMetrics: stability_metrics || { sanity_index: 1.0, contradiction_saturation: 0.0, memory_saturation: 0.0, status: 'STABLE' },

            // Phase 6
            kingValues: king_values || [],
            trustMetrics: trust_metrics || [],
            alignmentAudits: alignment_audits || [],
            emotionalWeights: emotional_weights || null,
            alignmentDrift: alignment_drift || null,
            trustPropagation: trust_propagation || {},

            // Phase 7
            cognitiveNodes: cognitive_nodes || [],
            memoryShards: memory_shards || [],
            federatedGovernors: federated_governors || [],
            civilizationState: civilization_state || null,
            nervousReflexes: nervous_reflexes || [],

            // Phase 8
            cognitiveMutations: cognitive_mutations || [],
            doctrineCompetitions: doctrine_competitions || [],
            cognitiveGenomes: cognitive_genomes || [],
            metaLearningRuns: meta_learning_runs || [],
            metaLearningTrends: meta_learning_trends || { mutational_stability: 1.0, learning_accuracy: 1.0, failure_reduction: 0.0, wisdom_compression: 1.0 },

            // Phase 9
            scientificDiscoveries: scientific_discoveries || [],
            scientificCausalChains: scientific_causal_chains || [],
            scientificSimulationBranches: scientific_simulation_branches || [],
            scientificTheses: scientific_theses || [],
            scientificExperiments: scientific_experiments || [],
            scientificKnowledgeGaps: scientific_knowledge_gaps || [],
            scientificComputeBudget: scientific_compute_budget || 1000.0
          });
        }
      } catch (err) {
        console.error('Error handling WebSocket message:', err);
      }
    };

    socket.onclose = (event) => {
      console.log(`WebSocket connection closed. Code: ${event.code}, Reason: ${event.reason}. Retrying connection in 5 seconds...`);
      set({ ws: null });
      setTimeout(() => {
        const currentWs = get().ws;
        if (!currentWs) {
          get().connectWebSocket();
        }
      }, 5000);
    };

    socket.onerror = (err: any) => {
      console.error('WebSocket encountered an error:', err);
      console.error('WebSocket readyState:', socket.readyState);
    };

    set({ ws: socket });
  },

  disconnectWebSocket: () => {
    const { ws } = get();
    if (ws) {
      ws.onclose = null;
      ws.close();
    }
    set({ ws: null });
  },

  triggerRaftElection: async () => {
    try {
      await api.triggerRaftElection();
    } catch (err: any) {
      set({ error: `RAFT Election failed: ${err.message}` });
    }
  },

  scaleSwarmNode: async (specialization: string) => {
    try {
      await api.scaleSwarmNode(specialization);
    } catch (err: any) {
      set({ error: `Node scaling failed: ${err.message}` });
    }
  },

  triggerSimulatedAnomaly: async (node_id: string, reason: string) => {
    try {
      await api.triggerSimulatedAnomaly(node_id, reason);
    } catch (err: any) {
      set({ error: `Simulated anomaly trigger failed: ${err.message}` });
    }
  },

  proposeMutation: async (type: string, desc: string, params: Record<string, any>) => {
    set({ loading: true, error: null });
    try {
      const newMutation = await api.proposeMutation(type, desc, params);
      const currentMutations = get().cognitiveMutations;
      set({
        cognitiveMutations: [newMutation, ...currentMutations],
        loading: false,
      });
    } catch (err: any) {
      set({ error: `Cognitive mutation proposal failed: ${err.message}`, loading: false });
      throw err;
    }
  },

  triggerTournament: async (compA: string, compB: string) => {
    set({ loading: true, error: null });
    try {
      const newTournament = await api.triggerTournament(compA, compB);
      const currentTournaments = get().doctrineCompetitions;
      set({
        doctrineCompetitions: [newTournament, ...currentTournaments],
        loading: false,
      });
    } catch (err: any) {
      set({ error: `Tournament run failed: ${err.message}`, loading: false });
      throw err;
    }
  },

  fetchMetaHistory: async () => {
    try {
      const mlData = await api.getMetaHistory();
      set({
        cognitiveMutations: mlData.mutations || [],
        doctrineCompetitions: mlData.tournaments || [],
        cognitiveGenomes: mlData.genomes || [],
        metaLearningRuns: mlData.runs || [],
        metaLearningTrends: mlData.trends || { mutational_stability: 1.0, learning_accuracy: 1.0, failure_reduction: 0.0, wisdom_compression: 1.0 },
      });
    } catch (err: any) {
      console.warn("Failed fetching meta history:", err);
    }
  },

  fetchScientificState: async () => {
    try {
      const data = await api.getScientificState();
      set({
        scientificDiscoveries: data.discoveries || [],
        scientificCausalChains: data.causal_chains || [],
        scientificSimulationBranches: data.simulation_branches || [],
        scientificTheses: data.theses || [],
        scientificExperiments: data.experiments || [],
        scientificKnowledgeGaps: data.knowledge_gaps || [],
        scientificComputeBudget: data.compute_budget || 1000.0,
      });
    } catch (err: any) {
      console.warn("Failed fetching scientific state:", err);
    }
  },

  generateScientificHypotheses: async () => {
    set({ loading: true, error: null });
    try {
      await api.generateScientificHypotheses();
      const data = await api.getScientificState();
      set({
        scientificDiscoveries: data.discoveries || [],
        scientificCausalChains: data.causal_chains || [],
        scientificSimulationBranches: data.simulation_branches || [],
        scientificTheses: data.theses || [],
        scientificExperiments: data.experiments || [],
        scientificKnowledgeGaps: data.knowledge_gaps || [],
        scientificComputeBudget: data.compute_budget || 1000.0,
        loading: false,
      });
    } catch (err: any) {
      set({ error: `Failed generating hypotheses: ${err.message}`, loading: false });
    }
  },

  triggerScientificExperiment: async (hypothesis_id?: string) => {
    set({ loading: true, error: null });
    try {
      await api.triggerScientificExperiment(hypothesis_id);
      const data = await api.getScientificState();
      set({
        scientificDiscoveries: data.discoveries || [],
        scientificCausalChains: data.causal_chains || [],
        scientificSimulationBranches: data.simulation_branches || [],
        scientificTheses: data.theses || [],
        scientificExperiments: data.experiments || [],
        scientificKnowledgeGaps: data.knowledge_gaps || [],
        scientificComputeBudget: data.compute_budget || 1000.0,
        loading: false,
      });
    } catch (err: any) {
      set({ error: `Failed triggering experiment: ${err.message}`, loading: false });
    }
  },

  voteOnThesis: async (thesis_id: string, vote_for = true) => {
    try {
      await api.voteOnThesis(thesis_id, vote_for);
      const data = await api.getScientificState();
      set({
        scientificDiscoveries: data.discoveries || [],
        scientificCausalChains: data.causal_chains || [],
        scientificSimulationBranches: data.simulation_branches || [],
        scientificTheses: data.theses || [],
        scientificExperiments: data.experiments || [],
        scientificKnowledgeGaps: data.knowledge_gaps || [],
        scientificComputeBudget: data.compute_budget || 1000.0,
      });
    } catch (err: any) {
      set({ error: `Failed voting on thesis: ${err.message}` });
    }
  },
}));

