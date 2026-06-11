'use client';

import React from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { Shield, ShieldAlert, ShieldCheck, Skull, Ban, HelpCircle, Activity } from 'lucide-react';

export default function SoldierMonitor() {
  const { topology, tasks } = useKingdomStore();

  // Extract all soldier nodes
  const soldiers = topology.nodes.filter(
    (n) => n.type === 'SOLDIER' || n.type === 'RETIRED_SOLDIER' || n.type === 'QUARANTINED_SOLDIER'
  );

  // Group task outputs and calculate individual soldier success/failure rates
  const getSoldierStats = (soldierId: string, status: string) => {
    const soldierTasks = tasks.filter((t) => t.assigned_soldier === soldierId || t.id.includes(soldierId) || t.title.includes(soldierId));
    const successes = soldierTasks.filter((t) => t.status === 'COMPLETED').length;
    const failures = soldierTasks.filter((t) => t.status === 'FAILED').length;
    const level = Math.max(1, Math.floor(successes / 3) + 1);

    // Calculate a trust rating from 0.0 to 1.0 (defaults to 1.0 if no tasks have executed yet)
    let trustScore = 1.0;
    if (successes + failures > 0) {
      trustScore = successes / (successes + failures);
    }
    
    // Force quarantine or retirement overrides
    if (status === 'QUARANTINED_SOLDIER') trustScore = 0.0;
    if (status === 'RETIRED_SOLDIER') trustScore = Math.max(0.4, trustScore * 0.7);

    return {
      successes: successes || (status === 'RETIRED_SOLDIER' ? 3 : 0),
      failures: failures || (status === 'QUARANTINED_SOLDIER' ? 1 : 0),
      level: status === 'QUARANTINED_SOLDIER' ? 1 : level,
      trustScore: parseFloat(trustScore.toFixed(2)),
    };
  };

  const getHouseName = (soldierId: string) => {
    if (soldierId.toLowerCase().includes('transformer')) return 'DataTransformer';
    if (soldierId.toLowerCase().includes('cryptographer')) return 'Cryptographer';
    if (soldierId.toLowerCase().includes('evolution')) return 'Evolver';
    if (soldierId.toLowerCase().includes('stability')) return 'Stabilizer';
    return 'General Swarm';
  };

  return (
    <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-6">
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center">
            <Activity className="w-5 h-5 text-teal-400" />
          </div>
          <div>
            <h2 className="font-orbitron text-md font-bold tracking-wider text-teal-400">Soldier Activity Monitor</h2>
            <p className="text-xxs text-slate-400 font-mono">Observe live operational state, trust quotients, and lifespans</p>
          </div>
        </div>
        <span className="text-xxs font-mono bg-teal-500/10 text-teal-400 border border-teal-500/20 px-2 py-0.5 rounded flex items-center gap-2">
          <span>{soldiers.filter(s => s.type === 'SOLDIER').length} Active</span>
          <span className="text-slate-500">|</span>
          <span className="text-slate-400">{soldiers.length} Total Deployed</span>
        </span>
      </div>

      {soldiers.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <span className="text-3xl opacity-40 mb-3">🛡️</span>
          <p className="text-slate-400 text-sm font-mono">No active soldiers spawned.</p>
          <p className="text-slate-600 text-xs font-mono mt-1">Spawning triggers dynamically upon objective analysis.</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 pb-3">
                <th className="pb-3 font-semibold tracking-wider">Soldier Address</th>
                <th className="pb-3 font-semibold tracking-wider">Assigned House</th>
                <th className="pb-3 font-semibold tracking-wider">Status</th>
                <th className="pb-3 font-semibold tracking-wider text-center">Level</th>
                <th className="pb-3 font-semibold tracking-wider text-center">Success / Failure</th>
                <th className="pb-3 font-semibold tracking-wider text-center">Trust Integrity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {soldiers.map((soldier) => {
                const stats = getSoldierStats(soldier.id, soldier.type);
                const house = getHouseName(soldier.id);
                
                // Set status elements
                let statusBadge = (
                  <span className="flex items-center gap-1.5 text-teal-400 bg-teal-500/10 border border-teal-500/20 px-2 py-0.5 rounded-full text-xxs font-bold">
                    <ShieldCheck className="w-3.5 h-3.5" /> ACTIVE
                  </span>
                );
                if (soldier.type === 'RETIRED_SOLDIER') {
                  statusBadge = (
                    <span className="flex items-center gap-1.5 text-slate-500 bg-slate-500/5 border border-slate-500/10 px-2 py-0.5 rounded-full text-xxs font-bold">
                      <Skull className="w-3.5 h-3.5" /> RETIRED
                    </span>
                  );
                } else if (soldier.type === 'QUARANTINED_SOLDIER') {
                  statusBadge = (
                    <span className="flex items-center gap-1.5 text-red-500 bg-red-500/10 border border-red-500/20 px-2 py-0.5 rounded-full text-xxs font-bold animate-pulse">
                      <ShieldAlert className="w-3.5 h-3.5" /> QUARANTINED
                    </span>
                  );
                }

                // Trust bar colors
                const trustColor = 
                  stats.trustScore >= 0.8 ? 'bg-teal-500 shadow-teal-500/30' :
                  stats.trustScore >= 0.5 ? 'bg-yellow-500 shadow-yellow-500/30' :
                  'bg-red-500 shadow-red-500/30';

                return (
                  <tr key={soldier.id} className="hover:bg-white/[0.01] transition duration-200">
                    <td className="py-3.5 font-semibold text-slate-200">{soldier.id}</td>
                    <td className="py-3.5 text-slate-400">{house}</td>
                    <td className="py-3.5">{statusBadge}</td>
                    <td className="py-3.5 text-center font-bold text-slate-300">{stats.level}</td>
                    <td className="py-3.5 text-center font-semibold text-slate-300">
                      <span className="text-emerald-400">{stats.successes}</span>
                      <span className="text-slate-600"> / </span>
                      <span className="text-red-400">{stats.failures}</span>
                    </td>
                    <td className="py-3.5">
                      <div className="flex items-center justify-center gap-3">
                        <div className="w-24 h-2 bg-black/40 border border-white/5 rounded-full overflow-hidden">
                          <div 
                            style={{ width: `${stats.trustScore * 100}%` }}
                            className={`h-full rounded-full shadow-[0_0_8px] transition-all duration-500 ${trustColor}`}
                          />
                        </div>
                        <span className="font-bold text-slate-300 text-xxs w-8">{stats.trustScore}</span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
