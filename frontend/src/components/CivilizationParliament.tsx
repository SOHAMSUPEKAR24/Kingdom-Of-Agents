'use client';

import React, { useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  MessageSquare, GitFork, Activity, HelpCircle, 
  ArrowRight, ShieldCheck, Flame, Scale, 
  Workflow, Cpu, TrendingUp, AlertTriangle, CheckCircle2 
} from 'lucide-react';

export default function CivilizationParliament() {
  const { debates, scenarios, hypotheses, consensus } = useKingdomStore();
  const [selectedScenario, setSelectedScenario] = useState<string>('Plan B');

  // Grab the latest consensus decision or fallback to mockup values
  const activeConsensus = consensus && consensus.length > 0 ? consensus[0] : {
    final_plan: 'Awaiting parliament session trigger. Enter a high-level directive in the Throne Room to initiate structured cognitive debate and consensus selection.',
    tension_index: 0.45,
    consensus_confidence: 0.85,
    resolved_conflicts: [
      'Vetoed ChaosHouse recommendations bypassing mandatory sandboxed validations.',
      'Calibrated SQLite transaction sequence locks based on SkepticHouse performance queries.'
    ],
    perspective_weights: {
      StrategyHouse: 0.20,
      LogicHouse: 0.15,
      SkepticHouse: 0.12,
      ChaosHouse: 0.05,
      SecurityHouse: 0.13,
      SimulationHouse: 0.10,
      EconomicHouse: 0.10,
      EthicsGovernanceHouse: 0.10,
      EvolutionHouse: 0.03,
      MemoryHouse: 0.02
    },
    strategic_directive: 'STANDBY_CONGRUENCE'
  };

  // Determine dynamic colors based on tension index (0.0 to 1.0)
  const tension = activeConsensus.tension_index;
  let tensionColor = 'text-emerald-400';
  let tensionBorder = 'border-emerald-500/30';
  let tensionBg = 'bg-emerald-500/10';
  let tensionGlow = 'shadow-[0_0_20px_rgba(16,185,129,0.3)]';

  if (tension > 0.7) {
    tensionColor = 'text-rose-500';
    tensionBorder = 'border-rose-500/30';
    tensionBg = 'bg-rose-500/10';
    tensionGlow = 'shadow-[0_0_20px_rgba(244,63,94,0.3)]';
  } else if (tension > 0.4) {
    tensionColor = 'text-amber-500';
    tensionBorder = 'border-amber-500/30';
    tensionBg = 'bg-amber-500/10';
    tensionGlow = 'shadow-[0_0_20px_rgba(245,158,11,0.3)]';
  }

  // Map of tailored HSL badges for House senders in debate
  const getHouseStyle = (house: string) => {
    switch (house) {
      case 'StrategyHouse':
        return 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30';
      case 'LogicHouse':
        return 'bg-blue-500/10 text-blue-400 border border-blue-500/30';
      case 'ChaosHouse':
        return 'bg-rose-500/10 text-rose-400 border border-rose-500/30';
      case 'SkepticHouse':
        return 'bg-amber-500/10 text-amber-400 border border-amber-500/30';
      case 'EconomicHouse':
        return 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30';
      case 'EthicsGovernanceHouse':
        return 'bg-purple-500/10 text-purple-400 border border-purple-500/30';
      case 'SimulationHouse':
        return 'bg-violet-500/10 text-violet-400 border border-violet-500/30';
      case 'SecurityHouse':
        return 'bg-red-500/10 text-red-400 border border-red-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border border-slate-500/30';
    }
  };

  const activeScenarioData = scenarios.find(s => s.branch_name === selectedScenario) || 
    (selectedScenario === 'Plan A' ? {
      branch_name: 'Plan A',
      success_probability: 0.65,
      stability_index: 0.40,
      speed_rating: 0.95,
      cost_score: 0.30,
      risk_coefficient: 0.85,
      topology_projection: {
        nodes: [{ id: 'StrategyHouse' }, { id: 'EngineeringHouse' }],
        edges: [{ source: 'StrategyHouse', target: 'EngineeringHouse' }]
      }
    } : selectedScenario === 'Plan B' ? {
      branch_name: 'Plan B',
      success_probability: 0.90,
      stability_index: 0.85,
      speed_rating: 0.70,
      cost_score: 0.80,
      risk_coefficient: 0.25,
      topology_projection: {
        nodes: [{ id: 'StrategyHouse' }, { id: 'SecurityHouse' }, { id: 'EngineeringHouse' }, { id: 'MemoryHouse' }],
        edges: [
          { source: 'StrategyHouse', target: 'SecurityHouse' },
          { source: 'SecurityHouse', target: 'EngineeringHouse' },
          { source: 'EngineeringHouse', target: 'MemoryHouse' }
        ]
      }
    } : {
      branch_name: 'Plan C',
      success_probability: 0.85,
      stability_index: 0.90,
      speed_rating: 0.45,
      cost_score: 0.50,
      risk_coefficient: 0.30,
      topology_projection: {
        nodes: [{ id: 'StrategyHouse' }, { id: 'ResearchHouse' }, { id: 'LogicHouse' }, { id: 'EngineeringHouse' }, { id: 'EthicsGovernanceHouse' }],
        edges: [
          { source: 'StrategyHouse', target: 'ResearchHouse' },
          { source: 'ResearchHouse', target: 'LogicHouse' },
          { source: 'LogicHouse', target: 'EngineeringHouse' },
          { source: 'EngineeringHouse', target: 'EthicsGovernanceHouse' }
        ]
      }
    });

  return (
    <div className="space-y-6">
      
      {/* SECTION 1: SUPREME PARLIAMENT HEADING */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl">
        <div className="flex items-center space-x-3.5">
          <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.3)]">
            <Workflow className="w-6 h-6 text-violet-400 animate-pulse" />
          </div>
          <div>
            <h2 className="font-orbitron text-lg font-bold tracking-wider text-slate-100 uppercase">
              Civilization Parliament
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              Recursive meta-cognition debates, scenario tree branches, and dynamic consensus alignment
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xxs font-mono bg-violet-500/10 text-violet-400 border border-violet-500/20 px-3 py-1 rounded-full uppercase tracking-wider font-semibold">
            Directive: {activeConsensus.strategic_directive}
          </span>
        </div>
      </div>

      {/* SECTION 2: TOP METRICS GAUGE & CONSENSUS PANEL */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* TENSION INDEX CIRCULAR DIAL (Col: 4) */}
        <div className="lg:col-span-4 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col items-center justify-center text-center space-y-4">
          <div className="flex items-center space-x-2 border-b border-white/5 pb-2 w-full justify-center">
            <Flame className="w-4 h-4 text-orange-500" />
            <h3 className="font-orbitron text-xs font-bold tracking-widest text-slate-300 uppercase">
              Cognitive Tension
            </h3>
          </div>
          
          <div className="relative flex items-center justify-center w-36 h-36">
            {/* SVG Gauges */}
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="72"
                cy="72"
                r="64"
                className="stroke-slate-800"
                strokeWidth="8"
                fill="transparent"
              />
              <circle
                cx="72"
                cy="72"
                r="64"
                className={`transition-all duration-1000 ease-out ${
                  tension > 0.7 ? 'stroke-rose-500' : tension > 0.4 ? 'stroke-amber-500' : 'stroke-emerald-400'
                }`}
                strokeWidth="8"
                strokeDasharray={402}
                strokeDashoffset={402 - (402 * tension)}
                strokeLinecap="round"
                fill="transparent"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center font-mono">
              <span className={`text-4xl font-extrabold tracking-tighter ${tensionColor}`}>
                {Math.round(tension * 100)}%
              </span>
              <span className="text-xxs text-slate-500 uppercase tracking-widest font-semibold mt-0.5">
                Tension Index
              </span>
            </div>
          </div>

          <div className={`w-full p-3 rounded-xl border text-xxs font-mono text-center leading-relaxed ${tensionBorder} ${tensionBg} ${tensionGlow}`}>
            {tension > 0.7 ? (
              <p>⚠️ <strong>CRITICAL TENSION INDEX</strong>: Swarm shows high perspective polarization. Risk projections are divergent. Prompt mutation active to seek stabilization.</p>
            ) : tension > 0.4 ? (
              <p>⚡ <strong>STABLE DIALECTIC TENSION</strong>: Optimal swarm divergence. Houses are robustly debating contradictory options without cognitive stalemate.</p>
            ) : (
              <p>✅ <strong>LOW COGNITIVE TENSION</strong>: Consummate swarm convergence. The prefrontal system is operating in lockstep agreement across all Houses.</p>
            )}
          </div>
        </div>

        {/* FINAL CONSENSUS PLANNING REPORT (Col: 8) */}
        <div className="lg:col-span-8 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col space-y-4 justify-between">
          <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
            <div className="flex items-center space-x-2">
              <Scale className="w-4 h-4 text-cyan-400" />
              <h3 className="font-orbitron text-xs font-bold tracking-widest text-slate-300 uppercase">
                Consensus Strategic Plan
              </h3>
            </div>
            <div className="flex items-center gap-1.5 font-mono text-xxs bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Confidence: {Math.round(activeConsensus.consensus_confidence * 100)}%
            </div>
          </div>

          <div className="bg-black/25 border border-white/5 rounded-xl p-4 font-sans text-xs text-slate-300 leading-relaxed italic">
            &ldquo;{activeConsensus.final_plan}&rdquo;
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            
            {/* Resolved Conflicts Column */}
            <div className="space-y-2">
              <span className="text-xxs font-mono text-slate-400 uppercase tracking-wider block font-semibold">
                🛡️ Resolved Constraints & Conflict Resolutions
              </span>
              <ul className="space-y-1.5 font-mono text-xxs text-slate-300">
                {activeConsensus.resolved_conflicts.map((conflict: string, index: number) => (
                  <li key={index} className="flex items-start gap-1.5">
                    <span className="text-amber-500 font-bold">•</span>
                    <span>{conflict}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Top Perspective Weights Column */}
            <div className="space-y-2">
              <span className="text-xxs font-mono text-slate-400 uppercase tracking-wider block font-semibold">
                🧠 Prefrontal Lens Weights
              </span>
              <div className="space-y-2 font-mono text-xxs">
                {Object.entries(activeConsensus.perspective_weights)
                  .sort((a: any, b: any) => b[1] - a[1])
                  .slice(0, 3)
                  .map(([house, val]: any) => (
                    <div key={house} className="space-y-1">
                      <div className="flex items-center justify-between text-slate-400">
                        <span>{house}</span>
                        <span className="text-cyan-400 font-bold">W = {val.toFixed(2)}</span>
                      </div>
                      <div className="w-full h-1 bg-black/40 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-cyan-400 rounded-full transition-all duration-500" 
                          style={{ width: `${val * 300}%` }} // scaling visualization
                        />
                      </div>
                    </div>
                  ))}
              </div>
            </div>

          </div>
        </div>

      </div>

      {/* SECTION 3: DEBATE ARENA & SCENARIOS / HYPOTHESES */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* PARLIAMENT DEBATE ARENA (Col: 7) */}
        <div className="lg:col-span-7 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col space-y-4">
          <div className="flex items-center space-x-2 border-b border-white/5 pb-3">
            <MessageSquare className="w-4 h-4 text-violet-400" />
            <h3 className="font-orbitron text-xs font-bold tracking-widest text-slate-300 uppercase">
              Parliament Debate Arena
            </h3>
          </div>

          <div className="space-y-4 max-h-[500px] overflow-y-auto pr-1 scrollbar-thin">
            {debates.length === 0 ? (
              <div className="text-center py-20 text-slate-500 font-mono text-xs space-y-2">
                <div>No active debates in this session.</div>
                <div className="opacity-60 text-xxs font-sans">
                  The Swarm Parliament is silent. Spawn a new objective to hear the Houses weigh options!
                </div>
              </div>
            ) : (
              debates.map((turn, idx) => (
                <div key={turn.id || idx} className="space-y-2 p-3 bg-white/[0.01] hover:bg-white/[0.02] border border-white/5 rounded-xl transition duration-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={`text-xxs font-mono px-2 py-0.5 rounded font-semibold ${getHouseStyle(turn.sender)}`}>
                        {turn.sender}
                      </span>
                      <span className="text-xxs font-mono text-slate-500">
                        Round {turn.round}
                      </span>
                    </div>
                    <div className="flex items-center gap-1 text-xxs font-mono text-slate-400">
                      <span>Tension:</span>
                      <span className={turn.tension_score > 0.7 ? 'text-rose-400 font-bold' : turn.tension_score > 0.4 ? 'text-amber-400 font-bold' : 'text-emerald-400'}>
                        {turn.tension_score.toFixed(2)}
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-1.5 font-sans text-xs">
                    <p className="text-slate-200 leading-relaxed bg-black/20 p-2.5 rounded-lg border border-white/5">
                      {turn.argument}
                    </p>
                    {turn.counter_argument && (
                      <div className="flex items-start gap-2 text-xxs font-mono pl-4 text-slate-400 border-l border-white/10 py-1">
                        <ArrowRight className="w-3 h-3 text-cyan-400 flex-shrink-0 mt-0.5" />
                        <p className="italic">{turn.counter_argument}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* SCENARIO COMPARISON & HYPOTHESES DECK (Col: 5) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* FUTURE SCENARIO BRANCHES */}
          <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center space-x-2 border-b border-white/5 pb-2.5">
              <GitFork className="w-4 h-4 text-yellow-500" />
              <h3 className="font-orbitron text-xs font-bold tracking-widest text-slate-300 uppercase">
                Future Scenario Branches
              </h3>
            </div>

            {/* Plan Selector Buttons */}
            <div className="grid grid-cols-3 gap-2">
              {['Plan A', 'Plan B', 'Plan C'].map((p) => (
                <button
                  key={p}
                  onClick={() => setSelectedScenario(p)}
                  className={`py-1.5 font-mono text-xxs border rounded-xl select-none cursor-pointer text-center font-bold transition duration-300 ${
                    selectedScenario === p
                      ? 'border-yellow-500/50 bg-yellow-500/10 text-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.2)]'
                      : 'border-white/10 bg-white/[0.01] text-slate-400 hover:text-slate-200 hover:border-white/20'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>

            {/* Active Plan Metrics */}
            <div className="space-y-3 font-mono text-xxs p-3.5 bg-black/25 rounded-xl border border-white/5">
              <div className="flex items-center justify-between border-b border-white/5 pb-1.5">
                <span className="font-bold text-slate-200 uppercase tracking-wider text-[10px]">
                  {activeScenarioData.branch_name} Branch Outlook
                </span>
                <span className="text-yellow-500 font-bold">
                  {selectedScenario === 'Plan A' ? 'FAST / UNSTABLE' : selectedScenario === 'Plan B' ? 'BALANCED / CONCENTRIC' : 'SLOW / RESILIENT'}
                </span>
              </div>

              {/* Progress bars for metrics */}
              <div className="space-y-2">
                {[
                  { label: 'Success Likelihood', val: activeScenarioData.success_probability, color: 'bg-emerald-500' },
                  { label: 'Stability Index', val: activeScenarioData.stability_index, color: 'bg-cyan-500' },
                  { label: 'Execution Speed', val: activeScenarioData.speed_rating, color: 'bg-amber-500' },
                  { label: 'Resource Cost Rating', val: activeScenarioData.cost_score, color: 'bg-purple-500' },
                  { label: 'Risk Coefficient', val: activeScenarioData.risk_coefficient, color: 'bg-rose-500' }
                ].map((item) => (
                  <div key={item.label} className="space-y-1">
                    <div className="flex items-center justify-between text-slate-400">
                      <span>{item.label}</span>
                      <span className="text-slate-200 font-semibold">{Math.round(item.val * 100)}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-black/40 rounded-full overflow-hidden">
                      <div className={`h-full ${item.color} rounded-full`} style={{ width: `${item.val * 100}%` }} />
                    </div>
                  </div>
                ))}
              </div>

              {/* Topology Path Display */}
              <div className="border-t border-white/5 pt-3.5 space-y-2">
                <span className="text-slate-400 block uppercase tracking-wider text-[10px] font-semibold">
                  🧬 Branch Node Projections
                </span>
                <div className="flex flex-wrap items-center gap-1.5">
                  {activeScenarioData.topology_projection.nodes.map((node: any, nIdx: number) => (
                    <React.Fragment key={node.id}>
                      <span className={`px-2 py-1 rounded border text-[9px] font-semibold ${getHouseStyle(node.id)}`}>
                        {node.id.replace('House', '')}
                      </span>
                      {nIdx < activeScenarioData.topology_projection.nodes.length - 1 && (
                        <ArrowRight className="w-3 h-3 text-slate-600 flex-shrink-0" />
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* SCIENTIFIC HYPOTHESES */}
          <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center space-x-2 border-b border-white/5 pb-2.5">
              <HelpCircle className="w-4 h-4 text-emerald-400" />
              <h3 className="font-orbitron text-xs font-bold tracking-widest text-slate-300 uppercase">
                Scientific Hypotheses
              </h3>
            </div>

            <div className="space-y-3 max-h-[220px] overflow-y-auto pr-1 scrollbar-thin">
              {hypotheses.length === 0 ? (
                <div className="text-center py-8 text-slate-500 font-mono text-[10px]">
                  No hypotheses tracked.
                </div>
              ) : (
                hypotheses.map((hypo) => {
                  let statusBadge = 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30';
                  if (hypo.status === 'TESTING') {
                    statusBadge = 'bg-amber-500/10 text-amber-400 border border-amber-500/30';
                  } else if (hypo.status === 'RETIRED') {
                    statusBadge = 'bg-slate-500/10 text-slate-400 border border-slate-500/30';
                  }

                  return (
                    <div key={hypo.id} className="p-3 bg-white/[0.01] hover:bg-white/[0.02] border border-white/5 rounded-xl transition duration-200 space-y-1.5">
                      <div className="flex items-center justify-between text-xxs font-mono">
                        <span className="font-bold text-slate-200">{hypo.title}</span>
                        <span className={`px-2 py-0.5 rounded font-semibold text-[9px] uppercase tracking-wider ${statusBadge}`}>
                          {hypo.status}
                        </span>
                      </div>
                      
                      <p className="text-xxs text-slate-400 leading-normal font-sans">
                        {hypo.statement}
                      </p>

                      <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 border-t border-white/5 pt-1.5 mt-1">
                        <span>Proving Score: <strong className="text-emerald-400">{Math.round(hypo.proving_score * 100)}%</strong></span>
                        <span>Runs: {hypo.tracking_metrics?.verifications || 0}</span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
