'use client';

import React, { useEffect, useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import ThroneRoom from '../components/ThroneRoom';
import GraphEngine from '../components/GraphEngine';
import SwarmEvolution from '../components/SwarmEvolution';
import SoldierMonitor from '../components/SoldierMonitor';
import MemoryCrypt from '../components/MemoryCrypt';
import Constitution from '../components/Constitution';
import Observability from '../components/Observability';
import CivilizationParliament from '../components/CivilizationParliament';
import ThoughtEvolution from '../components/ThoughtEvolution';
import TrustAlignment from '../components/TrustAlignment';
import PlanetaryMesh from '../components/PlanetaryMesh';
import MetaLearning from '../components/MetaLearning';
import ScientificEvolution from '../components/ScientificEvolution';
import ScientificThroneRoom from '../components/ScientificThroneRoom';
import SovereignStrategicThroneRoom from '../components/SovereignStrategicThroneRoom';
import ExecutionResultPanel from '../components/ExecutionResultPanel';
import SystemHealthCenter from '../components/SystemHealthCenter';
import ExpertiseEvolutionCenter from '../components/ExpertiseEvolutionCenter';
import ExecutiveCommandCenter from '../components/ExecutiveCommandCenter';
import ExecutiveThroneRoomV2 from '../components/ExecutiveThroneRoomV2';
import LineageVisualizer from '../components/LineageVisualizer';
import { ShieldCheck, Cpu, HardDrive, Settings, Activity, Sparkles } from 'lucide-react';

export default function Dashboard() {
  const { 
    fetchAllData, 
    startPolling, 
    stopPolling, 
    connectWebSocket, 
    disconnectWebSocket, 
    topology, 
    tasks, 
    memories, 
    error, 
    clearError 
  } = useKingdomStore();
  const [activeTab, setActiveTab] = useState<'sovereign' | 'scientific' | 'executive_v2' | 'executive' | 'throne' | 'planetary_mesh' | 'parliament' | 'thought_evolution' | 'graph' | 'evolution' | 'soldiers' | 'crypt' | 'governance' | 'logs' | 'trust_alignment' | 'meta_learning' | 'scientific_evolution' | 'execution' | 'health' | 'expertise'>('sovereign');

  // Trigger initial full fetch and background 2s poll sync loops + WebSocket streams
  useEffect(() => {
    fetchAllData();
    startPolling();
    connectWebSocket();
    return () => {
      stopPolling();
      disconnectWebSocket();
    };
  }, [fetchAllData, startPolling, stopPolling, connectWebSocket, disconnectWebSocket]);

  // Calculate aggregated metrics
  const activeSoldiers = topology.nodes.filter(n => n.type === 'SOLDIER').length;
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.status === 'COMPLETED').length;
  const compPct = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Calculate average compression ratio savings
  const compressedMemories = memories.filter(m => m.compressed_content);
  const avgSavings = compressedMemories.length > 0
    ? Math.round(
        compressedMemories.reduce((acc, m) => {
          const original = m.compression_ratio?.original || m.raw_content.length;
          const compressed = m.compression_ratio?.compressed || m.compressed_content?.length || original;
          const savings = original > 0 ? Math.max(0, 1 - (compressed / original)) : 0;
          return acc + savings;
        }, 0) / compressedMemories.length * 100
      )
    : 0;

  const tabItems = [
    { id: 'sovereign', label: '👑 Sovereign Autonomy', desc: 'Long-Horizon Civilization Intel' },
    { id: 'scientific', label: '🔬 Scientific Throne', desc: 'Deep Reasoning & Causal Cognition' },
    { id: 'executive_v2', label: '👑 Knight-0 Ascension', desc: 'Real cognition & autonomy' },
    { id: 'executive', label: '👑 Executive Command', desc: 'Synthesized intel & lineage' },
    { id: 'throne', label: '⚔️ Throne Room', desc: 'Supreme directives' },
    { id: 'planetary_mesh', label: '🌐 Planetary Mesh', desc: 'Distributed mesh & RAFT' },
    { id: 'parliament', label: '🏛️ Parliament', desc: 'Debate & Scenario trees' },
    { id: 'thought_evolution', label: '🧠 Thought Evolution', desc: 'Meta-cognition & ATG' },
    { id: 'meta_learning', label: '🧠 Meta-Learning', desc: 'DNA & Self-Evolution' },
    { id: 'scientific_evolution', label: '🔬 Scientific Evolution', desc: 'Causal & branch forecast' },
    { id: 'execution', label: '⚡ Execution Results', desc: 'Live execution panel' },
    { id: 'graph', label: '🕸️ Graph Engine', desc: 'Civilization topology' },
    { id: 'evolution', label: '🧬 Swarm Evolution', desc: 'Genetics & tool ancestry' },
    { id: 'soldiers', label: '🛡️ Soldiers Monitor', desc: 'Swarm health monitor' },
    { id: 'crypt', label: '🪦 Memory Crypt', desc: 'Compressed wisdom' },
    { id: 'governance', label: '⚖️ Constitution', desc: 'Governance chamber' },
    { id: 'trust_alignment', label: '🛡️ Trust & Alignment', desc: 'Safeguards & emotions' },
    { id: 'health', label: '🏥 System Health', desc: 'Execution reality verification' },
    { id: 'expertise', label: '📈 Expertise Evolution', desc: 'Real capability benchmarking' },
    { id: 'logs', label: '📺 Observability Logs', desc: 'Live event stream' },
  ];

  return (
    <main className="min-h-screen bg-[#030307] text-slate-100 font-sans pb-12 selection:bg-cyan-500/20">
      
      {/* 1. Glassmorphic Navigation Header bar */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-[#030307]/70 border-b border-white/5 py-4 px-6 md:px-12 flex items-center justify-between">
        <div className="flex items-center space-x-3.5">
          <div className="w-9 h-9 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center shadow-[0_0_12px_rgba(6,182,212,0.2)]">
            <Sparkles className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h1 className="font-orbitron font-extrabold text-md tracking-widest text-slate-100 uppercase">
              ANTIGRAVITY
            </h1>
            <span className="text-xxs font-mono text-cyan-500/60 uppercase tracking-widest block -mt-1 font-bold">
              Cognitive Civilization Control Center
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {error && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1 bg-red-500/10 border border-red-500/20 rounded-lg text-xxs font-mono text-red-400">
              <span>Error: {error.length > 50 ? `${error.slice(0, 50)}...` : error}</span>
              <button onClick={clearError} className="hover:text-white ml-2">✕</button>
            </div>
          )}
          <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full text-xxs font-mono text-emerald-400">
            <ShieldCheck className="w-3.5 h-3.5" /> SYSTEM COMPLIANT
          </div>
        </div>
      </header>

      {/* 2. Content Container */}
      <div className="max-w-7xl mx-auto px-6 md:px-12 mt-8 space-y-8">
        
        {/* Real-time stats summary cards */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 font-mono">
          <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-5 shadow-lg flex items-center gap-4 hover:border-white/20 transition duration-300">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
              <Cpu className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <span className="text-slate-500 text-xxs uppercase tracking-wider block">Active Soldiers</span>
              <span className="text-xl font-bold text-slate-100">{activeSoldiers} Online</span>
            </div>
          </div>

          <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-5 shadow-lg flex items-center gap-4 hover:border-white/20 transition duration-300">
            <div className="w-10 h-10 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center">
              <Activity className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <span className="text-slate-500 text-xxs uppercase tracking-wider block">DAG Completion</span>
              <span className="text-xl font-bold text-slate-100">{compPct}% ({completedTasks}/{totalTasks})</span>
            </div>
          </div>

          <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-5 shadow-lg flex items-center gap-4 hover:border-white/20 transition duration-300">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <span className="text-slate-500 text-xxs uppercase tracking-wider block">Wisdom Compression</span>
              <span className="text-xl font-bold text-slate-100">-{avgSavings}% Savings</span>
            </div>
          </div>

          <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-5 shadow-lg flex items-center gap-4 hover:border-white/20 transition duration-300">
            <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center">
              <Settings className="w-5 h-5 text-rose-500" />
            </div>
            <div>
              <span className="text-slate-500 text-xxs uppercase tracking-wider block">Constitutional Status</span>
              <span className="text-xl font-bold text-slate-100">100% Enforced</span>
            </div>
          </div>
        </section>

        {/* 3. Navigation Tabs Controller */}
        <section className="border-b border-white/5 pb-2">
          <div className="flex flex-wrap md:flex-nowrap gap-2 overflow-x-auto pb-2 scrollbar-thin">
            {tabItems.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex-1 min-w-[150px] p-3 border rounded-2xl text-left select-none cursor-pointer transition duration-300 ${
                  activeTab === tab.id
                    ? 'border-cyan-500 bg-cyan-500/5 text-cyan-400 shadow-[0_0_12px_rgba(6,182,212,0.1)]'
                    : 'border-white/10 bg-white/[0.01] text-slate-400 hover:border-white/20 hover:text-slate-200'
                }`}
              >
                <div className="font-orbitron font-bold text-xs tracking-wider">{tab.label}</div>
                <div className="text-xxs opacity-60 font-mono mt-0.5 truncate">{tab.desc}</div>
              </button>
            ))}
          </div>
        </section>

        {/* 4. Active Tab Component Portal */}
        <section className="transition-all duration-300">
          {activeTab === 'sovereign' && (
            <div className="space-y-8">
              <SovereignStrategicThroneRoom />
            </div>
          )}
          {activeTab === 'scientific' && (
            <div className="space-y-8">
              <ScientificThroneRoom />
            </div>
          )}
          {activeTab === 'executive_v2' && (
            <div className="space-y-8">
              <ExecutiveThroneRoomV2 />
            </div>
          )}
          {activeTab === 'executive' && (
            <div className="space-y-8">
              <ExecutiveCommandCenter />
              <LineageVisualizer />
            </div>
          )}
          {activeTab === 'throne' && <ThroneRoom />}
          {activeTab === 'planetary_mesh' && <PlanetaryMesh />}
          {activeTab === 'parliament' && <CivilizationParliament />}
          {activeTab === 'thought_evolution' && <ThoughtEvolution />}
          {activeTab === 'meta_learning' && <MetaLearning />}
          {activeTab === 'scientific_evolution' && <ScientificEvolution />}
          {activeTab === 'execution' && <ExecutionResultPanel />}
          {activeTab === 'graph' && <GraphEngine />}
          {activeTab === 'evolution' && <SwarmEvolution />}
          {activeTab === 'soldiers' && <SoldierMonitor />}
          {activeTab === 'crypt' && <MemoryCrypt />}
          { activeTab === 'governance' && <Constitution /> }
          { activeTab === 'trust_alignment' && <TrustAlignment /> }
          { activeTab === 'health' && <SystemHealthCenter /> }
          { activeTab === 'expertise' && <ExpertiseEvolutionCenter /> }
          { activeTab === 'logs' && <Observability /> }
        </section>

      </div>
    </main>
  );
}
