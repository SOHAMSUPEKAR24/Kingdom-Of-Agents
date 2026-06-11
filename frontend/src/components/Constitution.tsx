'use client';

import React from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { Scale, Lock, Key, Zap, CheckCircle2 } from 'lucide-react';

export default function Constitution() {
  const { 
    constitutionalRules, 
    discretionaryPermissions, 
    houseWeights, 
    togglePermission 
  } = useKingdomStore();

  const handleToggle = (key: string, currentValue: boolean) => {
    togglePermission(key, !currentValue);
  };

  // Human-readable labels for discretionary keys
  const permissionLabels: Record<string, { title: string; desc: string }> = {
    autonomous_scaling: {
      title: 'Autonomous Scaling (Spawning)',
      desc: 'Allows the system to recursively spawn disposable workers without asking the King.',
    },
    replication_permissions: {
      title: 'Self-Replication Permissions',
      desc: 'Allows soldiers to clone themselves to accelerate parallel workloads.',
    },
    reinforcement_sensitivity: {
      title: 'Adaptive Reward Sensitivity',
      desc: 'Enables high-frequency prompt mutating algorithms on success thresholds.',
    },
    quarantine_strictness: {
      title: 'Aggressive Threat Isolation',
      desc: 'Instantly quarantines entire Houses if performance index is compromised.',
    },
    evolution_aggressiveness: {
      title: 'Runtime Tool Creation',
      desc: 'Allows dynamic tool creation sandboxes to run testing environments directly.',
    },
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      {/* 1. Immutable Sovereign Laws (Col: 7) */}
      <div className="lg:col-span-7 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-6">
        <div className="flex items-center space-x-3 border-b border-white/5 pb-3">
          <div className="w-10 h-10 rounded-lg bg-red-500/10 border border-red-500/30 flex items-center justify-center">
            <Scale className="w-5 h-5 text-red-400" />
          </div>
          <div>
            <h2 className="font-orbitron text-md font-bold tracking-wider text-red-400">Constitution Chamber</h2>
            <p className="text-xxs text-slate-400 font-mono">Immutable laws of the digital kingdom governed by King authority</p>
          </div>
        </div>

        <div className="space-y-4 max-h-[460px] overflow-y-auto pr-1 scrollbar-thin">
          {constitutionalRules.length === 0 ? (
            <div className="text-center py-12 text-slate-500 font-mono text-xs">
              Loading immutable sovereign laws...
            </div>
          ) : (
            constitutionalRules.map((rule) => (
              <div 
                key={rule.id} 
                className="p-4 border border-red-500/10 bg-red-950/[0.02] rounded-xl flex items-start gap-3.5 transition duration-200 hover:bg-red-950/[0.04]"
              >
                <div className="w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Lock className="w-4 h-4 text-red-400" />
                </div>
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h4 className="font-bold text-sm text-slate-200 font-sans">{rule.title}</h4>
                    <span className="text-xxs font-mono bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded">
                      IMMUTABLE
                    </span>
                  </div>
                  <p className="text-slate-400 text-xs font-sans leading-relaxed">{rule.description}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* 2. Discretionary Settings & House Coordination Panels (Col: 5) */}
      <div className="lg:col-span-5 space-y-6">
        
        {/* Discretionary Authority */}
        <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center space-x-3 border-b border-white/5 pb-2">
            <Key className="w-4 h-4 text-yellow-500" />
            <h3 className="font-orbitron text-sm font-bold tracking-wider text-yellow-500">Discretionary Permissions</h3>
          </div>

          <div className="space-y-4 font-mono text-xs">
            {Object.keys(discretionaryPermissions).length === 0 ? (
              <div className="text-center py-6 text-slate-500">
                Loading authority permissions...
              </div>
            ) : (
              Object.entries(discretionaryPermissions).map(([key, val]) => {
                const meta = permissionLabels[key] || {
                  title: key.replace(/_/g, ' '),
                  desc: 'Custom system toggle permission setting.',
                };

                return (
                  <div key={key} className="flex items-start justify-between gap-4 p-3 bg-white/[0.01] hover:bg-white/[0.02] border border-white/5 rounded-xl transition duration-200">
                    <div className="space-y-1">
                      <div className="font-bold text-slate-200">{meta.title}</div>
                      <p className="text-xxs text-slate-400 leading-normal font-sans">{meta.desc}</p>
                    </div>

                    <button
                      onClick={() => handleToggle(key, !!val)}
                      className={`relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
                        val ? 'bg-yellow-500' : 'bg-slate-700'
                      }`}
                    >
                      <span
                        className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-black shadow ring-0 transition duration-200 ease-in-out ${
                          val ? 'translate-x-4' : 'translate-x-0'
                        }`}
                      />
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* House Weights coordination */}
        <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center space-x-3 border-b border-white/5 pb-2">
            <Zap className="w-4 h-4 text-cyan-400" />
            <h3 className="font-orbitron text-sm font-bold tracking-wider text-cyan-400">House Coordination Weights</h3>
          </div>

          <div className="space-y-4 font-mono text-xs">
            {Object.keys(houseWeights).length === 0 ? (
              <div className="text-center py-6 text-slate-500">
                Waiting for House reinforcement metrics...
              </div>
            ) : (
              Object.entries(houseWeights).map(([house, weight]) => (
                <div key={house} className="space-y-1.5 p-3 bg-white/[0.01] border border-white/5 rounded-xl">
                  <div className="flex items-center justify-between text-xxs">
                    <span className="font-bold text-slate-200">{house}</span>
                    <span className="text-cyan-400 font-semibold flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> W = {weight.toFixed(2)}
                    </span>
                  </div>
                  <div className="w-full h-2 bg-black/40 border border-white/5 rounded-full overflow-hidden">
                    <div 
                      style={{ width: `${Math.min(100, weight * 100)}%` }}
                      className="h-full bg-cyan-500 rounded-full shadow-[0_0_8px_#00f2fe] transition-all duration-500"
                    />
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
