'use client';

import React, { useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  Activity, ShieldAlert, BrainCircuit, Globe, GitFork, 
  BookOpen, Sparkles, AlertCircle, Compass, History 
} from 'lucide-react';

export default function ThoughtEvolution() {
  const { 
    thoughtNodes, 
    thoughtEdges, 
    worldState, 
    civilizationDoctrines, 
    reflections, 
    forecasts, 
    stabilityMetrics 
  } = useKingdomStore();

  const [selectedBranch, setSelectedBranch] = useState<'Plan A' | 'Plan B' | 'Plan C'>('Plan B');
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  // Helper colors for thought node types
  const getNodeColor = (type: string) => {
    switch (type) {
      case 'LENS': return 'text-cyan-400 border-cyan-500/30 bg-cyan-500/5 shadow-[0_0_10px_rgba(6,182,212,0.15)]';
      case 'DEBATE_ARGUMENT': return 'text-purple-400 border-purple-500/30 bg-purple-500/5 shadow-[0_0_10px_rgba(168,85,247,0.15)]';
      case 'AUDIT': return 'text-amber-400 border-amber-500/30 bg-amber-500/5 shadow-[0_0_10px_rgba(245,158,11,0.15)]';
      case 'CONSENSUS': return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/5 shadow-[0_0_10px_rgba(16,185,129,0.15)]';
      case 'REFLECTION': return 'text-pink-400 border-pink-500/30 bg-pink-500/5 shadow-[0_0_10px_rgba(244,63,94,0.15)]';
      default: return 'text-slate-300 border-slate-500/30 bg-slate-500/5';
    }
  };

  // Branch trade-offs mockup
  const branches = {
    'Plan A': {
      speed: 95, stability: 45, cost: 20, risk: 80,
      description: 'High-concurrency parallel dispatching with raw SQLite write parameters. Extremely fast but susceptible to SQLite concurrency write locks.',
      cascade: ['Parallel Spawns Triggered', 'Concurrency Lock Warning', 'Context Stability Quarantine Isolation']
    },
    'Plan B': {
      speed: 75, stability: 92, cost: 55, risk: 15,
      description: 'Decentralized orchestration mapping with capability analysis limits and sandbox tests. Optimal compromise balancing security and speed.',
      cascade: ['Strategic Parser Check', 'Capabilities Verification', 'Compliance Audit Sandbox', 'Stable Pipeline Dispatch']
    },
    'Plan C': {
      speed: 40, stability: 98, cost: 90, risk: 5,
      description: 'Throttled single-worker sequence with total relational transaction logs and continuous governance verification gates.',
      cascade: ['Strict Serial Enqueue', 'Step-by-Step Transaction Commits', 'Governance Observer Verification']
    }
  };

  const currentBranchData = branches[selectedBranch];

  // Helper to draw circular gauges
  const radius = 38;
  const circumference = 2 * Math.PI * radius;

  return (
    <div className="space-y-8 font-sans">
      
      {/* 1. TOP HEADER SUMMARY */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl backdrop-blur-md bg-white/[0.02] border border-white/5 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-cyan-500/5 blur-3xl rounded-full -mr-20 -mt-20 pointer-events-none" />
        <div className="flex items-center space-x-4 z-10">
          <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center shadow-[0_0_20px_rgba(6,182,212,0.15)]">
            <BrainCircuit className="w-6 h-6 text-cyan-400 animate-pulse" />
          </div>
          <div>
            <h2 className="text-xl font-orbitron font-extrabold tracking-wider text-slate-100 uppercase">
              Thought Evolution Chamber
            </h2>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Recursively self-improving synthetic strategic cognition & internal world models
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2.5 bg-cyan-500/5 border border-cyan-500/10 px-4 py-2 rounded-2xl font-mono text-xxs tracking-wider text-cyan-400 z-10 uppercase">
          <Compass className="w-3.5 h-3.5 animate-spin" /> Sovereign Governor Active
        </div>
      </div>

      {/* 2. THREE-PANEL COGNITIVE DASHBOARD GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* PANEL A: COGNITIVE STABILITY & SANITY METRICS */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 left-0 w-40 h-40 bg-purple-500/5 blur-3xl rounded-full -ml-10 -mt-10 pointer-events-none" />
          
          <div>
            <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-6">
              <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
                <Activity className="w-4 h-4 text-purple-400" /> Stability & Sanity Dashboard
              </span>
              <span className={`text-xxs font-mono px-2 py-0.5 rounded-full border ${
                stabilityMetrics.status === 'STABLE' 
                  ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                  : 'bg-red-500/10 border-red-500/20 text-red-400'
              }`}>
                {stabilityMetrics.status}
              </span>
            </div>

            {/* Circular Gauges Row */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              {/* Sanity Index */}
              <div className="flex flex-col items-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="40" cy="40" r={radius} stroke="rgba(255,255,255,0.03)" strokeWidth="4" fill="transparent" />
                    <circle cx="40" cy="40" r={radius} stroke="#06b6d4" strokeWidth="4" fill="transparent"
                      strokeDasharray={circumference}
                      strokeDashoffset={circumference * (1 - (stabilityMetrics.sanity_index || 1))}
                      className="transition-all duration-1000" />
                  </svg>
                  <span className="absolute text-xs font-mono font-bold text-cyan-400">
                    {Math.round((stabilityMetrics.sanity_index || 1) * 100)}%
                  </span>
                </div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400 mt-2 text-center">
                  Sanity Index
                </span>
              </div>

              {/* Contradiction Saturation */}
              <div className="flex flex-col items-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="40" cy="40" r={radius} stroke="rgba(255,255,255,0.03)" strokeWidth="4" fill="transparent" />
                    <circle cx="40" cy="40" r={radius} stroke="#a855f7" strokeWidth="4" fill="transparent"
                      strokeDasharray={circumference}
                      strokeDashoffset={circumference * (1 - (stabilityMetrics.contradiction_saturation || 0))}
                      className="transition-all duration-1000" />
                  </svg>
                  <span className="absolute text-xs font-mono font-bold text-purple-400">
                    {Math.round((stabilityMetrics.contradiction_saturation || 0) * 100)}%
                  </span>
                </div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400 mt-2 text-center">
                  Contradictions
                </span>
              </div>

              {/* Memory Saturation */}
              <div className="flex flex-col items-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="40" cy="40" r={radius} stroke="rgba(255,255,255,0.03)" strokeWidth="4" fill="transparent" />
                    <circle cx="40" cy="40" r={radius} stroke="#f43f5e" strokeWidth="4" fill="transparent"
                      strokeDasharray={circumference}
                      strokeDashoffset={circumference * (1 - (stabilityMetrics.memory_saturation || 0))}
                      className="transition-all duration-1000" />
                  </svg>
                  <span className="absolute text-xs font-mono font-bold text-rose-400">
                    {Math.round((stabilityMetrics.memory_saturation || 0) * 100)}%
                  </span>
                </div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400 mt-2 text-center">
                  Memory Load
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white/[0.01] border border-white/5 rounded-2xl p-4 font-mono text-[10px] text-slate-400 leading-relaxed space-y-2">
            <div className="flex items-center justify-between border-b border-white/5 pb-1">
              <span className="text-slate-500 font-bold uppercase">Stability Log</span>
              <span className="text-slate-600">UTC REALTIME</span>
            </div>
            {stabilityMetrics.sanity_index < 0.5 ? (
              <div className="text-red-400 flex items-start gap-1">
                <ShieldAlert className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" />
                <span>Recursive overload quarantined: sanity threshold breach isolated.</span>
              </div>
            ) : (
              <div className="text-slate-400 flex items-start gap-1">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400 mt-0.5 flex-shrink-0" />
                <span>Parliament consensus tension balanced. Runaway protection: ENFORCED.</span>
              </div>
            )}
          </div>
        </div>

        {/* PANEL B: EMERGENT SWARM DOCTRINES */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-40 h-40 bg-cyan-500/5 blur-3xl rounded-full -mr-10 -mt-10 pointer-events-none" />
          
          <div>
            <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-4">
              <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-cyan-400" /> Emergent Swarm Doctrines
              </span>
              <span className="text-xxs font-mono text-cyan-500/80">
                {civilizationDoctrines.length} Wisdoms
              </span>
            </div>

            <div className="space-y-4 max-h-[220px] overflow-y-auto scrollbar-thin pr-1">
              {civilizationDoctrines.length > 0 ? (
                civilizationDoctrines.map((doc, idx) => (
                  <div key={doc.id || idx} className="p-3.5 rounded-2xl bg-white/[0.01] border border-white/5 hover:border-white/10 transition group">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="font-orbitron font-bold text-[10px] text-cyan-400 tracking-wider">
                        {doc.title || `Doctrine Synth-${idx+1}`}
                      </span>
                      <span className="text-[9px] font-mono bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 px-1.5 py-0.5 rounded-full">
                        Score {Math.round(doc.verification_score * 100)}%
                      </span>
                    </div>
                    <p className="text-[11px] font-mono text-slate-400 leading-normal">
                      {doc.philosophy_text}
                    </p>
                  </div>
                ))
              ) : (
                <div className="p-4 border border-dashed border-white/5 rounded-2xl text-center">
                  <span className="text-xxs font-mono text-slate-500 block mb-1">NO ACTIVE PHILOSOPHIES</span>
                  <span className="text-[10px] font-mono text-slate-600 block">Doctrines emerge dynamically after objective failure reflections.</span>
                </div>
              )}
            </div>
          </div>

          <div className="text-[9px] font-mono text-slate-500 text-center border-t border-white/5 pt-3 mt-4">
            Doctrines are synthesized from historical outcomes by the Prefrontal Parliament.
          </div>
        </div>

        {/* PANEL C: WORLD STATE CAUSAL MODEL */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 relative overflow-hidden flex flex-col justify-between">
          <div className="absolute bottom-0 right-0 w-40 h-40 bg-amber-500/5 blur-3xl rounded-full -mr-10 -mb-10 pointer-events-none" />
          
          <div>
            <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-4">
              <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
                <Globe className="w-4 h-4 text-amber-500" /> Internal World Model
              </span>
              <span className="text-xxs font-mono text-amber-500/80 uppercase">
                Causal Map
              </span>
            </div>

            <div className="space-y-3.5">
              {worldState.map((node) => (
                <div key={node.id} className="p-3 rounded-2xl bg-white/[0.01] border border-white/5 flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold border ${
                      node.status === 'HEALTHY' 
                        ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.1)]' 
                        : 'bg-amber-500/10 border-amber-500/20 text-amber-400 shadow-[0_0_8px_rgba(245,158,11,0.1)]'
                    }`}>
                      {node.node_type[0]}
                    </div>
                    <div>
                      <span className="text-xxs font-mono font-bold text-slate-200 block">
                        {node.id}
                      </span>
                      <span className="text-[9px] font-mono text-slate-500 block uppercase">
                        {node.node_type} • Connections: {node.connections?.length || 0}
                      </span>
                    </div>
                  </div>
                  <span className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${
                    node.status === 'HEALTHY' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'
                  }`}>
                    {node.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="text-[9px] font-mono text-slate-500 text-center border-t border-white/5 pt-3 mt-4">
            World Models update environment states to predict cascade failures.
          </div>
        </div>

      </div>

      {/* 3. INTERACTIVE ADAPTIVE THOUGHT GRAPH (ATG) */}
      <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/[0.02] blur-3xl rounded-full pointer-events-none" />
        
        <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-6">
          <div>
            <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
              <BrainCircuit className="w-4 h-4 text-cyan-400" /> Adaptive Thought Graph (ATG)
            </span>
            <span className="text-[10px] text-slate-500 font-mono mt-0.5 block">
              Active recursive thought networks displaying arguments, audits, and prefrontal syntheses
            </span>
          </div>
          <div className="text-xxs font-mono text-slate-400 bg-white/5 px-3 py-1 rounded-xl border border-white/5">
            Nodes: {thoughtNodes.length} • Edges: {thoughtEdges.length}
          </div>
        </div>

        {/* Thought Graph Interactive SVG */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-3 border border-white/5 rounded-2xl bg-black/20 relative min-h-[380px] flex items-center justify-center overflow-hidden">
            
            {thoughtNodes.length > 0 ? (
              <svg className="w-full h-[380px] absolute inset-0">
                <defs>
                  <marker id="arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#06b6d4" opacity="0.3" />
                  </marker>
                </defs>

                {/* Draw Edges */}
                {thoughtNodes.map((node, i) => {
                  const x1 = 100 + i * (550 / (thoughtNodes.length - 1 || 1));
                  const y1 = 190 + (i % 2 === 0 ? -60 : 60);

                  const nextNode = thoughtNodes[i + 1];
                  if (!nextNode) return null;
                  const x2 = 100 + (i + 1) * (550 / (thoughtNodes.length - 1 || 1));
                  const y2 = 190 + ((i + 1) % 2 === 0 ? -60 : 60);

                  return (
                    <line key={`edge-${i}`} x1={x1} y1={y1} x2={x2} y2={y2}
                      stroke="rgba(6, 182, 212, 0.25)" strokeWidth="1.5" strokeDasharray="4 3"
                      markerEnd="url(#arrow)" />
                  );
                })}

                {/* Draw Nodes */}
                {thoughtNodes.map((node, i) => {
                  const x = 100 + i * (550 / (thoughtNodes.length - 1 || 1));
                  const y = 190 + (i % 2 === 0 ? -60 : 60);
                  const isHovered = hoveredNode === node.id;

                  return (
                    <g key={node.id} 
                       onMouseEnter={() => setHoveredNode(node.id)}
                       onMouseLeave={() => setHoveredNode(null)}
                       className="cursor-pointer group">
                      <circle cx={x} cy={y} r={isHovered ? 24 : 18} 
                              fill="#030307" 
                              className="transition-all duration-300 stroke-cyan-500/30"
                              strokeWidth={isHovered ? 3 : 1.5} />
                      <circle cx={x} cy={y} r={isHovered ? 12 : 8} 
                              className={`transition-all duration-300 ${
                                node.type === 'CONSENSUS' ? 'fill-emerald-500' :
                                node.type === 'AUDIT' ? 'fill-amber-500' :
                                node.type === 'DEBATE_ARGUMENT' ? 'fill-purple-500' :
                                node.type === 'REFLECTION' ? 'fill-rose-500' : 'fill-cyan-500'
                              }`} />
                      <text x={x} y={y - (isHovered ? 30 : 24)} 
                            textAnchor="middle" 
                            className="fill-slate-200 text-[10px] font-mono uppercase tracking-wider font-bold transition-opacity duration-300"
                            opacity={isHovered ? 1 : 0.6}>
                        {node.type}
                      </text>
                    </g>
                  );
                })}
              </svg>
            ) : (
              <div className="text-center font-mono text-xs text-slate-500">
                <span>Adaptive Thought Graph is idle. Accept a new King command to spawn thought nodes.</span>
              </div>
            )}

            {/* Instruction Legend Overlay */}
            <div className="absolute bottom-4 left-4 right-4 flex justify-between items-center text-[9px] font-mono text-slate-500 bg-[#030307]/80 backdrop-blur border border-white/5 px-3 py-1.5 rounded-xl z-20">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-cyan-400" /> Lens node
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-purple-400" /> Debate node
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-amber-400" /> Audit node
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400" /> Consensus node
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-rose-400" /> Reflection node
              </span>
            </div>
          </div>

          {/* Node Metadata Detail Card */}
          <div className="border border-white/5 rounded-2xl p-5 bg-white/[0.01] flex flex-col justify-between">
            <div>
              <span className="font-orbitron font-bold text-[10px] text-slate-400 block mb-4 uppercase tracking-widest border-b border-white/5 pb-2">
                Thought Node Inspector
              </span>

              {hoveredNode ? (
                (() => {
                  const node = thoughtNodes.find(n => n.id === hoveredNode);
                  if (!node) return null;
                  return (
                    <div className="space-y-4 font-mono">
                      <div>
                        <span className="text-[10px] text-slate-500 uppercase block">Node ID</span>
                        <span className="text-xs text-slate-200 font-bold">{node.id}</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-500 uppercase block">Perspective Type</span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded border inline-block mt-1 ${getNodeColor(node.type)}`}>
                          {node.type}
                        </span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-500 uppercase block">Title</span>
                        <span className="text-xs text-slate-300 font-bold block mt-1 leading-snug">{node.title}</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-500 uppercase block">Audited Summary</span>
                        <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{node.summary}</p>
                      </div>
                    </div>
                  );
                })()
              ) : thoughtNodes.length > 0 ? (
                <div className="text-center py-10">
                  <AlertCircle className="w-8 h-8 text-slate-600 mx-auto mb-2" />
                  <span className="text-[10px] font-mono text-slate-500 block leading-relaxed">
                    Hover over any node in the graph to inspect detailed recursive audits and prefrontal reasoning metadata.
                  </span>
                </div>
              ) : (
                <span className="text-[10px] font-mono text-slate-500 block leading-relaxed">
                  No active thought networks to inspect.
                </span>
              )}
            </div>

            <div className="text-[9px] font-mono text-slate-500 text-center border-t border-white/5 pt-3 mt-4">
              Visualizes real-time thought evolution paths and relationship matrices.
            </div>
          </div>
        </div>
      </div>

      {/* 4. CAUSAL TIMELINE & BRANCH COMPARISON */}
      <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 relative">
        <div className="absolute bottom-0 right-0 w-90 h-90 bg-purple-500/[0.02] blur-3xl rounded-full pointer-events-none" />
        
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-white/5 pb-4 mb-6 gap-4">
          <div>
            <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
              <GitFork className="w-4 h-4 text-purple-400" /> Multi-Timeline Future Simulation
            </span>
            <span className="text-[10px] text-slate-500 font-mono mt-0.5 block">
              Proactive branching simulations of Plan A, Plan B, and Plan C cascading outcomes
            </span>
          </div>

          {/* Tab buttons */}
          <div className="flex bg-white/5 border border-white/5 p-1 rounded-2xl sm:self-center font-mono text-xxs">
            {['Plan A', 'Plan B', 'Plan C'].map((branch) => (
              <button
                key={branch}
                onClick={() => setSelectedBranch(branch as any)}
                className={`px-3 py-1.5 rounded-xl cursor-pointer transition select-none ${
                  selectedBranch === branch 
                    ? 'bg-purple-500/20 text-purple-300 font-bold border border-purple-500/20' 
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {branch}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Branch Trade-off bars */}
          <div className="lg:col-span-1 border border-white/5 rounded-2xl p-5 bg-white/[0.01] space-y-4">
            <span className="font-orbitron font-bold text-[10px] text-slate-400 block border-b border-white/5 pb-2 uppercase tracking-widest">
              Branch Metrics
            </span>
            
            <div className="space-y-4 font-mono text-[10px]">
              {/* Success Prob */}
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">PROBABILITY OF SUCCESS</span>
                  <span className="text-emerald-400 font-bold">{currentBranchData.stability}%</span>
                </div>
                <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 transition-all duration-500" style={{ width: `${currentBranchData.stability}%` }} />
                </div>
              </div>

              {/* Speed */}
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">DISPATCHING VELOCITY</span>
                  <span className="text-cyan-400 font-bold">{currentBranchData.speed}%</span>
                </div>
                <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-cyan-500 transition-all duration-500" style={{ width: `${currentBranchData.speed}%` }} />
                </div>
              </div>

              {/* Resource Cost */}
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">COMPUTE RESOURCE TAX</span>
                  <span className="text-purple-400 font-bold">{currentBranchData.cost}%</span>
                </div>
                <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 transition-all duration-500" style={{ width: `${currentBranchData.cost}%` }} />
                </div>
              </div>

              {/* Risk Factor */}
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">RISK COEFFICIENT</span>
                  <span className="text-rose-400 font-bold">{currentBranchData.risk}%</span>
                </div>
                <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-rose-500 transition-all duration-500" style={{ width: `${currentBranchData.risk}%` }} />
                </div>
              </div>
            </div>
          </div>

          {/* Branch narrative and cascade lane */}
          <div className="lg:col-span-2 border border-white/5 rounded-2xl p-5 bg-white/[0.01] flex flex-col justify-between">
            <div className="space-y-4">
              <span className="font-orbitron font-bold text-[10px] text-slate-400 block border-b border-white/5 pb-2 uppercase tracking-widest">
                Cascading Consequences Timeline
              </span>
              
              <div className="space-y-3">
                <p className="text-xs text-slate-300 font-mono leading-relaxed">
                  {currentBranchData.description}
                </p>
                
                {/* Horizontal timeline cascade chain */}
                <div className="pt-4 flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-2">
                  {currentBranchData.cascade.map((step, idx) => (
                    <React.Fragment key={idx}>
                      <div className="p-3 bg-[#030307] border border-white/5 rounded-xl font-mono text-[10px] text-slate-300 flex items-center gap-2">
                        <span className="w-4 h-4 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center text-[8px] font-bold font-mono">
                          {idx+1}
                        </span>
                        <span>{step}</span>
                      </div>
                      {idx < currentBranchData.cascade.length - 1 && (
                        <div className="hidden sm:block text-slate-600 text-xs font-bold font-mono px-1">➔</div>
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </div>

            <div className="text-[9px] font-mono text-slate-500 text-center border-t border-white/5 pt-3 mt-4">
              Cascade simulations map cause and effect to optimize high-resilience strategies.
            </div>
          </div>
        </div>
      </div>

      {/* 5. HISTORICAL OUTCOMES REFLECTIONS */}
      <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-3xl p-6 relative">
        <div className="absolute top-0 left-0 w-90 h-90 bg-cyan-500/[0.01] blur-3xl rounded-full pointer-events-none" />
        
        <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-6">
          <div>
            <span className="font-orbitron font-bold text-xs uppercase tracking-widest text-slate-300 flex items-center gap-2">
              <History className="w-4 h-4 text-cyan-400" /> Outcomes Reflection Audits
            </span>
            <span className="text-[10px] text-slate-500 font-mono mt-0.5 block">
              Historical audits comparing prefrontal predictions vs actual pipeline outcomes
            </span>
          </div>
        </div>

        <div className="space-y-4 max-h-[300px] overflow-y-auto scrollbar-thin pr-1">
          {reflections.length > 0 ? (
            reflections.map((ref, idx) => (
              <div key={ref.id || idx} className="p-4 rounded-2xl bg-white/[0.01] border border-white/5 flex flex-col md:flex-row md:items-center justify-between gap-4 font-mono text-xxs">
                <div className="space-y-2 max-w-xl">
                  <div className="flex items-center gap-2">
                    <span className="font-orbitron font-bold text-[10px] text-cyan-400 uppercase">
                      Objective {ref.objective_id}
                    </span>
                    <span className={`text-[8px] font-bold px-1.5 py-0.5 rounded uppercase ${
                      ref.compliance_deviation < 0.2 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
                    }`}>
                      Deviation {Math.round(ref.compliance_deviation * 100)}%
                    </span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-slate-400 text-[10px] leading-relaxed">
                    <div>
                      <span className="text-slate-500 block uppercase text-[9px] font-bold">Prediction Estimate</span>
                      <span>{ref.predicted_outcome}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block uppercase text-[9px] font-bold">Actual Workflow Result</span>
                      <span>{ref.actual_outcome}</span>
                    </div>
                  </div>
                  {ref.derived_philosophy && (
                    <div className="border-t border-white/5 pt-2 mt-2">
                      <span className="text-cyan-500/80 block uppercase text-[9px] font-bold">Derived Swarm Philosophy</span>
                      <p className="text-[10px] text-slate-300 leading-normal italic mt-0.5">"{ref.derived_philosophy}"</p>
                    </div>
                  )}
                </div>

                <div className="text-right text-[10px] text-slate-500 flex-shrink-0">
                  <span>AUDITED SUCCESS</span>
                  <div className="text-xs text-slate-300 font-bold block mt-0.5">
                    {ref.created_at ? new Date(ref.created_at).toLocaleTimeString() : 'RECENT'}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="p-8 border border-dashed border-white/5 rounded-3xl text-center">
              <span className="text-xxs font-mono text-slate-500 block mb-1">NO PAST REFLECTIONS</span>
              <span className="text-[10px] font-mono text-slate-600 block">Outcomes reflection logs appear here as soon as objective schedules finish execution.</span>
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
