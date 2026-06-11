import React from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { Server, Database, ShieldAlert, Activity, CheckCircle, XCircle } from 'lucide-react';

export default function SystemHealthCenter() {
  const { systemHealth } = useKingdomStore();

  if (!systemHealth) {
    return (
      <div className="flex justify-center items-center h-64 text-slate-500 font-mono">
        <Activity className="w-5 h-5 mr-3 animate-pulse" />
        Scanning Civilization Infrastructure Reality...
      </div>
    );
  }

  const { version, uptime_seconds, civilization_status, infrastructure, subsystems, reality_enforcement } = systemHealth;
  
  const uptimeStr = new Date(uptime_seconds * 1000).toISOString().substr(11, 8);
  const isHealthy = civilization_status === "ONLINE_AND_STABLE";

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-orbitron font-bold text-slate-100 flex items-center">
            <Server className="w-6 h-6 mr-3 text-cyan-400" />
            Infrastructure Reality Engine
          </h2>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Validating persistence layer integrity and cognitive execution reality. (v{version})
          </p>
        </div>
        
        <div className={`px-4 py-2 rounded-lg font-mono text-sm font-bold flex items-center shadow-lg ${
          isHealthy 
            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
            : 'bg-red-500/10 text-red-400 border border-red-500/20 animate-pulse'
        }`}>
          {isHealthy ? <CheckCircle className="w-4 h-4 mr-2" /> : <ShieldAlert className="w-4 h-4 mr-2" />}
          STATUS: {civilization_status}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        {/* Postgres */}
        <div className={`p-4 rounded-xl border backdrop-blur-sm ${infrastructure.postgres === 'ONLINE' ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-red-500/5 border-red-500/20'}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-300 text-sm font-bold">PostgreSQL</span>
            <Database className={`w-4 h-4 ${infrastructure.postgres === 'ONLINE' ? 'text-emerald-400' : 'text-red-400'}`} />
          </div>
          <div className="text-xs text-slate-500 uppercase">Relational Core</div>
          <div className={`mt-2 text-sm font-bold ${infrastructure.postgres === 'ONLINE' ? 'text-emerald-400' : 'text-red-400'}`}>
            {infrastructure.postgres}
          </div>
        </div>

        {/* Redis */}
        <div className={`p-4 rounded-xl border backdrop-blur-sm ${infrastructure.redis === 'ONLINE' ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-red-500/5 border-red-500/20'}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-300 text-sm font-bold">Redis Streams</span>
            <Activity className={`w-4 h-4 ${infrastructure.redis === 'ONLINE' ? 'text-emerald-400' : 'text-red-400'}`} />
          </div>
          <div className="text-xs text-slate-500 uppercase">Event Bus</div>
          <div className={`mt-2 text-sm font-bold ${infrastructure.redis === 'ONLINE' ? 'text-emerald-400' : 'text-red-400'}`}>
            {infrastructure.redis}
          </div>
        </div>

        {/* Qdrant */}
        <div className={`p-4 rounded-xl border backdrop-blur-sm ${infrastructure.qdrant === 'ONLINE' ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-yellow-500/5 border-yellow-500/20'}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-300 text-sm font-bold">Qdrant Vector</span>
            <Database className={`w-4 h-4 ${infrastructure.qdrant === 'ONLINE' ? 'text-emerald-400' : 'text-yellow-400'}`} />
          </div>
          <div className="text-xs text-slate-500 uppercase">Semantic Memory</div>
          <div className={`mt-2 text-sm font-bold ${infrastructure.qdrant === 'ONLINE' ? 'text-emerald-400' : 'text-yellow-400'}`}>
            {infrastructure.qdrant}
          </div>
        </div>

        {/* Neo4j */}
        <div className={`p-4 rounded-xl border backdrop-blur-sm ${infrastructure.neo4j === 'ONLINE' ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-yellow-500/5 border-yellow-500/20'}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-300 text-sm font-bold">Neo4j Graph</span>
            <Database className={`w-4 h-4 ${infrastructure.neo4j === 'ONLINE' ? 'text-emerald-400' : 'text-yellow-400'}`} />
          </div>
          <div className="text-xs text-slate-500 uppercase">Topology Memory</div>
          <div className={`mt-2 text-sm font-bold ${infrastructure.neo4j === 'ONLINE' ? 'text-emerald-400' : 'text-yellow-400'}`}>
            {infrastructure.neo4j}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-sm font-bold text-cyan-400 mb-4 font-orbitron">Cognitive Subsystems</h3>
          <div className="space-y-3 font-mono text-sm">
            {Object.entries(subsystems || {}).map(([key, val]) => (
              <div key={key} className="flex justify-between items-center border-b border-white/5 pb-2">
                <span className="text-slate-300">{key}</span>
                <span className={`px-2 py-0.5 rounded text-xs ${val === 'ONLINE' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                  {String(val)}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white/5 border border-white/10 rounded-xl p-5">
          <h3 className="text-sm font-bold text-cyan-400 mb-4 font-orbitron">Execution Reality Audit</h3>
          <div className="space-y-3 font-mono text-sm">
            <div className="flex justify-between items-center border-b border-white/5 pb-2">
              <span className="text-slate-300">Enforcement Policy</span>
              <span className="text-emerald-400 font-bold">{reality_enforcement}</span>
            </div>
            <div className="flex justify-between items-center border-b border-white/5 pb-2">
              <span className="text-slate-300">Continuous Uptime</span>
              <span className="text-cyan-400">{uptimeStr}</span>
            </div>
            <div className="flex justify-between items-center border-b border-white/5 pb-2">
              <span className="text-slate-300">Mock Fallbacks</span>
              <span className="bg-red-500/20 text-red-400 px-2 py-0.5 rounded text-xs">DISABLED</span>
            </div>
          </div>
        </div>
      </div>
      
      {!isHealthy && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 font-mono text-sm text-red-300">
          <p className="font-bold mb-2 flex items-center">
            <XCircle className="w-4 h-4 mr-2" />
            INFRASTRUCTURE DEGRADATION DETECTED
          </p>
          <p>
            The civilization has detected a loss of connection to critical persistence components. 
            Execution and memory formulation will be paused or quarantined until full infrastructure connection is restored.
          </p>
        </div>
      )}
    </div>
  );
}
