'use client';

import React, { useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  Dna, Cpu, Award, BookOpen, Clock, Activity, Zap, Shield, 
  TrendingUp, RefreshCw, BarChart2, Star, CheckCircle, AlertTriangle 
} from 'lucide-react';

export default function SwarmEvolution() {
  const { 
    genomes, 
    tools, 
    doctrines, 
    reinforcements, 
    houseWeights, 
    bayesianFitness, 
    centrality 
  } = useKingdomStore();

  const [activeSubTab, setActiveSubTab] = useState<'houses' | 'genomes' | 'tools' | 'doctrines'>('houses');

  // Format timestamp helper
  const formatTime = (isoString?: string) => {
    if (!isoString) return 'Just now';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return 'Just now';
    }
  };

  return (
    <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col gap-6 animate-fade-in text-slate-200">
      
      {/* Header telemetry summary bar */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between border-b border-white/10 pb-4 gap-4">
        <div>
          <h2 className="font-orbitron text-xl font-bold tracking-wider text-emerald-400 flex items-center gap-2">
            <Dna className="w-6 h-6 text-emerald-400 animate-pulse" /> Swarm Evolution Dashboard
          </h2>
          <p className="text-xxs text-slate-400 font-mono">Real-time Bayesian fitness learning, genetic prompts, and dynamic tool replacements</p>
        </div>

        {/* Quick status pill counters */}
        <div className="flex flex-wrap gap-2 text-xxs font-mono">
          <div className="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Genomes: {genomes.length}</span>
          </div>
          <div className="bg-cyan-500/10 border border-cyan-500/20 px-3 py-1.5 rounded-full flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
            <span>Tools Evolved: {tools.length}</span>
          </div>
          <div className="bg-fuchsia-500/10 border border-fuchsia-500/20 px-3 py-1.5 rounded-full flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-fuchsia-400"></span>
            <span>Doctrines: {doctrines.length}</span>
          </div>
        </div>
      </div>

      {/* Glassmorphic Navigation Tabs */}
      <div className="flex border-b border-white/5 pb-0.5 gap-2 overflow-x-auto">
        <button
          onClick={() => setActiveSubTab('houses')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'houses' 
              ? 'border-emerald-400 text-emerald-400 bg-emerald-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Shield className="w-4 h-4" /> House Telemetry V2
        </button>

        <button
          onClick={() => setActiveSubTab('genomes')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'genomes' 
              ? 'border-emerald-400 text-emerald-400 bg-emerald-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Dna className="w-4 h-4" /> Swarm Genetics
        </button>

        <button
          onClick={() => setActiveSubTab('tools')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'tools' 
              ? 'border-emerald-400 text-emerald-400 bg-emerald-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Cpu className="w-4 h-4" /> Tool Evolution
        </button>

        <button
          onClick={() => setActiveSubTab('doctrines')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'doctrines' 
              ? 'border-emerald-400 text-emerald-400 bg-emerald-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <BookOpen className="w-4 h-4" /> Wisdom Doctrines
        </button>
      </div>

      {/* Sub-tab Views */}
      <div className="flex-1 min-h-[380px]">
        
        {/* SUBTAB 1: HOUSES TELEMETRY GRID */}
        {activeSubTab === 'houses' && (
          <div className="space-y-6 animate-slide-up">
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
              {['StrategyHouse', 'ResearchHouse', 'EngineeringHouse', 'SecurityHouse', 'MemoryHouse'].map((house) => {
                const weight = houseWeights[house] || 1.0;
                const probability = bayesianFitness[house] || 0.85;
                const centralityScore = centrality[house] || 0.0;

                // Color themes per House
                const themes: Record<string, { text: string, border: string, bg: string, glow: string }> = {
                  StrategyHouse: { text: 'text-amber-400', border: 'border-amber-500/20', bg: 'bg-amber-500/5', glow: 'shadow-[0_0_15px_rgba(245,158,11,0.15)]' },
                  ResearchHouse: { text: 'text-cyan-400', border: 'border-cyan-500/20', bg: 'bg-cyan-500/5', glow: 'shadow-[0_0_15px_rgba(6,182,212,0.15)]' },
                  EngineeringHouse: { text: 'text-sky-400', border: 'border-sky-500/20', bg: 'bg-sky-500/5', glow: 'shadow-[0_0_15px_rgba(14,165,233,0.15)]' },
                  SecurityHouse: { text: 'text-rose-400', border: 'border-rose-500/20', bg: 'bg-rose-500/5', glow: 'shadow-[0_0_15px_rgba(244,63,94,0.15)]' },
                  MemoryHouse: { text: 'text-emerald-400', border: 'border-emerald-500/20', bg: 'bg-emerald-500/5', glow: 'shadow-[0_0_15px_rgba(16,185,129,0.15)]' }
                };

                const currentTheme = themes[house] || themes.StrategyHouse;

                return (
                  <div key={house} className={`backdrop-blur-md border rounded-2xl p-5 flex flex-col justify-between transition-all duration-300 hover:scale-[1.02] ${currentTheme.border} ${currentTheme.bg} ${currentTheme.glow}`}>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="font-orbitron font-bold text-xxs tracking-wider uppercase text-slate-400">
                          {house.replace('House', '')}
                        </span>
                        <Shield className={`w-4 h-4 ${currentTheme.text}`} />
                      </div>
                      
                      <div className="space-y-1">
                        <span className="text-xxs text-slate-500 uppercase font-mono block">Prompt Weight</span>
                        <div className="flex items-baseline gap-2">
                          <span className={`text-xl font-bold font-orbitron ${currentTheme.text}`}>{weight.toFixed(3)}</span>
                          <span className="text-xxs text-emerald-400 font-mono flex items-center gap-0.5">
                            <TrendingUp className="w-3 h-3" /> active
                          </span>
                        </div>
                      </div>

                      {/* Weight progress bar */}
                      <div className="w-full bg-white/5 rounded-full h-1">
                        <div 
                          className="bg-emerald-400 h-1 rounded-full shadow-[0_0_6px_#10b981]" 
                          style={{ width: `${Math.min(100, (weight / 2.5) * 100)}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="mt-6 border-t border-white/5 pt-4 space-y-4">
                      {/* Bayesian Success Probability */}
                      <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                          <span className="text-xxxs text-slate-500 uppercase font-mono block">Bayesian Fitness</span>
                          <span className="font-mono text-[10px] font-bold text-slate-300">P(Success|Evidence)</span>
                        </div>
                        <div className="relative flex items-center justify-center">
                          <span className="font-orbitron font-bold text-xs text-emerald-400">
                            {Math.round(probability * 100)}%
                          </span>
                        </div>
                      </div>

                      {/* Betweenness Centrality */}
                      <div className="flex items-center justify-between">
                        <span className="text-xxxs text-slate-500 uppercase font-mono">Centrality (load)</span>
                        <span className="font-mono text-xxs text-slate-400 font-bold bg-white/5 px-2 py-0.5 rounded">
                          {centralityScore.toFixed(3)}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Reinforcement Mutation Events Logs */}
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-2xl p-5 space-y-4">
              <h3 className="font-orbitron font-bold text-xs tracking-wider text-slate-200 flex items-center gap-1.5">
                <Activity className="w-4 h-4 text-emerald-400" /> Reinforcement Learning logs & Mutations
              </h3>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-xxs border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-slate-400 font-bold">
                      <th className="py-2.5">Time</th>
                      <th className="py-2.5">House</th>
                      <th className="py-2.5">Type</th>
                      <th className="py-2.5">Before Modification</th>
                      <th className="py-2.5">After Modification</th>
                      <th className="py-2.5 text-right">Fitness</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5 text-slate-300">
                    {reinforcements.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="py-8 text-center text-slate-500">
                          Waiting for evolutionary reinforcement events...
                        </td>
                      </tr>
                    ) : (
                      reinforcements.slice(0, 8).map((evt) => (
                        <tr key={evt.id} className="hover:bg-white/[0.02] transition-colors">
                          <td className="py-2.5 text-slate-400">{formatTime(evt.created_at)}</td>
                          <td className="py-2.5 font-bold text-cyan-400">{evt.house}</td>
                          <td className="py-2.5">
                            <span className={`px-2 py-0.5 rounded text-xxxs font-bold font-mono border ${
                              evt.event_type === 'GENETIC_MUTATION' ? 'bg-fuchsia-500/10 border-fuchsia-500/20 text-fuchsia-400' :
                              evt.event_type === 'REWARD' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
                              'bg-rose-500/10 border-rose-500/20 text-rose-400 animate-pulse'
                            }`}>
                              {evt.event_type}
                            </span>
                          </td>
                          <td className="py-2.5 truncate max-w-[150px] text-slate-500" title={evt.before_value || ''}>
                            {evt.before_value || 'None'}
                          </td>
                          <td className="py-2.5 truncate max-w-[200px] text-slate-200" title={evt.after_value || ''}>
                            {evt.after_value || 'None'}
                          </td>
                          <td className="py-2.5 text-right font-bold text-emerald-400">{(evt.fitness_score || 1.0).toFixed(2)}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* SUBTAB 2: SWARM GENETICS */}
        {activeSubTab === 'genomes' && (
          <div className="space-y-6 animate-slide-up">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {genomes.map((g) => (
                <div key={g.id} className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-2xl p-5 flex flex-col justify-between gap-4 shadow-xl">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between border-b border-white/5 pb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/20 text-[10px] font-bold text-emerald-400 font-mono">
                          GENOME
                        </span>
                        <span className="font-mono text-xxs font-bold text-slate-300">{g.id}</span>
                      </div>
                      
                      <div className="flex items-center gap-1">
                        <Star className="w-3.5 h-3.5 fill-emerald-400 text-emerald-400" />
                        <span className="font-orbitron font-bold text-xs text-emerald-400">
                          {g.fitness_score.toFixed(2)}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3 text-xxs font-mono">
                      <div>
                        <span className="text-xxxs text-slate-500 uppercase block">Affiliation</span>
                        <span className="font-semibold text-cyan-400">{g.house}</span>
                      </div>
                      <div>
                        <span className="text-xxxs text-slate-500 uppercase block">Reasoning Method</span>
                        <span className="font-semibold text-fuchsia-400 bg-fuchsia-500/10 px-2 py-0.5 rounded inline-block">
                          {g.reasoning_style}
                        </span>
                      </div>
                    </div>

                    <div className="space-y-1">
                      <span className="text-xxs text-slate-500 uppercase font-mono block">Prompt Blueprint</span>
                      <p className="bg-black/35 border border-white/5 p-3 rounded-xl font-mono text-[10px] text-slate-300 leading-normal max-h-20 overflow-y-auto select-all scrollbar-thin">
                        {g.prompt_template}
                      </p>
                    </div>
                  </div>

                  <div className="border-t border-white/5 pt-3 flex items-center justify-between text-xxs font-mono">
                    <div className="flex items-center gap-3">
                      <div>
                        <span className="text-xxxs text-slate-500 block">Trust Level</span>
                        <span className={`font-bold ${g.trust_metric >= 0.8 ? 'text-emerald-400' : 'text-amber-500'}`}>
                          {Math.round(g.trust_metric * 100)}%
                        </span>
                      </div>
                      {g.parent_id && (
                        <div>
                          <span className="text-xxxs text-slate-500 block">Ancestry parent</span>
                          <span className="text-slate-400 truncate max-w-[80px] block">{g.parent_id}</span>
                        </div>
                      )}
                    </div>
                    
                    <span className="text-xxxs text-slate-500">{formatTime(g.created_at)}</span>
                  </div>
                </div>
              ))}

              {genomes.length === 0 && (
                <div className="col-span-2 backdrop-blur-md bg-white/[0.01] border border-white/5 border-dashed rounded-2xl py-16 flex flex-col items-center justify-center text-slate-500 font-mono text-xs gap-2">
                  <Dna className="w-8 h-8 text-slate-600 animate-pulse" />
                  <span>No genetic prompt genomes synthesized yet. Execute an objective to begin.</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* SUBTAB 3: TOOL EVOLUTION */}
        {activeSubTab === 'tools' && (
          <div className="space-y-6 animate-slide-up">
            <div className="overflow-x-auto bg-black/25 border border-white/5 rounded-2xl">
              <table className="w-full text-left font-mono text-xxs border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-slate-400 font-bold bg-white/[0.02]">
                    <th className="p-4">Tool Name</th>
                    <th className="p-4">Version</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Success Rate</th>
                    <th className="p-4">Avg Latency</th>
                    <th className="p-4">Parent Origin</th>
                    <th className="p-4">Replaced By</th>
                    <th className="p-4 text-right">Evolved</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-slate-300">
                  {tools.map((t) => (
                    <tr key={t.id} className="hover:bg-white/[0.02] transition-colors">
                      <td className="p-4 font-bold text-cyan-400 flex items-center gap-2">
                        <Cpu className="w-3.5 h-3.5" /> {t.name}
                      </td>
                      <td className="p-4 text-slate-300">v{t.version}</td>
                      <td className="p-4">
                        <span className={`px-2 py-0.5 rounded text-xxxs font-bold border ${
                          t.status === 'ACTIVE' 
                            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                            : 'bg-slate-800 border-slate-700 text-slate-500 border-dashed opacity-50'
                        }`}>
                          {t.status}
                        </span>
                      </td>
                      <td className="p-4 font-bold text-emerald-400">{t.success_rate.toFixed(1)}%</td>
                      <td className="p-4 font-bold text-amber-400 flex items-center gap-1">
                        <Clock className="w-3 h-3 text-amber-500/80" /> {t.avg_latency.toFixed(0)} ms
                      </td>
                      <td className="p-4 text-slate-500 truncate max-w-[100px]">{t.parent_tool || 'Baseline'}</td>
                      <td className="p-4 text-rose-400 font-bold truncate max-w-[100px]">{t.replaced_by || '—'}</td>
                      <td className="p-4 text-right text-slate-400">{formatTime(t.created_at)}</td>
                    </tr>
                  ))}

                  {tools.length === 0 && (
                    <tr>
                      <td colSpan={8} className="py-16 text-center text-slate-500">
                        <Cpu className="w-8 h-8 text-slate-600 animate-pulse mx-auto mb-2" />
                        <span>No dynamic evolutionary tool upgrades recorded.</span>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* SUBTAB 4: WISDOM DOCTRINES */}
        {activeSubTab === 'doctrines' && (
          <div className="space-y-6 animate-slide-up">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {doctrines.map((d) => (
                <div key={d.id} className="relative overflow-hidden backdrop-blur-md bg-yellow-500/[0.02] border border-yellow-500/20 rounded-2xl p-6 shadow-xl space-y-4">
                  {/* Subtle royal background glow pattern */}
                  <div className="absolute -top-10 -right-10 w-24 h-24 rounded-full bg-yellow-500/5 blur-2xl"></div>

                  <div className="flex items-center justify-between border-b border-yellow-500/10 pb-3">
                    <div className="flex items-center gap-2">
                      <Award className="w-5 h-5 text-yellow-400 animate-bounce" />
                      <span className="font-orbitron font-bold text-xs tracking-widest uppercase text-yellow-400">
                        Synthesized Kingdom Decree
                      </span>
                    </div>
                    <span className="font-mono text-xxxs text-slate-500">{formatTime(d.created_at)}</span>
                  </div>

                  <div className="space-y-3 font-mono text-xs">
                    <div className="text-yellow-100/90 leading-relaxed bg-black/40 border border-yellow-500/10 p-4 rounded-xl shadow-inner select-all leading-normal whitespace-pre-wrap">
                      {d.doctrine_text}
                    </div>

                    <div className="flex flex-wrap items-center gap-2 text-xxs">
                      <span className="text-slate-500 uppercase tracking-wider text-xxxs">Failure Source Nodes:</span>
                      {d.source_failure_clusters.map((clusterId) => (
                        <span key={clusterId} className="px-2 py-0.5 rounded bg-red-500/10 border border-red-500/20 text-red-400 font-bold">
                          {clusterId.substring(0, 8)}...
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}

              {doctrines.length === 0 && (
                <div className="col-span-2 backdrop-blur-md bg-white/[0.01] border border-white/5 border-dashed rounded-2xl py-16 flex flex-col items-center justify-center text-slate-500 font-mono text-xs gap-2">
                  <BookOpen className="w-8 h-8 text-slate-600 animate-pulse" />
                  <span>No wisdom doctrines synthesized yet. System needs repeat task failures to generate wisdom.</span>
                </div>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
