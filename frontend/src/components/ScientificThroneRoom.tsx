import React, { useEffect, useState } from 'react';
import { Microscope, Brain, GitBranch, ShieldAlert } from 'lucide-react';

export default function ScientificThroneRoom() {
  const [graphs, setGraphs] = useState<any[]>([]);
  const [hypotheses, setHypotheses] = useState<any[]>([]);
  const [abstractions, setAbstractions] = useState<any[]>([]);
  const [depthMetrics, setDepthMetrics] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [gRes, hRes, aRes, dRes] = await Promise.all([
          fetch('http://localhost:8000/api/v1/reasoning/causal-graphs').then(r => r.json()),
          fetch('http://localhost:8000/api/v1/reasoning/hypotheses').then(r => r.json()),
          fetch('http://localhost:8000/api/v1/reasoning/abstractions').then(r => r.json()),
          fetch('http://localhost:8000/api/v1/reasoning/depth').then(r => r.json())
        ]);
        
        setGraphs(Array.isArray(gRes) ? gRes : []);
        setHypotheses(Array.isArray(hRes) ? hRes : []);
        setAbstractions(Array.isArray(aRes) ? aRes : []);
        setDepthMetrics(Array.isArray(dRes) ? dRes : []);
      } catch (err) {
        console.error("Failed to fetch deep reasoning state", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 20000);
    return () => clearInterval(interval);
  }, []);

  const currentDepth = depthMetrics[0] || { abstraction_depth: 0, strategic_complexity: 0, reasoning_horizon: 0 };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 border-b border-indigo-500/20 pb-4">
        <Microscope className="w-8 h-8 text-indigo-400" />
        <div>
          <h2 className="text-2xl font-orbitron font-bold text-slate-100">Scientific Throne Room</h2>
          <p className="text-sm font-mono text-slate-400">Deep Sovereign Intelligence & Causal Cognition</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-indigo-500/10 border border-indigo-500/20 p-5 rounded-2xl backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Brain className="w-5 h-5 text-indigo-400" />
            <h3 className="font-orbitron text-indigo-100 font-bold">Cognitive Depth</h3>
          </div>
          <div className="space-y-2 mt-4 font-mono text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Abstraction:</span>
              <span className="text-cyan-400 font-bold">{(currentDepth.abstraction_depth * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Strategic Complexity:</span>
              <span className="text-purple-400 font-bold">{(currentDepth.strategic_complexity * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Reasoning Horizon:</span>
              <span className="text-emerald-400 font-bold">{(currentDepth.reasoning_horizon * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-purple-500/10 border border-purple-500/20 p-5 rounded-2xl backdrop-blur-sm md:col-span-2">
          <div className="flex items-center gap-2 mb-2">
            <ShieldAlert className="w-5 h-5 text-purple-400" />
            <h3 className="font-orbitron text-purple-100 font-bold">Active Hypotheses</h3>
          </div>
          {hypotheses.length === 0 ? (
            <p className="text-slate-500 text-sm italic mt-4">No active hypotheses forming...</p>
          ) : (
            <div className="space-y-3 mt-4 max-h-[150px] overflow-y-auto scrollbar-thin">
              {hypotheses.map(h => (
                <div key={h.id} className="p-3 bg-black/40 rounded border border-white/5 flex justify-between items-center">
                  <div>
                    <div className="text-sm font-bold text-slate-200">{h.title}</div>
                    <div className="text-xs text-slate-400 truncate max-w-sm">{h.description}</div>
                  </div>
                  <div className="text-xs font-mono text-emerald-400">Evid: {h.empirical_evidence_score.toFixed(2)}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-emerald-500/10 border border-emerald-500/20 p-5 rounded-2xl backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <GitBranch className="w-5 h-5 text-emerald-400" />
            <h3 className="font-orbitron text-emerald-100 font-bold">Causal Graphs</h3>
          </div>
          {graphs.length === 0 ? (
            <p className="text-slate-500 text-sm italic mt-4">Awaiting causal derivation...</p>
          ) : (
            <div className="space-y-3 mt-4 max-h-[200px] overflow-y-auto scrollbar-thin">
              {graphs.map(g => (
                <div key={g.id} className="p-3 bg-black/40 rounded border border-emerald-500/20">
                  <div className="text-sm font-bold text-emerald-200">{g.title}</div>
                  <div className="text-xs text-slate-400 mt-1">Nodes: {g.nodes?.length || 0} | Edges: {g.edges?.length || 0}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-cyan-500/10 border border-cyan-500/20 p-5 rounded-2xl backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Brain className="w-5 h-5 text-cyan-400" />
            <h3 className="font-orbitron text-cyan-100 font-bold">Conceptual Abstractions</h3>
          </div>
          {abstractions.length === 0 ? (
            <p className="text-slate-500 text-sm italic mt-4">Compressing heuristics...</p>
          ) : (
            <div className="space-y-3 mt-4 max-h-[200px] overflow-y-auto scrollbar-thin">
              {abstractions.map(a => (
                <div key={a.id} className="p-3 bg-black/40 rounded border border-cyan-500/20">
                  <div className="text-sm font-bold text-cyan-200">{a.concept_name}</div>
                  <div className="text-xs text-slate-300 mt-1">{a.generalized_principle}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
