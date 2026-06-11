import { Task, MemoryItem, GovernanceStatus, TopologyData, Log, CognitiveMutation, DoctrineCompetition, CognitiveGenome, MetaLearningRun, ScientificDiscovery, CausalChain, SimulationBranch, ResearchThesis, ScientificExperiment, ScientificKnowledgeGap } from '../types';

const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || `http://${window.location.hostname}:8000/api/v1`;
  }
  return process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';
};

const API_BASE_URL = getApiBaseUrl();

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
    });

    if (!res.ok) {
      let errorMessage = `HTTP Error ${res.status}`;
      try {
        const errorDetail = await res.json();
        if (errorDetail && errorDetail.detail) {
          errorMessage = errorDetail.detail;
        }
      } catch {
        // Fallback if not JSON
      }
      throw new Error(errorMessage);
    }

    return (await res.json()) as T;
  } catch (error: any) {
    console.error(`API Call failed on ${url}:`, error);
    throw error;
  }
}

export const api = {
  submitObjective: async (objective: string): Promise<Task[]> => {
    return fetchJson<Task[]>('/objective', {
      method: 'POST',
      body: JSON.stringify({ objective }),
    });
  },

  getTasks: async (): Promise<Task[]> => {
    return fetchJson<Task[]>('/tasks');
  },

  getMemories: async (query?: string): Promise<MemoryItem[]> => {
    const endpoint = query ? `/memories?query=${encodeURIComponent(query)}` : '/memories';
    return fetchJson<MemoryItem[]>(endpoint);
  },

  getGovernance: async (): Promise<GovernanceStatus> => {
    return fetchJson<GovernanceStatus>('/governance');
  },

  updatePermission: async (key: string, value: boolean): Promise<{ success: boolean; message: string }> => {
    return fetchJson<{ success: boolean; message: string }>('/governance/permission', {
      method: 'PUT',
      body: JSON.stringify({ key, value }),
    });
  },

  getTopology: async (): Promise<TopologyData> => {
    return fetchJson<TopologyData>('/topology');
  },

  getLogs: async (limit = 100): Promise<Log[]> => {
    return fetchJson<Log[]>(`/observability/logs?limit=${limit}`);
  },

  triggerRaftElection: async (): Promise<{ success: boolean; message: string }> => {
    return fetchJson<{ success: boolean; message: string }>('/distributed/election', {
      method: 'POST',
    });
  },

  scaleSwarmNode: async (specialization: string): Promise<{ success: boolean; node_id: string; message: string }> => {
    return fetchJson<{ success: boolean; node_id: string; message: string }>('/distributed/scale', {
      method: 'POST',
      body: JSON.stringify({ specialization }),
    });
  },

  triggerSimulatedAnomaly: async (node_id: string, reason: string): Promise<{ success: boolean; message: string }> => {
    return fetchJson<{ success: boolean; message: string }>('/distributed/anomaly', {
      method: 'POST',
      body: JSON.stringify({ node_id, reason }),
    });
  },

  proposeMutation: async (mutation_type: string, description: string, parameters: Record<string, any>): Promise<CognitiveMutation> => {
    return fetchJson<CognitiveMutation>('/meta-learning/mutate', {
      method: 'POST',
      body: JSON.stringify({ mutation_type, description, parameters }),
    });
  },

  triggerTournament: async (competitor_a_id: string, competitor_b_id: string): Promise<DoctrineCompetition> => {
    return fetchJson<DoctrineCompetition>('/meta-learning/tournament', {
      method: 'POST',
      body: JSON.stringify({ competitor_a_id, competitor_b_id }),
    });
  },

  getMetaHistory: async (): Promise<any> => {
    return fetchJson<any>('/meta-learning/history');
  },

  generateScientificHypotheses: async (): Promise<{ success: boolean; hypotheses_proposed: number; details: any[] }> => {
    return fetchJson<{ success: boolean; hypotheses_proposed: number; details: any[] }>('/scientific/hypothesis/generate', {
      method: 'POST',
    });
  },

  triggerScientificExperiment: async (hypothesis_id?: string): Promise<{ success: boolean; experiment_id: string; title: string; outcome_analysis?: string; status: string }> => {
    return fetchJson<{ success: boolean; experiment_id: string; title: string; outcome_analysis?: string; status: string }>('/scientific/experiment/trigger', {
      method: 'POST',
      body: JSON.stringify({ hypothesis_id }),
    });
  },

  voteOnThesis: async (thesis_id: string, vote_for = true): Promise<{ success: boolean; thesis_id: string; votes_for: number; votes_against: number; status: string }> => {
    return fetchJson<{ success: boolean; thesis_id: string; votes_for: number; votes_against: number; status: string }>('/scientific/thesis/vote', {
      method: 'POST',
      body: JSON.stringify({ thesis_id, vote_for }),
    });
  },

  getScientificState: async (): Promise<{
    discoveries: ScientificDiscovery[];
    causal_chains: CausalChain[];
    simulation_branches: SimulationBranch[];
    theses: ResearchThesis[];
    experiments: ScientificExperiment[];
    knowledge_gaps: ScientificKnowledgeGap[];
    compute_budget: number;
  }> => {
    return fetchJson<any>('/scientific/state');
  },

  getExecutionTraces: async (): Promise<any[]> => {
    return fetchJson<any[]>('/execution/traces');
  },

  getArtifacts: async (): Promise<any[]> => {
    return fetchJson<any[]>('/artifacts');
  },

  getSystemHealth: async (): Promise<any> => {
    return fetchJson<any>('/health/full');
  },

  getSovereignObjectives: async (): Promise<any[]> => {
    return fetchJson<any[]>('/sovereign/objectives');
  },

  getCapabilityGaps: async (): Promise<any[]> => {
    return fetchJson<any[]>('/sovereign/gaps');
  },

  getCivilizationRoadmaps: async (): Promise<any[]> => {
    return fetchJson<any[]>('/sovereign/roadmaps');
  },

  getSpecialistDynasties: async (): Promise<any[]> => {
    return fetchJson<any[]>('/sovereign/dynasties');
  },

  getExpertiseEvolution: async (): Promise<any> => {
    return fetchJson<any>('/expertise/evolution');
  },

  getMissionOutputs: async (): Promise<any[]> => {
    return fetchJson<any[]>('/mission_outputs');
  },

  getActivityReport: async (): Promise<any> => {
    return fetchJson<any>('/activity_report');
  },
};

