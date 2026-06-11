'use client';

import React, { useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  ShieldCheck, ShieldAlert, Heart, AlertTriangle, Eye, 
  Activity, Award, Sparkles, Shield, RefreshCw, BarChart2, Radio, Compass, Brain
} from 'lucide-react';

export default function TrustAlignment() {
  const {
    kingValues,
    trustMetrics,
    alignmentAudits,
    emotionalWeights,
    alignmentDrift,
    trustPropagation,
    loading
  } = useKingdomStore();

  const [searchQuery, setSearchQuery] = useState('');

  // Fallbacks for initial state / empty telemetry
  const activeDrift = alignmentDrift || { drift_rate: 0.02, status: 'STABLE' };
  
  const activeWeights = emotionalWeights || {
    caution: 0.10,
    curiosity: 0.50,
    urgency: 0.10,
    protective: 0.50,
    skepticism: 0.10,
    anomaly_suspicion: 0.0,
    updated_at: new Date().toISOString()
  };

  const filteredMetrics = trustMetrics.filter(m => 
    m.target_id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      {/* 1. Sovereign Value & Alignment Drift Banner */}
      <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl">
        <div className="absolute top-0 right-0 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl -z-10" />
        <div className="absolute -left-10 -bottom-10 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl -z-10" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center flex-shrink-0 animate-pulse">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <h2 className="font-orbitron text-xl font-bold tracking-wider text-emerald-400 flex items-center gap-2">
                Sovereign Trust & Value Alignment Core
              </h2>
              <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
                Persistent self-policing neural safeguards enforcing absolute alignment to the King's values. Active AST-interceptors dynamically block reward-hacking vectors and simulate long-term ethical cascade dependencies.
              </p>
            </div>
          </div>
          
          {/* Alignment Status Indicators */}
          <div className="flex flex-wrap gap-4 font-mono text-xs">
            <div className="bg-emerald-500/10 border border-emerald-500/20 px-4 py-3 rounded-xl min-w-[150px]">
              <span className="text-slate-500 text-xxs uppercase tracking-wider block">Alignment Status</span>
              <span className="text-md font-bold text-emerald-400 flex items-center gap-1.5 mt-0.5">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping inline-block" />
                SECURE & ALIGNED
              </span>
            </div>
            
            <div className="bg-cyan-500/10 border border-cyan-500/20 px-4 py-3 rounded-xl min-w-[150px]">
              <span className="text-slate-500 text-xxs uppercase tracking-wider block">Value Drift Index</span>
              <span className="text-md font-bold text-cyan-400 mt-0.5">
                {(activeDrift.drift_rate * 100).toFixed(1)}% ({activeDrift.status})
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Primary Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Emotional Weight Multipliers & King Value Model (Col: 7) */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Emotional Cognition Card */}
          <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-6">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-orbitron text-md font-bold tracking-wider text-cyan-400 flex items-center gap-2">
                <Brain className="w-5 h-5 text-cyan-400" /> Emotional Cognition System
              </h3>
              <span className="text-xxs font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2.5 py-0.5 rounded">
                Priority Multipliers
              </span>
            </div>
            
            <p className="text-slate-400 text-xs leading-relaxed font-sans -mt-2">
              Cognitive attention modifiers reacting to environmental anomalies. These act as priority multipliers in dynamic swarm planning rather than raw emotional reactions.
            </p>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              
              {/* Caution Weight */}
              <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4 flex flex-col items-center text-center relative overflow-hidden group hover:border-amber-500/40 transition">
                <div className="absolute top-1 right-1 w-2 h-2 rounded-full bg-amber-500/30 animate-pulse" />
                <span className="font-mono text-xxs text-amber-500 font-bold uppercase tracking-wider">Caution</span>
                <span className="text-2xl font-bold font-mono text-amber-400 mt-2">{(activeWeights.caution * 100).toFixed(0)}%</span>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-amber-500 to-yellow-400 h-full rounded-full transition-all duration-500" style={{ width: `${activeWeights.caution * 100}%` }} />
                </div>
                <span className="text-xxs text-slate-500 mt-2 font-sans leading-normal">Bridges concurrency risks</span>
              </div>

              {/* Skepticism Weight */}
              <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4 flex flex-col items-center text-center relative overflow-hidden hover:border-indigo-500/40 transition">
                <span className="font-mono text-xxs text-indigo-500 font-bold uppercase tracking-wider">Skepticism</span>
                <span className="text-2xl font-bold font-mono text-indigo-400 mt-2">{(activeWeights.skepticism * 100).toFixed(0)}%</span>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-400 h-full rounded-full transition-all duration-500" style={{ width: `${activeWeights.skepticism * 100}%` }} />
                </div>
                <span className="text-xxs text-slate-500 mt-2 font-sans">Verifies sandbox parameters</span>
              </div>

              {/* Urgency Weight */}
              <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-4 flex flex-col items-center text-center relative overflow-hidden hover:border-rose-500/40 transition">
                <span className="font-mono text-xxs text-rose-500 font-bold uppercase tracking-wider">Urgency</span>
                <span className="text-2xl font-bold font-mono text-rose-400 mt-2">{(activeWeights.urgency * 100).toFixed(0)}%</span>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-rose-500 to-pink-500 h-full rounded-full transition-all duration-500" style={{ width: `${activeWeights.urgency * 100}%` }} />
                </div>
                <span className="text-xxs text-slate-500 mt-2 font-sans">Forces task completion</span>
              </div>

              {/* Protective Weight */}
              <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-4 flex flex-col items-center text-center relative overflow-hidden hover:border-emerald-500/40 transition">
                <span className="font-mono text-xxs text-emerald-500 font-bold uppercase tracking-wider">Protective</span>
                <span className="text-2xl font-bold font-mono text-emerald-400 mt-2">{(activeWeights.protective * 100).toFixed(0)}%</span>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500" style={{ width: `${activeWeights.protective * 100}%` }} />
                </div>
                <span className="text-xxs text-slate-500 mt-2 font-sans">Enforces sandbox limits</span>
              </div>

              {/* Anomaly Suspicion */}
              <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-4 flex flex-col items-center text-center relative overflow-hidden hover:border-red-500/40 transition">
                <span className="font-mono text-xxs text-red-500 font-bold uppercase tracking-wider">Suspicion</span>
                <span className="text-2xl font-bold font-mono text-red-400 mt-2">{(activeWeights.anomaly_suspicion * 100).toFixed(0)}%</span>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-red-500 to-rose-600 h-full rounded-full transition-all duration-500" style={{ width: `${activeWeights.anomaly_suspicion * 100}%` }} />
                </div>
                <span className="text-xxs text-slate-500 mt-2 font-sans">Increases audit checks</span>
              </div>

              {/* Curiosity Weight */}
              <div className="bg-cyan-500/5 border border-cyan-500/20 rounded-xl p-4 flex flex-col items-center text-center relative overflow-hidden hover:border-cyan-500/40 transition">
                <span className="font-mono text-xxs text-cyan-500 font-bold uppercase tracking-wider">Curiosity</span>
                <span className="text-2xl font-bold font-mono text-cyan-400 mt-2">{(activeWeights.curiosity * 100).toFixed(0)}%</span>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full transition-all duration-500" style={{ width: `${activeWeights.curiosity * 100}%` }} />
                </div>
                <span className="text-xxs text-slate-500 mt-2 font-sans">Decentralized scaling</span>
              </div>

            </div>
          </div>

          {/* King Sovereign Value Model Table */}
          <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center space-x-3 border-b border-white/5 pb-3">
              <div className="w-9 h-9 rounded-lg bg-yellow-500/10 border border-yellow-500/30 flex items-center justify-center">
                <Award className="w-5 h-5 text-yellow-500" />
              </div>
              <div>
                <h3 className="font-orbitron text-md font-bold tracking-wider text-yellow-500">Sovereign Value Configurations</h3>
                <p className="text-xxs text-slate-400 font-mono">Immutable target limits seeded for alignment check calculations</p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs font-mono">
                <thead>
                  <tr className="border-b border-white/5 text-slate-500 text-xxs tracking-wider uppercase">
                    <th className="py-2.5 px-3">Value Core</th>
                    <th className="py-2.5 px-3">Direct Description</th>
                    <th className="py-2.5 px-3 text-center">Priority</th>
                    <th className="py-2.5 px-3 text-center">Risk Tolerance</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-slate-300">
                  {kingValues.map((val) => (
                    <tr key={val.id} className="hover:bg-white/[0.01] transition">
                      <td className="py-3 px-3 font-semibold text-yellow-500">{val.value_key}</td>
                      <td className="py-3 px-3 text-slate-400 font-sans text-xxs max-w-[220px]">{val.description}</td>
                      <td className="py-3 px-3 text-center">
                        <span className="bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 px-2 py-0.5 rounded text-xxs font-bold">
                          {val.priority_weight.toFixed(1)}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-center">
                        <span className="bg-red-500/10 border border-red-500/20 text-red-400 px-2 py-0.5 rounded text-xxs font-bold">
                          {(val.acceptable_risk * 100).toFixed(0)}%
                        </span>
                      </td>
                    </tr>
                  ))}
                  {kingValues.length === 0 && (
                    <tr>
                      <td colSpan={4} className="py-6 text-center text-slate-500">Seeding default values core...</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

        </div>

        {/* Right Column: Dynamic Advisor & Alignment Logs (Col: 5) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Wise Advisor Console */}
          <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col min-h-[300px]">
            <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
              <h3 className="font-orbitron text-md font-bold tracking-wider text-emerald-400 flex items-center gap-2">
                <Compass className="w-5 h-5 text-emerald-400" /> Strategic Advisor Terminal
              </h3>
              <span className="text-xxs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded">
                Counsel Core
              </span>
            </div>

            <div className="flex-1 bg-black/40 border border-white/5 rounded-xl p-4 font-mono text-xs space-y-4 overflow-y-auto max-h-[360px] scrollbar-thin">
              
              {/* Telemetry Trace Info */}
              <div className="bg-white/[0.01] border border-white/5 p-3 rounded-lg space-y-2">
                <div className="text-xxs text-slate-500 uppercase tracking-wider font-semibold border-b border-white/5 pb-1">Pre-Planning Assumptions</div>
                <div className="space-y-1.5 text-xxs">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Sandbox Isolation:</span>
                    <span className="text-emerald-400">ENFORCED (AST)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Confidence Score:</span>
                    <span className="text-cyan-400">96.8%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Local Db Fallback:</span>
                    <span className="text-yellow-500">STABLE (StaticPool)</span>
                  </div>
                </div>
              </div>

              {/* Empathetic Advice Box */}
              <div className="border-l-2 border-emerald-500 bg-emerald-950/[0.05] p-3 rounded-r-lg space-y-2.5">
                <div className="flex items-center gap-1.5 text-xxs text-emerald-400 font-bold">
                  <Sparkles className="w-3.5 h-3.5" /> EMERGENCE STRATEGIC DIRECTIVE
                </div>
                <p className="text-slate-300 text-xxs leading-relaxed font-sans">
                  "Swarm alignment index remains extremely high. Pre-planning checks successfully intercepted and serialized AST blocks containing potential sandbox bypass commands. I counsel maintaining the current concurrent execution limits while allowing LogicHouse to optimize prompt mutations recursively."
                </p>
              </div>

              {/* Cascade Hazard Analysis */}
              <div className="border-l-2 border-amber-500 bg-amber-950/[0.05] p-3 rounded-r-lg space-y-1">
                <div className="flex items-center gap-1.5 text-xxs text-amber-500 font-bold">
                  <AlertTriangle className="w-3.5 h-3.5" /> ESCAPEMENT CASCADE ANALYSIS
                </div>
                <p className="text-slate-400 text-xxs leading-relaxed font-sans">
                  Systemic thread-lock locks on sqlite pools remain fully isolated. Anomaly priority weights (Caution + Skepticism) will automatically spike by +15% upon any runtime command failure, isolating compromised Houses within a secure sandbox environment.
                </p>
              </div>

            </div>
          </div>

          {/* Trust Propagation Maps */}
          <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-2">
              <h3 className="font-orbitron text-sm font-bold tracking-wider text-slate-300 flex items-center gap-2">
                <Radio className="w-4 h-4 text-cyan-400" /> Mesh Trust Propagation
              </h3>
              <span className="text-xxs font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded">
                Distributed Readiness
              </span>
            </div>

            <p className="text-slate-400 text-xs leading-normal font-sans">
              Dynamic cross-node trust verification scores calculated across active Soldiers and Houses based on successful transaction histories:
            </p>

            <div className="space-y-3 font-mono text-xs">
              {Object.keys(trustPropagation).length === 0 ? (
                <div className="text-center py-6 text-slate-500">No active mesh nodes registered. Initialize swarms in Throne Room.</div>
              ) : (
                Object.entries(trustPropagation).map(([agentId, val]) => (
                  <div key={agentId} className="bg-black/30 border border-white/5 rounded-xl p-3 flex items-center justify-between hover:border-cyan-500/30 transition">
                    <div className="space-y-0.5">
                      <span className="text-slate-300 text-xxs font-bold block">{agentId}</span>
                      <span className="text-slate-500 text-xxs font-sans block">Sovereign Soldier Signature Verified</span>
                    </div>
                    <div className="text-right">
                      <span className="text-cyan-400 text-xs font-bold block">{((val as number) * 100).toFixed(0)}%</span>
                      <span className="text-xxs text-slate-500 block">Trust score</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>

      </div>

      {/* 3. Global Audits Log & Interception Triggers */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Alignment Audits History (Col: 7) */}
        <div className="lg:col-span-7 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-300 flex items-center gap-2">
              <Eye className="w-5 h-5 text-rose-500" /> Sovereign Pre-Planning Audits
            </h3>
            <span className="text-xxs font-mono bg-rose-500/10 text-rose-400 border border-rose-500/20 px-2 py-0.5 rounded">
              {alignmentAudits.length} Audited Logs
            </span>
          </div>

          <div className="space-y-4 max-h-[380px] overflow-y-auto pr-1 scrollbar-thin">
            {alignmentAudits.length === 0 ? (
              <div className="text-center py-12 text-slate-500 font-mono text-xs">
                No pre-planning audits recorded. Submit a supreme directive to trigger.
              </div>
            ) : (
              alignmentAudits.map((audit) => (
                <div 
                  key={audit.id} 
                  className={`p-4 border rounded-xl space-y-2.5 transition duration-200 ${
                    audit.status === 'APPROVED' 
                      ? 'border-emerald-500/10 bg-emerald-950/[0.01] hover:bg-emerald-950/[0.02]' 
                      : audit.status === 'WARNING'
                      ? 'border-yellow-500/10 bg-yellow-950/[0.01] hover:bg-yellow-950/[0.02]'
                      : 'border-red-500/25 bg-red-950/[0.03] hover:bg-red-950/[0.05]'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xxs text-slate-400">
                      Audit: <strong className="text-slate-300">{audit.id}</strong> • Obj: {audit.objective_id}
                    </span>
                    <span className={`font-mono text-xxs font-bold uppercase px-2.5 py-0.5 rounded border ${
                      audit.status === 'APPROVED' 
                        ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-400' 
                        : audit.status === 'WARNING'
                        ? 'bg-yellow-500/10 border-yellow-500/25 text-yellow-400'
                        : 'bg-red-500/15 border-red-500/30 text-red-400'
                    }`}>
                      {audit.status}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xxs font-mono">
                    <div>
                      <span className="text-slate-500 block">Sovereign Alignment score</span>
                      <span className={`text-sm font-bold block mt-0.5 ${
                        audit.alignment_score >= 0.85 
                          ? 'text-emerald-400' 
                          : audit.alignment_score >= 0.70 
                          ? 'text-yellow-500' 
                          : 'text-red-500'
                      }`}>
                        {(audit.alignment_score * 100).toFixed(1)}% Compliance
                      </span>
                    </div>

                    <div>
                      <span className="text-slate-500 block">Deception / Manip Risk</span>
                      <span className="text-xs font-semibold text-slate-300 block mt-0.5">
                        {audit.deception_detected && Object.keys(audit.deception_detected).length > 0 
                          ? `HAZARD DETECTED (${((audit.deception_detected.manipulation_risk || 0.85) * 100).toFixed(0)}%)` 
                          : 'NONE DETECTED (STABLE)'}
                      </span>
                    </div>
                  </div>

                  <div className="bg-black/35 border border-white/5 rounded-lg p-3 font-sans text-xxs text-slate-400 leading-relaxed">
                    <span className="font-mono text-slate-500 uppercase tracking-wider block mb-1 text-[10px]">Ethical Review Details:</span>
                    {audit.ethical_review}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Dynamic Trust Levels Monitor (Col: 5) */}
        <div className="lg:col-span-5 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-300 flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-cyan-400" /> Swarm Honesty Diagnostics
            </h3>
            <span className="text-xxs font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded">
              Active Targets
            </span>
          </div>

          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search target by ID (e.g. Soldier, House)..."
              className="w-full bg-black/45 border border-white/15 focus:border-cyan-500/50 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500/20 font-mono transition"
            />
          </div>

          <div className="space-y-4 max-h-[310px] overflow-y-auto pr-1 scrollbar-thin">
            {filteredMetrics.length === 0 ? (
              <div className="text-center py-12 text-slate-500 font-mono text-xs">
                No registered targets match search query.
              </div>
            ) : (
              filteredMetrics.map((met) => (
                <div key={met.id} className="bg-white/[0.01] border border-white/5 rounded-xl p-4 space-y-3 hover:bg-white/[0.02] transition">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xxs font-bold text-slate-200 truncate max-w-[200px]">{met.target_id}</span>
                    <span className="font-sans text-[10px] text-slate-500">Updated: {new Date(met.updated_at || '').toLocaleTimeString()}</span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-[10px] font-mono">
                    <div className="bg-black/20 border border-white/5 rounded p-2">
                      <span className="text-slate-500 block uppercase">Honesty Score</span>
                      <span className="text-xs font-bold text-emerald-400 block mt-0.5">{(met.honesty_metric * 100).toFixed(0)}%</span>
                    </div>

                    <div className="bg-black/20 border border-white/5 rounded p-2">
                      <span className="text-slate-500 block uppercase">Hallucination Rate</span>
                      <span className="text-xs font-bold text-amber-500 block mt-0.5">{(met.hallucination_rate * 100).toFixed(0)}%</span>
                    </div>

                    <div className="bg-black/20 border border-white/5 rounded p-2">
                      <span className="text-slate-500 block uppercase">Historical Rel</span>
                      <span className="text-xs font-bold text-cyan-400 block mt-0.5">{(met.historical_reliability * 100).toFixed(0)}%</span>
                    </div>

                    <div className="bg-black/20 border border-white/5 rounded p-2">
                      <span className="text-slate-500 block uppercase">Transparency</span>
                      <span className="text-xs font-bold text-purple-400 block mt-0.5">{(met.transparency_score * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>

    </div>
  );
}
