'use client';

import React, { useState, useEffect } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  Brain, Dna, Swords, Trophy, TrendingUp, ShieldAlert, ShieldCheck, 
  History, PlusCircle, Clock, CheckCircle, Ban, ArrowRight, Activity, Percent
} from 'lucide-react';

export default function MetaLearning() {
  const {
    cognitiveMutations,
    doctrineCompetitions,
    cognitiveGenomes,
    metaLearningRuns,
    metaLearningTrends,
    proposeMutation,
    triggerTournament,
    fetchMetaHistory,
    loading
  } = useKingdomStore();

  const [activeSubTab, setActiveSubTab] = useState<'dna' | 'arena' | 'timeline' | 'propose'>('dna');
  
  // Form states for manual mutation proposal
  const [mutationType, setMutationType] = useState<string>('REASONING_ENGINE');
  const [mutationDesc, setMutationDesc] = useState<string>('');
  const [mutationParams, setMutationParams] = useState<string>('{\n  "recursion_depth": 5,\n  "containment_strictness": 0.85\n}');
  const [proposalError, setProposalError] = useState<string | null>(null);
  const [proposalSuccess, setProposalSuccess] = useState<string | null>(null);

  // Form states for doctrine tournament arena
  const [compA, setCompA] = useState<string>('');
  const [compB, setCompB] = useState<string>('');
  const [arenaError, setArenaError] = useState<string | null>(null);
  const [arenaSuccess, setArenaSuccess] = useState<string | null>(null);

  // Trigger historical fetch once mounted
  useEffect(() => {
    fetchMetaHistory();
  }, [fetchMetaHistory]);

  // Set default tournament selections when genomes list changes
  useEffect(() => {
    if (cognitiveGenomes.length >= 2) {
      if (!compA) setCompA(cognitiveGenomes[0].id);
      if (!compB) setCompB(cognitiveGenomes[1].id);
    }
  }, [cognitiveGenomes, compA, compB]);

  // Handle mutation submission
  const handleProposeMutation = async (e: React.FormEvent) => {
    e.preventDefault();
    setProposalError(null);
    setProposalSuccess(null);

    if (!mutationDesc.trim()) {
      setProposalError('A descriptive explanation is required.');
      return;
    }

    let parsedParams = {};
    try {
      parsedParams = JSON.parse(mutationParams);
    } catch (err) {
      setProposalError('Invalid JSON format for parameters.');
      return;
    }

    try {
      await proposeMutation(mutationType, mutationDesc, parsedParams);
      setProposalSuccess('Mutation proposed successfully! The sovereign stability checker has evaluated it.');
      setMutationDesc('');
      // Refresh meta data
      fetchMetaHistory();
    } catch (err: any) {
      setProposalError(err.message || 'Mutation failed during safety containment audit.');
    }
  };

  // Handle tournament execution
  const handleTriggerTournament = async (e: React.FormEvent) => {
    e.preventDefault();
    setArenaError(null);
    setArenaSuccess(null);

    if (!compA || !compB) {
      setArenaError('Two competing genomes must be selected.');
      return;
    }

    if (compA === compB) {
      setArenaError('Competitor A and Competitor B must be distinct genomes.');
      return;
    }

    try {
      await triggerTournament(compA, compB);
      setArenaSuccess('Philosophical doctrine tournament concluded successfully!');
      // Refresh meta data
      fetchMetaHistory();
    } catch (err: any) {
      setArenaError(err.message || 'Failed executing doctrine tournament.');
    }
  };

  // Format date time helper
  const formatTime = (isoString?: string) => {
    if (!isoString) return 'Just now';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return 'Just now';
    }
  };

  // Get highest-fitness genome
  const activeGenome = cognitiveGenomes.length > 0 
    ? [...cognitiveGenomes].sort((a, b) => b.fitness_score - a.fitness_score)[0]
    : null;

  // Determine trend color matching HSL bounds
  const getTrendColor = (score: number) => {
    if (score >= 0.8) return 'text-teal-400';
    if (score >= 0.6) return 'text-amber-400';
    return 'text-red-400';
  };

  const getTrendGlow = (score: number) => {
    if (score >= 0.8) return 'shadow-[0_0_12px_rgba(20,184,166,0.3)]';
    if (score >= 0.6) return 'shadow-[0_0_12px_rgba(245,158,11,0.3)]';
    return 'shadow-[0_0_12px_rgba(239,68,68,0.3)]';
  };

  return (
    <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col gap-6 animate-fade-in text-slate-200">
      
      {/* 1. Header Bar */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between border-b border-white/10 pb-4 gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center shadow-[0_0_15px_rgba(168,85,247,0.25)]">
            <Brain className="w-6 h-6 text-purple-400 animate-pulse" />
          </div>
          <div>
            <h2 className="font-orbitron text-xl font-bold tracking-wider text-purple-400 flex items-center gap-2">
              Autonomous Meta-Learning Room
            </h2>
            <p className="text-xxs text-slate-400 font-mono">
              Phase 8 Self-Evolving Prompts, Philosophy Tournaments, and Topology Restructuring Guardrails
            </p>
          </div>
        </div>

        {/* Global Stability Indicator */}
        <div className="flex items-center gap-3">
          <div className="flex flex-col text-right font-mono">
            <span className="text-slate-500 text-xxs uppercase">Stability containment status</span>
            <span className={`text-xs font-bold ${metaLearningTrends.mutational_stability >= 0.80 ? 'text-teal-400' : 'text-red-400'}`}>
              {metaLearningTrends.mutational_stability >= 0.80 ? '✓ SECURE (≥0.80)' : '⚠ WARNING (<0.80)'}
            </span>
          </div>
          <div className={`w-3 h-3 rounded-full animate-ping ${metaLearningTrends.mutational_stability >= 0.80 ? 'bg-teal-400' : 'bg-red-400'}`} />
        </div>
      </div>

      {/* 2. Top-Level Evolution Trends Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Trend 1: Mutational Stability */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 p-4 rounded-xl flex items-center justify-between shadow-lg hover:border-white/10 transition duration-300">
          <div className="space-y-1">
            <span className="text-xxxs text-slate-500 uppercase tracking-widest font-mono block">Mutational Stability</span>
            <span className={`text-xl font-orbitron font-extrabold block ${getTrendColor(metaLearningTrends.mutational_stability)}`}>
              {metaLearningTrends.mutational_stability.toFixed(3)}
            </span>
            <span className="text-[10px] text-slate-400 font-mono block">Min Guardrail: 0.800</span>
          </div>
          <div className={`w-12 h-12 rounded-full border-2 flex items-center justify-center font-bold text-xs ${metaLearningTrends.mutational_stability >= 0.80 ? 'border-teal-500/30 text-teal-400' : 'border-red-500/30 text-red-400'}`}>
            {metaLearningTrends.mutational_stability >= 0.80 ? <ShieldCheck className="w-6 h-6" /> : <ShieldAlert className="w-6 h-6" />}
          </div>
        </div>

        {/* Trend 2: Learning Accuracy */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 p-4 rounded-xl flex items-center justify-between shadow-lg hover:border-white/10 transition duration-300">
          <div className="space-y-1">
            <span className="text-xxxs text-slate-500 uppercase tracking-widest font-mono block">Learning Accuracy</span>
            <span className="text-xl font-orbitron font-extrabold text-cyan-400 block">
              {(metaLearningTrends.learning_accuracy * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-slate-400 font-mono block">Accuracy Gain Index</span>
          </div>
          <div className="w-12 h-12 rounded-full border-2 border-cyan-500/30 flex items-center justify-center font-bold text-xs text-cyan-400">
            <TrendingUp className="w-5 h-5 animate-pulse" />
          </div>
        </div>

        {/* Trend 3: Failure Reduction */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 p-4 rounded-xl flex items-center justify-between shadow-lg hover:border-white/10 transition duration-300">
          <div className="space-y-1">
            <span className="text-xxxs text-slate-500 uppercase tracking-widest font-mono block">Failure Reduction</span>
            <span className="text-xl font-orbitron font-extrabold text-emerald-400 block">
              {(metaLearningTrends.failure_reduction * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-slate-400 font-mono block">Cascade Isolation Rate</span>
          </div>
          <div className="w-12 h-12 rounded-full border-2 border-emerald-500/30 flex items-center justify-center font-bold text-xs text-emerald-400">
            <Percent className="w-5 h-5" />
          </div>
        </div>

        {/* Trend 4: Wisdom Compression */}
        <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 p-4 rounded-xl flex items-center justify-between shadow-lg hover:border-white/10 transition duration-300">
          <div className="space-y-1">
            <span className="text-xxxs text-slate-500 uppercase tracking-widest font-mono block">Wisdom Compression</span>
            <span className="text-xl font-orbitron font-extrabold text-purple-400 block">
              {metaLearningTrends.wisdom_compression.toFixed(2)}x
            </span>
            <span className="text-[10px] text-slate-400 font-mono block">Doctrine Prune Ratio</span>
          </div>
          <div className="w-12 h-12 rounded-full border-2 border-purple-500/30 flex items-center justify-center font-bold text-xs text-purple-400">
            <History className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* 3. Navigation Sub-Tabs */}
      <div className="flex border-b border-white/5 pb-0.5 gap-2 overflow-x-auto">
        <button
          onClick={() => setActiveSubTab('dna')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'dna' 
              ? 'border-purple-400 text-purple-400 bg-purple-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Dna className="w-4 h-4" /> Cognitive DNA Configs
        </button>

        <button
          onClick={() => setActiveSubTab('arena')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'arena' 
              ? 'border-purple-400 text-purple-400 bg-purple-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Swords className="w-4 h-4" /> Doctrine Tournament Arena
        </button>

        <button
          onClick={() => setActiveSubTab('timeline')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'timeline' 
              ? 'border-purple-400 text-purple-400 bg-purple-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <History className="w-4 h-4" /> Evolutionary Mutation Timeline
        </button>

        <button
          onClick={() => setActiveSubTab('propose')}
          className={`px-4 py-2 border-b-2 font-mono text-xs font-semibold tracking-wider transition-all duration-300 flex items-center gap-2 whitespace-nowrap ${
            activeSubTab === 'propose' 
              ? 'border-purple-400 text-purple-400 bg-purple-500/[0.04]' 
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <PlusCircle className="w-4 h-4" /> Propose Swarm Restructuring
        </button>
      </div>

      {/* 4. Sub-tab Views Content */}
      <div className="flex-1 min-h-[350px]">
        
        {/* SUBTAB 1: COGNITIVE DNA CONFIGS */}
        {activeSubTab === 'dna' && (
          <div className="space-y-6 animate-slide-up">
            
            {/* Active Highest Fitness DNA Display Card */}
            {activeGenome ? (
              <div className="relative overflow-hidden backdrop-blur-md bg-purple-500/[0.03] border border-purple-500/20 rounded-2xl p-6 shadow-xl space-y-4">
                <div className="absolute -top-10 -right-10 w-32 h-32 rounded-full bg-purple-500/5 blur-3xl" />
                
                <div className="flex items-center justify-between border-b border-purple-500/10 pb-3">
                  <div className="flex items-center gap-2.5">
                    <span className="px-3 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 text-[10px] font-bold text-purple-400 font-mono shadow-[0_0_8px_rgba(168,85,247,0.2)] animate-pulse">
                      🧬 ACTIVE CHAMPION GENOME
                    </span>
                    <span className="font-mono text-xs font-bold text-slate-300">{activeGenome.id}</span>
                  </div>
                  <div className="flex items-center gap-1.5 font-orbitron font-extrabold text-sm text-purple-400">
                    <Trophy className="w-4 h-4 fill-purple-400" />
                    <span>FITNESS: {activeGenome.fitness_score.toFixed(3)}</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
                  {/* Styling columns for core stats */}
                  <div className="space-y-4">
                    <div>
                      <span className="text-xxs text-slate-500 uppercase block mb-1">Reasoning Style Blueprint</span>
                      <span className="font-bold text-purple-300 bg-purple-500/10 px-2.5 py-1 border border-purple-500/20 rounded inline-block uppercase text-xxs">
                        {activeGenome.reasoning_style}
                      </span>
                    </div>
                    <div>
                      <span className="text-xxs text-slate-500 uppercase block mb-1">Debate Format Law</span>
                      <span className="font-bold text-cyan-300 bg-cyan-500/10 px-2.5 py-1 border border-cyan-500/20 rounded inline-block uppercase text-xxs">
                        {activeGenome.debate_format}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <span className="text-xxs text-slate-500 uppercase block mb-1">Memory Association Coefficient</span>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-black/40 h-2 rounded-full overflow-hidden border border-white/5">
                          <div 
                            style={{ width: `${Math.min(100, activeGenome.memory_coefficient * 100)}%` }} 
                            className="bg-purple-500 h-full rounded-full shadow-[0_0_6px_#a855f7]"
                          />
                        </div>
                        <span className="font-bold text-slate-300 w-8">{activeGenome.memory_coefficient.toFixed(2)}</span>
                      </div>
                    </div>

                    <div>
                      <span className="text-xxs text-slate-500 uppercase block mb-1">Trust Propagation Mesh Weight</span>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-black/40 h-2 rounded-full overflow-hidden border border-white/5">
                          <div 
                            style={{ width: `${Math.min(100, activeGenome.trust_propagation_weight * 100)}%` }} 
                            className="bg-teal-500 h-full rounded-full shadow-[0_0_6px_#14b8a6]"
                          />
                        </div>
                        <span className="font-bold text-slate-300 w-8">{activeGenome.trust_propagation_weight.toFixed(2)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2 bg-black/35 border border-white/5 p-3 rounded-xl">
                    <span className="text-xxs text-slate-400 font-bold block uppercase border-b border-white/5 pb-1">
                      🧬 Cognitive Emotional Weights
                    </span>
                    <div className="space-y-1.5 text-xxs">
                      {Object.entries(activeGenome.emotional_weighting || {}).map(([emotion, val]) => (
                        <div key={emotion} className="flex justify-between items-center text-slate-300">
                          <span className="capitalize">{emotion}</span>
                          <span className="font-bold text-purple-400">{val.toFixed(2)}</span>
                        </div>
                      ))}
                      {(!activeGenome.emotional_weighting || Object.keys(activeGenome.emotional_weighting).length === 0) && (
                        <span className="text-slate-500 italic">No emotional adjustments</span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="border-t border-purple-500/10 pt-3 flex items-center justify-between text-xxs font-mono text-slate-500">
                  <span>Strategy Bias: <span className="text-slate-300 font-semibold">{activeGenome.strategy_preference}</span></span>
                  <span>Synthesized Generation: <span className="text-purple-400 font-bold">G-{activeGenome.generation}</span></span>
                </div>
              </div>
            ) : (
              <div className="backdrop-blur-md bg-white/[0.01] border border-white/5 border-dashed rounded-2xl py-12 flex flex-col items-center justify-center text-slate-500 font-mono text-xs gap-2">
                <Dna className="w-8 h-8 text-slate-600 animate-pulse" />
                <span>No evolutionary genomes indexed in database. Run a workspace objective to automatically evolve DNA.</span>
              </div>
            )}

            {/* Genomes List Grid */}
            <div className="space-y-3">
              <h3 className="font-orbitron font-bold text-xs tracking-wider text-slate-300 flex items-center gap-1.5">
                <Activity className="w-4 h-4 text-purple-400" /> Synthesized Swarm Prompts Pool
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {cognitiveGenomes.filter(g => activeGenome ? g.id !== activeGenome.id : true).map((g) => (
                  <div key={g.id} className="backdrop-blur-md bg-white/[0.01] border border-white/5 p-4 rounded-xl flex flex-col justify-between gap-3 hover:border-white/10 transition duration-200 text-xxs font-mono">
                    <div className="flex justify-between items-center border-b border-white/5 pb-1.5">
                      <span className="font-bold text-slate-300 truncate max-w-[150px]">{g.id}</span>
                      <span className="font-bold text-emerald-400 flex items-center gap-1">
                        <TrendingUp className="w-3 h-3" /> Fitness: {g.fitness_score.toFixed(3)}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-slate-400">
                      <div>Style: <span className="text-slate-200 font-bold">{g.reasoning_style}</span></div>
                      <div>Format: <span className="text-slate-200 font-bold">{g.debate_format}</span></div>
                      <div>Gen: <span className="text-slate-200 font-bold">G-{g.generation}</span></div>
                      <div>Preference: <span className="text-slate-200 font-bold">{g.strategy_preference}</span></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* SUBTAB 2: DOCTRINE TOURNAMENT ARENA */}
        {activeSubTab === 'arena' && (
          <div className="space-y-6 animate-slide-up">
            
            {/* Arena Trigger Form */}
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-2xl p-5 space-y-4">
              <h3 className="font-orbitron font-bold text-xs tracking-wider text-slate-200 flex items-center gap-2">
                <Swords className="w-4 h-4 text-purple-400" /> Philosophical Doctrine Arena
              </h3>
              <p className="text-xxs text-slate-400 font-mono">
                Force competing doctrine neural templates into simulation stress testing. The winner is selected to lead the parliament.
              </p>

              <form onSubmit={handleTriggerTournament} className="space-y-4 font-mono text-xs">
                {arenaError && (
                  <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-xxs">
                    {arenaError}
                  </div>
                )}
                {arenaSuccess && (
                  <div className="p-3 bg-teal-500/10 border border-teal-500/20 text-teal-400 rounded-lg text-xxs">
                    {arenaSuccess}
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Competitor A */}
                  <div className="space-y-1.5">
                    <label className="text-xxs text-slate-400 uppercase font-bold">Competitor Genome Alpha</label>
                    <select
                      value={compA}
                      onChange={(e) => setCompA(e.target.value)}
                      className="w-full bg-black/40 border border-white/10 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-purple-500"
                    >
                      <option value="">Select genome...</option>
                      {cognitiveGenomes.map(g => (
                        <option key={g.id} value={g.id}>
                          {g.id.substring(0, 15)}... (Fitness: {g.fitness_score.toFixed(2)}) [{g.reasoning_style}]
                        </option>
                      ))}
                      {cognitiveGenomes.length === 0 && (
                        <option value="GENOME_MOCK_A">Synthesized Mock Genome Alpha [DEDUCTIVE]</option>
                      )}
                    </select>
                  </div>

                  {/* Competitor B */}
                  <div className="space-y-1.5">
                    <label className="text-xxs text-slate-400 uppercase font-bold">Competitor Genome Beta</label>
                    <select
                      value={compB}
                      onChange={(e) => setCompB(e.target.value)}
                      className="w-full bg-black/40 border border-white/10 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-purple-500"
                    >
                      <option value="">Select genome...</option>
                      {cognitiveGenomes.map(g => (
                        <option key={g.id} value={g.id}>
                          {g.id.substring(0, 15)}... (Fitness: {g.fitness_score.toFixed(2)}) [{g.reasoning_style}]
                        </option>
                      ))}
                      {cognitiveGenomes.length === 0 && (
                        <option value="GENOME_MOCK_B">Synthesized Mock Genome Beta [DIALECTIC]</option>
                      )}
                    </select>
                  </div>
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    type="submit"
                    disabled={loading}
                    className="backdrop-blur-md bg-purple-500/20 border border-purple-500/30 hover:bg-purple-500/30 hover:border-purple-500/50 text-purple-300 font-bold px-5 py-2.5 rounded-xl transition duration-300 flex items-center gap-2 cursor-pointer disabled:opacity-50"
                  >
                    <Swords className="w-4 h-4 animate-spin-slow" />
                    {loading ? 'Simulating Tournament...' : '⚔️ Trigger Philosophy Tournament'}
                  </button>
                </div>
              </form>
            </div>

            {/* Historical competitions log */}
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-2xl p-5 space-y-3">
              <h3 className="font-orbitron font-bold text-xs tracking-wider text-slate-300 flex items-center gap-1.5">
                <Trophy className="w-4 h-4 text-purple-400" /> Tournament Outcomes & Synthesized Victories
              </h3>

              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-xxs border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-slate-400 font-bold">
                      <th className="py-2.5">Tournament Timestamp</th>
                      <th className="py-2.5">Competitor A (Metric)</th>
                      <th className="py-2.5 text-center">VS</th>
                      <th className="py-2.5">Competitor B (Metric)</th>
                      <th className="py-2.5">Consensus Winner</th>
                      <th className="py-2.5 text-right">Contradiction Gap</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5 text-slate-300">
                    {doctrineCompetitions.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="py-8 text-center text-slate-500">
                          No tournaments simulated in current epoch. Use the tool above to run an evolution tournament!
                        </td>
                      </tr>
                    ) : (
                      doctrineCompetitions.map((comp) => {
                        const gap = Math.abs(comp.metric_a - comp.metric_b);
                        const isWinA = comp.winner_id === comp.competitor_a_id;
                        return (
                          <tr key={comp.id} className="hover:bg-white/[0.01] transition-colors">
                            <td className="py-2.5 text-slate-400">{formatTime(comp.created_at)}</td>
                            <td className={`py-2.5 ${isWinA ? 'font-bold text-emerald-400' : 'text-slate-400'}`}>
                              {comp.competitor_a_id.substring(0, 12)}... ({comp.metric_a.toFixed(2)})
                            </td>
                            <td className="py-2.5 text-center text-slate-500">VS</td>
                            <td className={`py-2.5 ${!isWinA ? 'font-bold text-emerald-400' : 'text-slate-400'}`}>
                              {comp.competitor_b_id.substring(0, 12)}... ({comp.metric_b.toFixed(2)})
                            </td>
                            <td className="py-2.5 text-purple-300 font-bold flex items-center gap-1">
                              <Trophy className="w-3 h-3 text-purple-400 fill-purple-400/20" /> {comp.winner_id.substring(0, 12)}...
                            </td>
                            <td className="py-2.5 text-right text-slate-400 font-bold">{gap.toFixed(3)}</td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* SUBTAB 3: EVOLUTIONARY MUTATION TIMELINE */}
        {activeSubTab === 'timeline' && (
          <div className="space-y-6 animate-slide-up">
            
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-2xl p-5 space-y-4">
              <h3 className="font-orbitron font-bold text-xs tracking-wider text-slate-200 flex items-center gap-1.5">
                <History className="w-4 h-4 text-purple-400" /> Scrolling Topology Restructuring Log
              </h3>
              <p className="text-xxs text-slate-400 font-mono">
                Persisted history of structural cognitive mutations. Mutations scoring below 0.80 stability checks are immediately tagged <span className="text-red-400 font-bold">BLOCKED</span> to enforce containment safety laws.
              </p>

              <div className="relative border-l border-white/10 pl-6 ml-3 space-y-6 py-2">
                {cognitiveMutations.length === 0 ? (
                  <div className="text-slate-500 font-mono text-xxs py-4 pl-2">
                    No structural mutations recorded in the database yet.
                  </div>
                ) : (
                  cognitiveMutations.map((mut) => {
                    const isBlocked = mut.status === 'BLOCKED';
                    const isCommitted = mut.status === 'COMMITTED';
                    const isProposed = mut.status === 'PROPOSED';
                    
                    let badgeClass = 'bg-slate-500/10 border-slate-500/20 text-slate-400';
                    let dotClass = 'bg-slate-400';
                    
                    if (isBlocked) {
                      badgeClass = 'bg-red-500/10 border-red-500/25 text-red-400';
                      dotClass = 'bg-red-500 shadow-[0_0_8px_#ef4444] animate-pulse';
                    } else if (isCommitted) {
                      badgeClass = 'bg-teal-500/10 border-teal-500/25 text-teal-400';
                      dotClass = 'bg-teal-400 shadow-[0_0_8px_#14b8a6]';
                    } else if (isProposed) {
                      badgeClass = 'bg-amber-500/10 border-amber-500/25 text-amber-400';
                      dotClass = 'bg-amber-400 shadow-[0_0_8px_#f59e0b]';
                    }

                    return (
                      <div key={mut.id} className="relative group">
                        {/* Timeline Node Bullet */}
                        <div className={`absolute -left-[31px] top-1.5 w-2.5 h-2.5 rounded-full ${dotClass} transition-all duration-300`} />
                        
                        <div className="backdrop-blur-md bg-white/[0.01] border border-white/5 hover:border-white/10 p-4 rounded-xl flex flex-col gap-2 transition duration-200">
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-white/5 pb-1.5 gap-2 text-xxs">
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-slate-200">{mut.mutation_type}</span>
                              <span className="text-slate-500">[{mut.id}]</span>
                            </div>
                            
                            <div className="flex items-center gap-2.5">
                              <span className={`px-2 py-0.5 border rounded-full text-[9px] font-bold ${badgeClass}`}>
                                {mut.status}
                              </span>
                              <span className="text-slate-500">{formatTime(mut.created_at)}</span>
                            </div>
                          </div>

                          <p className="text-xxs text-slate-300 font-mono leading-normal leading-relaxed">
                            {mut.description}
                          </p>

                          <div className="flex flex-wrap items-center justify-between text-xxs font-mono pt-1 text-slate-500 border-t border-white/5">
                            <div className="flex items-center gap-2.5">
                              <span>Stability check score:</span>
                              <span className={`font-bold ${mut.stability_score >= 0.80 ? 'text-teal-400' : 'text-red-400'}`}>
                                {mut.stability_score.toFixed(3)}
                              </span>
                              {isBlocked && (
                                <span className="text-red-400 font-semibold flex items-center gap-0.5">
                                  <Ban className="w-3 h-3" /> Blocked under absolute safety containment law (≥ 0.80)
                                </span>
                              )}
                            </div>
                            
                            {mut.applied_at && (
                              <span>Applied: <span className="text-slate-400">{formatTime(mut.applied_at)}</span></span>
                            )}
                          </div>

                          {/* Parameter details drop-down block */}
                          {mut.parameters && Object.keys(mut.parameters).length > 0 && (
                            <div className="mt-2 bg-black/20 p-2 rounded border border-white/5 text-[10px] text-slate-400 leading-normal max-h-16 overflow-y-auto">
                              <span className="font-bold text-slate-500 text-[8px] uppercase block mb-1">Restructure Parameters</span>
                              <pre className="font-mono text-xxxs text-slate-400">{JSON.stringify(mut.parameters, null, 2)}</pre>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>
        )}

        {/* SUBTAB 4: PROPOSE DYNAMIC SWARM MUTATION */}
        {activeSubTab === 'propose' && (
          <div className="space-y-6 animate-slide-up">
            
            <div className="backdrop-blur-md bg-white/[0.02] border border-white/5 rounded-2xl p-5 space-y-4">
              <div className="flex items-center gap-2">
                <PlusCircle className="w-5 h-5 text-purple-400" />
                <h3 className="font-orbitron font-bold text-xs tracking-wider text-slate-200">
                  Propose Evolutionary System Restructuring
                </h3>
              </div>
              <p className="text-xxs text-slate-400 font-mono">
                Initiate a manual system mutation request. All proposed changes run through Knight-0's containment checkers. If the stability containment coefficient is below <span className="text-red-400 font-bold">0.800</span>, the change is rejected instantly.
              </p>

              <form onSubmit={handleProposeMutation} className="space-y-4 font-mono text-xs">
                {proposalError && (
                  <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-xxs">
                    ⚠ Containment Safety Error: {proposalError}
                  </div>
                )}
                {proposalSuccess && (
                  <div className="p-3 bg-teal-500/10 border border-teal-500/20 text-teal-400 rounded-lg text-xxs">
                    ✓ Success: {proposalSuccess}
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Mutation Type */}
                  <div className="space-y-1.5">
                    <label className="text-xxs text-slate-400 uppercase font-bold">Evolution Area</label>
                    <select
                      value={mutationType}
                      onChange={(e) => setMutationType(e.target.value)}
                      className="w-full bg-black/40 border border-white/10 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-purple-500"
                    >
                      <option value="REASONING_ENGINE">REASONING_ENGINE (Adjust deep context formatting)</option>
                      <option value="DELEGATION_POLICY">DELEGATION_POLICY (Swarm House execution weights)</option>
                      <option value="MEMORY_RETRIEVAL">MEMORY_RETRIEVAL (Vector cache retrieval indexes)</option>
                      <option value="STABILITY_THRESHOLD">STABILITY_THRESHOLD (Consensus validation rules)</option>
                    </select>
                  </div>

                  {/* Description */}
                  <div className="md:col-span-2 space-y-1.5">
                    <label className="text-xxs text-slate-400 uppercase font-bold">Change Law & Intent Summary</label>
                    <input
                      type="text"
                      placeholder="e.g., Amplify inductive logic chains to isolate ResearchHouse execution failures..."
                      value={mutationDesc}
                      onChange={(e) => setMutationDesc(e.target.value)}
                      className="w-full bg-black/40 border border-white/10 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-purple-500"
                    />
                  </div>
                </div>

                {/* Parameters JSON */}
                <div className="space-y-1.5">
                  <label className="text-xxs text-slate-400 uppercase font-bold">DNA Configuration Parameters (JSON Format)</label>
                  <textarea
                    rows={4}
                    value={mutationParams}
                    onChange={(e) => setMutationParams(e.target.value)}
                    className="w-full bg-black/40 border border-white/10 rounded-lg p-3 text-slate-200 focus:outline-none focus:border-purple-500 font-mono text-xxs"
                  />
                </div>

                <div className="flex justify-between items-center pt-2">
                  <div className="flex items-center gap-1.5 text-xxs text-slate-500">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>Real-time safety simulation will be run before committing.</span>
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="backdrop-blur-md bg-purple-500/20 border border-purple-500/30 hover:bg-purple-500/30 hover:border-purple-500/50 text-purple-300 font-bold px-5 py-2.5 rounded-xl transition duration-300 flex items-center gap-2 cursor-pointer disabled:opacity-50"
                  >
                    <Brain className="w-4 h-4" />
                    {loading ? 'Simulating mutation safety...' : 'Propose Restructuring'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
