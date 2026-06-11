'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { Terminal, ShieldAlert, Sparkles, Filter, ChevronDown } from 'lucide-react';

export default function Observability() {
  const { logs } = useKingdomStore();
  const [filter, setFilter] = useState('');
  const [autoScroll, setAutoScroll] = useState(true);
  const terminalEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll logic
  useEffect(() => {
    if (autoScroll && terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, autoScroll]);

  // Scan logs for sandbox isolations or critical errors in the active set
  const cognitiveAnomalies = logs.slice(0, 30).filter(
    (log) => 
      log.priority === 'CRITICAL' || 
      log.priority === 'ERROR' ||
      log.message.toLowerCase().includes('quarantine') ||
      log.message.toLowerCase().includes('violation') ||
      log.message.toLowerCase().includes('hallucination')
  );

  const filteredLogs = logs.filter(
    (log) => 
      log.sender.toLowerCase().includes(filter.toLowerCase()) ||
      log.message.toLowerCase().includes(filter.toLowerCase()) ||
      log.priority.toLowerCase().includes(filter.toLowerCase())
  );

  const priorityColors = {
    INFO: 'text-cyan-400 font-medium',
    WARNING: 'text-yellow-400 font-semibold',
    ERROR: 'text-rose-500 font-bold',
    CRITICAL: 'text-red-500 font-extrabold animate-pulse bg-red-500/10 border border-red-500/20 px-1 rounded',
  };

  return (
    <div className={`backdrop-blur-md bg-white/5 border rounded-2xl p-6 shadow-2xl space-y-6 transition duration-500 ${
      cognitiveAnomalies.length > 0 ? 'border-red-500/40 shadow-red-500/10 animate-border-pulse' : 'border-white/10'
    }`}>
      {/* Risk Alert dropdown Banner */}
      {cognitiveAnomalies.length > 0 && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center justify-between gap-4 animate-slide-up">
          <div className="flex items-center space-x-3 text-red-500">
            <ShieldAlert className="w-5 h-5 animate-pulse" />
            <div>
              <h4 className="font-orbitron font-bold text-xs tracking-wider uppercase">COGNITIVE ANOMALY DETECTED</h4>
              <p className="text-xxs text-red-400/90 font-mono">Sandbox isolations are active. An agent has violated structural validation checks.</p>
            </div>
          </div>
          <span className="text-xxs font-mono bg-red-500/20 border border-red-500/40 px-2 py-0.5 rounded text-red-400 font-bold">
            QUARANTINE LOCK
          </span>
        </div>
      )}

      {/* Terminal Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-white/5 pb-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
            <Terminal className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h2 className="font-orbitron text-md font-bold tracking-wider text-cyan-400">Observability Realm</h2>
            <p className="text-xxs text-slate-400 font-mono">Real-time terminal event streaming of civilization cognition logs</p>
          </div>
        </div>

        {/* Filter Toolbar */}
        <div className="flex items-center gap-3 w-full md:w-auto font-mono text-xxs">
          <div className="relative flex-1 md:w-56">
            <input
              type="text"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              placeholder="Filter trace stream..."
              className="w-full bg-black/40 border border-white/10 rounded-xl pl-8 pr-4 py-2 text-white focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition"
            />
            <Filter className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-500" />
          </div>
          
          <label className="flex items-center gap-2 text-slate-400 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
              className="accent-cyan-500 bg-black/40 border border-white/10"
            />
            Auto-Scroll
          </label>
        </div>
      </div>

      {/* Terminal Log Console */}
      <div className="bg-black/80 border border-white/5 rounded-xl p-5 h-80 overflow-y-auto font-mono text-xxs leading-normal scrollbar-thin select-text space-y-2">
        {filteredLogs.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-600">
            Waiting for real-time observability logs...
          </div>
        ) : (
          filteredLogs.map((log, idx) => {
            const time = new Date(log.timestamp).toLocaleTimeString();
            const priorityClass = priorityColors[log.priority as keyof typeof priorityColors] || '';

            return (
              <div key={idx} className="flex flex-wrap gap-x-2 py-0.5 hover:bg-white/[0.02] rounded px-1.5 transition">
                <span className="text-slate-600">[{time}]</span>
                <span className={priorityClass}>[{log.priority}]</span>
                <span className="text-purple-400 font-semibold">{log.sender}:</span>
                <span className="text-slate-300 break-words flex-1">{log.message}</span>
              </div>
            );
          })
        )}
        <div ref={terminalEndRef} />
      </div>

      {/* Observability Statistics Footer */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xxs text-slate-400">
        <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl space-y-1">
          <span className="text-slate-500 uppercase tracking-wider block">Execution Depth</span>
          <span className="font-bold text-slate-200 text-xs flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" /> Recursive Dynamic
          </span>
        </div>
        <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl space-y-1">
          <span className="text-slate-500 uppercase tracking-wider block">Latency Status</span>
          <span className="font-bold text-emerald-400 text-xs font-mono">0.05ms (Redis-bus)</span>
        </div>
        <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl space-y-1">
          <span className="text-slate-500 uppercase tracking-wider block">Quarantine State</span>
          <span className={`font-bold text-xs ${cognitiveAnomalies.length > 0 ? 'text-red-500 animate-pulse' : 'text-teal-400'}`}>
            {cognitiveAnomalies.length > 0 ? 'Threat Isolated' : 'System Secure'}
          </span>
        </div>
        <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl space-y-1">
          <span className="text-slate-500 uppercase tracking-wider block">Total Log Entries</span>
          <span className="font-bold text-slate-200 text-xs">{logs.length} Entries</span>
        </div>
      </div>
    </div>
  );
}
