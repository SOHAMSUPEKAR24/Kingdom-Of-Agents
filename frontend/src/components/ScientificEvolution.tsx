'use client';

import React, { useState, useEffect } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  Beaker, GitBranch, MessageSquare, AlertTriangle, BookOpen, 
  Cpu, Database, Sparkles, ChevronRight, TrendingUp, 
  Play, RefreshCw, Zap, Award, Layers, BarChart2, ShieldAlert
} from 'lucide-react';

export default function ScientificEvolution() {
  const {
    scientificDiscoveries,
    scientificCausalChains,
    scientificSimulationBranches,
    scientificTheses,
    scientificExperiments,
    scientificKnowledgeGaps,
    scientificComputeBudget,
    loading,
    error,
    generateScientificHypotheses,
    triggerScientificExperiment,
    voteOnThesis,
    fetchScientificState
  } = useKingdomStore();

  const [activeSubTab, setActiveSubTab] = useState<'graph' | 'parliament' | 'experiments' | 'archive'>('graph');
  const [selectedThesisId, setSelectedThesisId] = useState<string | null>(null);
  const [selectedExperimentId, setSelectedExperimentId] = useState<string | null>(null);

  // Auto-fetch on mount
  useEffect(() => {
    fetchScientificState();
  }, [fetchScientificState]);

  // Handle generating new hypotheses
  const handleGenerateHypotheses = async () => {
    try {
      await generateScientificHypotheses();
    } catch (err) {
      console.error('Failed generating hypotheses:', err);
    }
  };

  // Handle triggering a new experiment
  const handleTriggerExperiment = async (gapId: string) => {
    try {
      await triggerScientificExperiment(gapId);
      setActiveSubTab('experiments');
    } catch (err) {
      console.error('Failed launching experiment:', err);
    }
  };

  // Handle voting on active theses
  const handleVote = async (thesisId: string, voteFor: boolean) => {
    try {
      await voteOnThesis(thesisId, voteFor);
    } catch (err) {
      console.error('Failed voting on thesis:', err);
    }
  };

  // Parse divergence path details for branches
  const renderPathNodes = (path: Record<string, any>) => {
    return Object.entries(path).map(([key, val]) => (
      <div key={key} className="flex items-start gap-2 p-2 rounded bg-white/[0.01] border border-white/5 font-mono text-[10px]">
        <span className="text-cyan-400 capitalize">{key.replace('_', ' ')}:</span>
        <span className="text-slate-300">{String(val)}</span>
      </div>
    ));
  };

  return (
    <div className="space-y-8 font-sans">
      
      {/* 1. TOP HEADER SUMMARY */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl backdrop-blur-md bg-white/[0.02] border border-white/5 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-emerald-500/5 blur-3xl rounded-full -mr-20 -mt-20 pointer-events-none" />
        <div className="flex items-center space-x-4 z-10">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shadow-[0_0_20px_rgba(16,185,129,0.15)]">
            <Beaker className="w-6 h-6 text-emerald-400 animate-pulse" />
          </div>
          <div>
            <h2 className="text-xl font-orbitron font-extrabold tracking-wider text-slate-100 uppercase">
              🔬 Scientific Evolution Chamber
            </h2>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Phase 9: Scientific reasoning, causal network discovery, future branching simulations & reality auditing
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 z-10">
          <button
            onClick={() => fetchScientificState()}
            className="p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-slate-300 transition duration-200"
            title="Refresh scientific telemetry"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          
          <div className="flex items-center space-x-2.5 bg-emerald-500/5 border border-emerald-500/10 px-4 py-2 rounded-2xl font-mono text-xs tracking-wider text-emerald-400">
            <Cpu className="w-4 h-4" />
            <span>Compute Credits: {scientificComputeBudget.toFixed(1)}</span>
          </div>
        </div>
      </div>

      {/* 2. CORE STATS ROW */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="backdrop-blur-md bg-white/[0.01] border border-white/5 rounded-2xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Active Hypotheses</div>
            <div className="text-xl font-bold font-orbitron text-slate-200 mt-0.5">
              {scientificTheses.filter(t => t.status === 'UNDER_DEBATE').length}
            </div>
          </div>
        </div>

        <div className="backdrop-blur-md bg-white/[0.01] border border-white/5 rounded-2xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <GitBranch className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Causal Nodes</div>
            <div className="text-xl font-bold font-orbitron text-slate-200 mt-0.5">
              {new Set([
                ...scientificCausalChains.map(c => c.cause_event),
                ...scientificCausalChains.map(c => c.effect_event)
              ]).size}
            </div>
          </div>
        </div>

        <div className="backdrop-blur-md bg-white/[0.01] border border-white/5 rounded-2xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Synthesized Doctrines</div>
            <div className="text-xl font-bold font-orbitron text-slate-200 mt-0.5">
              {scientificDiscoveries.length}
            </div>
          </div>
        </div>

        <div className="backdrop-blur-md bg-white/[0.01] border border-white/5 rounded-2xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Lab Experiments</div>
            <div className="text-xl font-bold font-orbitron text-slate-200 mt-0.5">
              {scientificExperiments.length}
            </div>
          </div>
        </div>
      </div>

      {/* 3. ERROR LOG */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-2xl flex items-center gap-3 text-red-400 text-xs font-mono">
          <ShieldAlert className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* 4. MAIN LAYOUT GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* LEFT COLUMN: KNOWLEDGE GAPS & EXPERIMENTS DISPATCH (Col: 4) */}
        <div className="lg:col-span-4 space-y-6">
          <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-400" /> Knowledge Gap Queue
              </span>
              <button
                onClick={handleGenerateHypotheses}
                disabled={loading}
                className="text-[10px] font-mono text-cyan-400 hover:text-cyan-300 bg-cyan-500/10 border border-cyan-500/20 hover:bg-cyan-500/25 px-2 py-1 rounded transition duration-150 disabled:opacity-50"
              >
                Scan Telemetry
              </button>
            </div>

            <div className="space-y-4">
              {scientificKnowledgeGaps.length === 0 ? (
                <div className="text-center py-8 text-slate-500 font-mono text-xs">
                  No gaps identified. Swarm state fully analyzed!
                </div>
              ) : (
                scientificKnowledgeGaps.map((gap) => {
                  const percent = Math.round(gap.uncertainty * 100);
                  const hue = Math.max(0, Math.min(120, (1.0 - gap.uncertainty) * 120));
                  const hslColor = gap.color_indicator || `hsl(${hue}, 85%, 45%)`;
                  
                  return (
                    <div 
                      key={gap.id}
                      className="p-4 border border-white/5 bg-white/[0.01] rounded-2xl space-y-3 hover:bg-white/[0.02] transition"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="space-y-1">
                          <h4 className="text-xs font-bold text-slate-300 leading-snug">{gap.topic}</h4>
                          <span className={`text-[9px] px-2 py-0.5 rounded font-mono ${
                            gap.priority === 'HIGH' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                            gap.priority === 'MEDIUM' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                            'bg-slate-500/10 text-slate-400 border border-slate-500/20'
                          }`}>
                            {gap.priority} PRIORITY
                          </span>
                        </div>
                        <div className="flex flex-col items-end">
                          <span className="text-[10px] font-mono font-bold" style={{ color: hslColor }}>
                            {percent}%
                          </span>
                          <span className="text-[8px] text-slate-500 font-mono tracking-wider">UNCERTAINTY</span>
                        </div>
                      </div>

                      {/* Uncertainty Progress Bar */}
                      <div className="w-full bg-slate-950/60 rounded-full h-1.5 overflow-hidden border border-white/5">
                        <div 
                          className="h-full rounded-full transition-all duration-500" 
                          style={{ width: `${percent}%`, backgroundColor: hslColor }} 
                        />
                      </div>

                      <div className="flex items-center justify-between pt-1">
                        <span className="text-[9px] font-mono text-slate-400">
                          Status: <span className="font-bold uppercase" style={{ color: hslColor }}>{gap.risk_rating || 'NOMINAL'}</span>
                        </span>
                        <button
                          onClick={() => handleTriggerExperiment(gap.id)}
                          disabled={loading}
                          className="flex items-center gap-1 text-[9px] font-mono px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/20 hover:bg-emerald-500/20 text-emerald-400 rounded-lg transition"
                        >
                          <Play className="w-2.5 h-2.5" /> Trigger Lab Exp
                        </button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: INTERACTIVE TABS VIEWPORT (Col: 8) */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Sub Tabs Selector */}
          <div className="flex items-center gap-2 p-1 bg-slate-950/40 border border-white/5 rounded-2xl w-fit">
            {[
              { id: 'graph', label: 'Causal & Timelines', icon: GitBranch },
              { id: 'parliament', label: 'Research Parliament', icon: MessageSquare },
              { id: 'experiments', label: 'Experiment Logs', icon: Beaker },
              { id: 'archive', label: 'Doctrines Archive', icon: BookOpen }
            ].map(tab => {
              const Icon = tab.icon;
              const active = activeSubTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveSubTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl font-orbitron tracking-wider transition ${
                    active 
                      ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 shadow-xl' 
                      : 'text-slate-400 hover:text-slate-200 border border-transparent'
                  }`}
                >
                  <Icon className="w-4 h-4" /> {tab.label}
                </button>
              );
            })}
          </div>

          {/* TAB 1: GLOBAL CAUSAL GRAPH NETWORK & SIMULATOR */}
          {activeSubTab === 'graph' && (
            <div className="grid grid-cols-1 gap-6">
              
              {/* Causal Graph Visualizer */}
              <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 space-y-4">
                <div>
                  <h3 className="font-orbitron font-bold text-sm tracking-wider text-slate-200">Global Causal Graph Network</h3>
                  <p className="text-[10px] text-slate-400 font-mono mt-0.5">Empirically validated structural system-wide dependencies and causal weights</p>
                </div>

                <div className="relative border border-white/5 bg-slate-950/60 rounded-2xl h-[320px] flex items-center justify-center overflow-hidden">
                  <div className="absolute inset-0 bg-radial-gradient from-cyan-500/[0.02] to-transparent pointer-events-none" />
                  
                  {scientificCausalChains.length === 0 ? (
                    <div className="text-center py-12 text-slate-500 font-mono text-xs">
                      No causal relationships indexed yet. Execute tasks to trigger causal learning.
                    </div>
                  ) : (
                    <svg className="w-full h-full p-4" viewBox="0 0 600 280">
                      <defs>
                        <marker id="arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                          <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
                        </marker>
                        <marker id="arrow-positive" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                          <path d="M 0 0 L 10 5 L 0 10 z" fill="#10B981" />
                        </marker>
                        <marker id="arrow-negative" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                          <path d="M 0 0 L 10 5 L 0 10 z" fill="#EF4444" />
                        </marker>
                      </defs>

                      {/* Render links */}
                      {scientificCausalChains.map((chain, idx) => {
                        const count = scientificCausalChains.length;
                        const row = idx % 3;
                        const x1 = 80 + (idx * 90) % 400;
                        const y1 = 60 + row * 60;
                        const x2 = x1 + 100;
                        const y2 = y1 + (idx % 2 === 0 ? 30 : -30);
                        const isPos = chain.reinforcement_type === 'POSITIVE';
                        const strokeColor = isPos ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)';
                        
                        return (
                          <g key={chain.id}>
                            <line 
                              x1={x1} y1={y1} x2={x2} y2={y2}
                              stroke={strokeColor}
                              strokeWidth={2 + chain.probability * 2}
                              strokeDasharray={chain.reinforcement_type === 'INHIBITORY' ? '5,5' : 'none'}
                              markerEnd={`url(#arrow-${isPos ? 'positive' : 'negative'})`}
                              className="transition duration-300"
                            />
                            <text 
                              x={(x1 + x2) / 2} y={(y1 + y2) / 2 - 8}
                              className="fill-slate-400 font-mono text-[8px]"
                              textAnchor="middle"
                            >
                              w: {chain.probability.toFixed(2)}
                            </text>
                          </g>
                        );
                      })}

                      {/* Render nodes */}
                      {Array.from(new Set([
                        ...scientificCausalChains.map(c => c.cause_event),
                        ...scientificCausalChains.map(c => c.effect_event)
                      ])).map((nodeName, idx) => {
                        const x = 100 + (idx * 110) % 420;
                        const y = 80 + (idx % 3) * 60;
                        const hasFailure = nodeName.toLowerCase().includes('fail');
                        
                        return (
                          <g key={nodeName}>
                            <circle 
                              cx={x} cy={y} r="14" 
                              className={`fill-slate-900 stroke-2 ${
                                hasFailure ? 'stroke-red-500/40 fill-red-950/20' : 'stroke-cyan-500/40 fill-cyan-950/20'
                              }`}
                            />
                            <circle cx={x} cy={y} r="6" className={hasFailure ? 'fill-red-400 animate-ping' : 'fill-cyan-400'} />
                            <text 
                              x={x} y={y + 30}
                              className="fill-slate-200 font-mono text-[8px] font-bold"
                              textAnchor="middle"
                            >
                              {nodeName.length > 22 ? nodeName.substring(0, 20) + '...' : nodeName}
                            </text>
                          </g>
                        );
                      })}
                    </svg>
                  )}
                </div>
              </div>

              {/* Branching Future Simulator */}
              <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 space-y-4">
                <div>
                  <h3 className="font-orbitron font-bold text-sm tracking-wider text-slate-200">Branched Futures Simulator</h3>
                  <p className="text-[10px] text-slate-400 font-mono mt-0.5">Civilization survival probability horizons under extreme geopolitical resource stress</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {scientificSimulationBranches.length === 0 ? (
                    <div className="col-span-3 text-center py-6 text-slate-500 font-mono text-xs">
                      No simulation timelines run yet. Execute experiments to trigger path splits.
                    </div>
                  ) : (
                    scientificSimulationBranches.map(branch => {
                      const prob = Math.round(branch.divergence_probability * 100);
                      const resVal = Math.round(branch.resilience_rating * 100);
                      const isHighRisk = branch.resilience_rating < 0.6;
                      
                      return (
                        <div 
                          key={branch.id}
                          className={`p-4 border rounded-2xl relative overflow-hidden bg-slate-950/40 flex flex-col justify-between h-[210px] transition duration-200 ${
                            isHighRisk ? 'border-red-500/10 hover:border-red-500/20' : 'border-emerald-500/10 hover:border-emerald-500/20'
                          }`}
                        >
                          <div className={`absolute top-0 right-0 w-24 h-24 blur-2xl rounded-full pointer-events-none -mr-8 -mt-8 ${
                            isHighRisk ? 'bg-red-500/5' : 'bg-emerald-500/5'
                          }`} />

                          <div className="space-y-2 z-10">
                            <div className="flex items-center justify-between">
                              <span className="text-[8px] font-mono tracking-widest text-slate-400 uppercase">Divergent Branch</span>
                              <span className={`text-[8px] px-1.5 py-0.5 rounded font-mono ${
                                isHighRisk ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                              }`}>
                                {prob}% PROBABILITY
                              </span>
                            </div>

                            <h4 className="text-xs font-bold text-slate-200 font-orbitron">{branch.branch_name}</h4>
                          </div>

                          {/* Branch metrics gauges */}
                          <div className="space-y-3 z-10 py-2">
                            <div className="space-y-1">
                              <div className="flex justify-between text-[8px] font-mono text-slate-400">
                                <span>Resilience Rating</span>
                                <span className={isHighRisk ? 'text-red-400' : 'text-emerald-400'}>{resVal}%</span>
                              </div>
                              <div className="w-full bg-slate-900 rounded-full h-1 overflow-hidden">
                                <div 
                                  className={`h-full rounded-full ${isHighRisk ? 'bg-red-500' : 'bg-emerald-500'}`} 
                                  style={{ width: `${resVal}%` }}
                                />
                              </div>
                            </div>

                            <div className="space-y-1">
                              <div className="flex justify-between text-[8px] font-mono text-slate-400">
                                <span>Survival Horizon</span>
                                <span className="text-cyan-400">{branch.survival_horizon_months} Months</span>
                              </div>
                            </div>
                          </div>

                          <div className="border-t border-white/5 pt-2 mt-2 z-10">
                            <div className="space-y-1">
                              <span className="text-[8px] font-mono text-slate-500 tracking-wider">TIMELINE PATH</span>
                              <div className="space-y-1 max-h-[50px] overflow-y-auto pr-0.5 scrollbar-thin">
                                {renderPathNodes(branch.timeline_path)}
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: RESEARCH PARLIAMENT DEBATE CHAMBER */}
          {activeSubTab === 'parliament' && (
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 space-y-4">
              <div>
                <h3 className="font-orbitron font-bold text-sm tracking-wider text-slate-200">Research Parliament Chamber</h3>
                <p className="text-[10px] text-slate-400 font-mono mt-0.5">Active legislative debates and scientific voting logs of the 8 Research Houses</p>
              </div>

              <div className="space-y-4 max-h-[540px] overflow-y-auto pr-1 scrollbar-thin">
                {scientificTheses.length === 0 ? (
                  <div className="text-center py-12 text-slate-500 font-mono text-xs">
                    No research proposals active. Use "Scan Telemetry" to formulate hypotheses!
                  </div>
                ) : (
                  scientificTheses.map(thesis => {
                    const totalVotes = thesis.votes_for + thesis.votes_against;
                    const forPercent = totalVotes > 0 ? Math.round((thesis.votes_for / totalVotes) * 100) : 50;
                    
                    return (
                      <div 
                        key={thesis.id}
                        className={`p-5 border bg-slate-950/40 rounded-2xl space-y-4 transition ${
                          thesis.status === 'ACCEPTED' ? 'border-emerald-500/10 hover:border-emerald-500/25' :
                          thesis.status === 'REJECTED' ? 'border-red-500/10 hover:border-red-500/25' :
                          'border-white/5 hover:border-white/10'
                        }`}
                      >
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-white/5 pb-3">
                          <div className="space-y-1">
                            <span className="text-[8px] font-mono text-slate-500 uppercase tracking-widest">PROPOSED BY {thesis.proposer_house}</span>
                            <h4 className="text-xs font-bold text-slate-200 leading-snug">{thesis.title}</h4>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className={`text-[8px] px-2 py-0.5 rounded font-mono ${
                              thesis.status === 'ACCEPTED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                              thesis.status === 'REJECTED' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                              'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 animate-pulse'
                            }`}>
                              {thesis.status}
                            </span>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <span className="text-[9px] font-mono text-slate-400 uppercase tracking-wider block">Thesis Statement</span>
                          <p className="text-xs text-slate-300 leading-relaxed font-sans">{thesis.thesis_statement}</p>
                        </div>

                        {thesis.parliament_debate_summary && (
                          <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl space-y-1">
                            <span className="text-[8px] font-mono text-slate-500 tracking-wider">DEBATE SUMMARY</span>
                            <p className="text-[10px] text-slate-400 italic leading-relaxed">{thesis.parliament_debate_summary}</p>
                          </div>
                        )}

                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-2">
                          <div className="flex items-center gap-4 flex-1">
                            <div className="space-y-1 flex-1 max-w-[200px]">
                              <div className="flex justify-between text-[8px] font-mono text-slate-400">
                                <span>Support Quorum</span>
                                <span>{forPercent}% YES</span>
                              </div>
                              <div className="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden flex">
                                <div className="h-full bg-emerald-500 transition-all duration-300" style={{ width: `${forPercent}%` }} />
                                <div className="h-full bg-red-500 transition-all duration-300" style={{ width: `${100 - forPercent}%` }} />
                              </div>
                            </div>

                            <span className="text-[9px] font-mono text-slate-500">
                              Total Votes: {totalVotes}
                            </span>
                          </div>

                          {thesis.status === 'UNDER_DEBATE' && (
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => handleVote(thesis.id, true)}
                                disabled={loading}
                                className="px-3 py-1.5 rounded-lg border border-emerald-500/20 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 text-[10px] font-mono font-bold transition"
                              >
                                VOTE YES
                              </button>
                              <button
                                onClick={() => handleVote(thesis.id, false)}
                                disabled={loading}
                                className="px-3 py-1.5 rounded-lg border border-red-500/20 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-[10px] font-mono font-bold transition"
                              >
                                VOTE NO
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          )}

          {/* TAB 3: CONTROLLED LAB EXPERIMENTS */}
          {activeSubTab === 'experiments' && (
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 space-y-4">
              <div>
                <h3 className="font-orbitron font-bold text-sm tracking-wider text-slate-200">Controlled Lab Experiments</h3>
                <p className="text-[10px] text-slate-400 font-mono mt-0.5">Empirical simulation trials evaluating environmental parameters and control vs variant outcomes</p>
              </div>

              <div className="space-y-4 max-h-[540px] overflow-y-auto pr-1 scrollbar-thin">
                {scientificExperiments.length === 0 ? (
                  <div className="text-center py-12 text-slate-500 font-mono text-xs">
                    No simulation experiment logs available yet. Trigger an experiment from a knowledge gap!
                  </div>
                ) : (
                  scientificExperiments.map(exp => (
                    <div 
                      key={exp.id}
                      className="p-5 border border-white/5 bg-slate-950/40 rounded-2xl space-y-4"
                    >
                      <div className="flex items-center justify-between border-b border-white/5 pb-3">
                        <div className="space-y-1">
                          <span className="text-[8px] font-mono text-slate-500 uppercase tracking-widest">Experiment Run</span>
                          <h4 className="text-xs font-bold text-slate-200 leading-snug">{exp.title}</h4>
                        </div>
                        <span className="text-[8px] px-2 py-0.5 rounded font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {exp.status}
                        </span>
                      </div>

                      {/* Control vs Variant comparison grids */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="p-3.5 bg-slate-950/60 border border-white/5 rounded-xl space-y-2">
                          <span className="text-[8px] font-mono text-slate-500 tracking-wider block uppercase">Control Environment Baseline</span>
                          <div className="space-y-1">
                            {Object.entries(exp.control_metrics).map(([k, v]) => (
                              <div key={k} className="flex justify-between font-mono text-[10px]">
                                <span className="text-slate-400 capitalize">{k.replace(/_/g, ' ')}:</span>
                                <span className="text-slate-300 font-bold">{String(v)}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="p-3.5 bg-emerald-950/10 border border-emerald-500/10 rounded-xl space-y-2">
                          <span className="text-[8px] font-mono text-emerald-500/70 tracking-wider block uppercase">Variant Environment Optimized</span>
                          <div className="space-y-1">
                            {Object.entries(exp.variant_metrics).map(([k, v]) => (
                              <div key={k} className="flex justify-between font-mono text-[10px]">
                                <span className="text-emerald-400/80 capitalize">{k.replace(/_/g, ' ')}:</span>
                                <span className="text-emerald-400 font-bold">{String(v)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      {exp.outcome_analysis && (
                        <div className="p-4 bg-emerald-500/[0.02] border border-emerald-500/10 rounded-xl flex items-start gap-3">
                          <Sparkles className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                          <div className="space-y-1">
                            <span className="text-[8px] font-mono text-emerald-400 tracking-wider">EMPIRICAL OUTCOME ANALYSIS</span>
                            <p className="text-xs text-slate-300 leading-relaxed font-sans">{exp.outcome_analysis}</p>
                          </div>
                        </div>
                      )}

                      <div className="flex items-center justify-between text-[8px] font-mono text-slate-500">
                        <span>Hypothesis Link: {exp.hypothesis_id}</span>
                        <span>Executed: {exp.created_at ? new Date(exp.created_at).toLocaleString() : 'N/A'}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* TAB 4: SCIENTIFIC DISCOVERIES & DOCTRINE ARCHIVE */}
          {activeSubTab === 'archive' && (
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 space-y-4">
              <div>
                <h3 className="font-orbitron font-bold text-sm tracking-wider text-slate-200">Scientific Discoveries & Doctrines</h3>
                <p className="text-[10px] text-slate-400 font-mono mt-0.5">Permanent proved theorems and failure-to-theory derived protective caution guidelines</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[540px] overflow-y-auto pr-1 scrollbar-thin">
                {scientificDiscoveries.length === 0 ? (
                  <div className="col-span-2 text-center py-12 text-slate-500 font-mono text-xs">
                    No permanent doctrines archived yet. Pass active theses in the parliament to synthesize discoveries.
                  </div>
                ) : (
                  scientificDiscoveries.map(disc => {
                    const isGuardrail = disc.domain?.toLowerCase().includes('safety') || disc.domain?.toLowerCase().includes('stability');
                    return (
                      <div 
                        key={disc.id}
                        className={`p-5 border bg-slate-950/40 rounded-2xl flex flex-col justify-between h-[230px] transition duration-200 ${
                          isGuardrail ? 'border-red-500/10 hover:border-red-500/20' : 'border-cyan-500/10 hover:border-cyan-500/20'
                        }`}
                      >
                        <div className="space-y-3">
                          <div className="flex items-start justify-between gap-2">
                            <div className="space-y-1">
                              <span className="text-[8px] font-mono text-slate-500 uppercase tracking-widest">{disc.domain || 'CIVILIZATION DOCTRINE'}</span>
                              <h4 className="text-xs font-bold text-slate-200 leading-snug">{disc.title}</h4>
                            </div>
                            <span className={`text-[9px] px-2 py-0.5 rounded font-mono font-bold ${
                              isGuardrail ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                            }`}>
                              {(disc.confidence_score * 100).toFixed(0)}% CONF
                            </span>
                          </div>

                          <p className="text-[11px] text-slate-300 leading-relaxed font-sans max-h-[90px] overflow-y-auto pr-0.5 scrollbar-thin">{disc.derived_theory}</p>
                        </div>

                        {disc.evidence_summary && (
                          <div className="border-t border-white/5 pt-2.5 mt-2">
                            <span className="text-[8px] font-mono text-slate-500 block tracking-wider">EMPIRICAL PROOF</span>
                            <p className="text-[9px] text-slate-400 italic leading-snug truncate mt-0.5">{disc.evidence_summary}</p>
                          </div>
                        )}
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          )}

        </div>
      </div>

    </div>
  );
}
