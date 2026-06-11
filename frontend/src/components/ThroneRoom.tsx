'use client';

import React, { useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { Send, Cpu, Award, Zap, AlertTriangle } from 'lucide-react';

export default function ThroneRoom() {
  const [objective, setObjective] = useState('');
  const { submitObjective, tasks, logs, loading, error, clearError } = useKingdomStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!objective.trim() || loading) return;
    try {
      await submitObjective(objective);
      setObjective('');
    } catch {
      // Errors are handled in the Zustand store
    }
  };

  // Filter Knight strategic logs
  const knightLogs = logs
    .filter(log => log.sender.toLowerCase().includes('knight') || log.message.toLowerCase().includes('knight'))
    .slice(0, 15);

  // Group tasks by their level or build simple DAG levels
  const roots = tasks.filter(t => !t.dependencies || t.dependencies.length === 0);

  return (
    <div className="space-y-6">
      {/* 1. King Command Input Card */}
      <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl">
        <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl -z-10" />
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-yellow-500/10 border border-yellow-500/30 flex items-center justify-center">
            <span className="text-xl">👑</span>
          </div>
          <div>
            <h2 className="font-orbitron text-xl font-bold tracking-wider text-yellow-500">Throne Command Console</h2>
            <p className="text-xs text-slate-400">Issue supreme directives to the multi-agent cognitive civilization</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center justify-between">
            <span className="text-xs text-red-400 font-mono flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-500" /> {error}
            </span>
            <button onClick={clearError} className="text-xs text-slate-400 hover:text-white font-mono">✕</button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            disabled={loading}
            placeholder="Supreme directive... e.g. Design base64 xor cryptographer and transform target logs"
            className="flex-1 bg-black/40 border border-white/10 focus:border-cyan-500/50 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500/20 font-mono transition"
          />
          <button
            type="submit"
            disabled={loading || !objective.trim()}
            className="bg-yellow-500/10 border border-yellow-500/30 hover:bg-yellow-500/20 text-yellow-500 px-6 py-3 rounded-xl flex items-center gap-2 text-sm font-orbitron tracking-wider transition disabled:opacity-50 cursor-pointer"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            Orchestrate
          </button>
        </form>
      </div>

      {/* 2. Grid for Task DAG Tree & Knight-0 Reasoning */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Task DAG Viewer (Col: 7) */}
        <div className="lg:col-span-7 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col min-h-[400px]">
          <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-300 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-cyan-400" /> Active Objective DAG Pipeline
            </h3>
            <span className="text-xxs font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded">
              {tasks.length} Active Nodes
            </span>
          </div>

          {tasks.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
              <span className="text-4xl opacity-40 mb-3">🕸️</span>
              <p className="text-slate-400 text-sm font-mono">No active objectives executing.</p>
              <p className="text-slate-600 text-xs font-mono mt-1">Issue a command above to construct an execution tree.</p>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto space-y-4 max-h-[420px] pr-2 scrollbar-thin">
              {roots.map(root => (
                <div key={root.id} className="space-y-3">
                  <TaskNode task={root} allTasks={tasks} depth={0} />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Knight reasoning stream (Col: 5) */}
        <div className="lg:col-span-5 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col min-h-[400px]">
          <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-yellow-500 flex items-center gap-2">
              <Award className="w-4 h-4 text-yellow-500" /> Knight-0 Strategic Reasoning
            </h3>
            <span className="text-xxs font-mono bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 px-2 py-0.5 rounded">
              Cognition Stream
            </span>
          </div>

          <div className="flex-1 bg-black/40 border border-white/5 rounded-xl p-4 font-mono text-xs overflow-y-auto max-h-[420px] scrollbar-thin space-y-3">
            {knightLogs.length === 0 ? (
              <div className="h-full flex items-center justify-center text-slate-600 text-center">
                Waiting for Knight strategic logs...
              </div>
            ) : (
              knightLogs.map((log, idx) => (
                <div key={idx} className="border-l-2 border-yellow-500/30 pl-3 py-1 space-y-1 bg-white/[0.01] rounded-r">
                  <div className="flex items-center justify-between text-xxs text-yellow-500/70">
                    <span className="font-semibold flex items-center gap-1">
                      <Zap className="w-3 h-3" /> {log.sender}
                    </span>
                    <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <p className="text-slate-300 leading-relaxed break-words">{log.message}</p>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

// Recursive task renderer with clean dependency nesting and glow colors
interface TaskNodeProps {
  task: any;
  allTasks: any[];
  depth: number;
}

function TaskNode({ task, allTasks, depth }: TaskNodeProps) {
  // Find child tasks that depend on this task
  const children = allTasks.filter(t => t.dependencies && t.dependencies.includes(task.id));

  const statusColors = {
    PENDING: 'border-slate-500/20 bg-slate-500/5 text-slate-400 shadow-slate-500/5',
    RUNNING: 'border-yellow-500/40 bg-yellow-500/5 text-yellow-400 shadow-yellow-500/20 pulse-glow',
    COMPLETED: 'border-emerald-500/40 bg-emerald-500/5 text-emerald-400 shadow-emerald-500/10',
    FAILED: 'border-red-500/40 bg-red-500/5 text-red-400 shadow-red-500/20 animate-pulse',
  };

  return (
    <div className="space-y-3">
      <div 
        style={{ marginLeft: `${depth * 24}px` }} 
        className={`relative flex items-center gap-4 p-4 border rounded-xl shadow-lg transition duration-300 hover:bg-white/[0.02] ${statusColors[task.status as keyof typeof statusColors] || statusColors.PENDING}`}
      >
        {/* Glow connector bar for nested visual tree layout */}
        {depth > 0 && (
          <div 
            style={{ left: `-${16}px`, width: `${16}px` }} 
            className="absolute top-1/2 -translate-y-1/2 h-[2px] bg-cyan-500/20 -z-10"
          />
        )}

        <div className="flex-1 space-y-1">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xxs font-semibold opacity-60 tracking-wider">
              {task.id} • {task.assigned_house}
            </span>
            <span className="font-mono text-xxs font-bold uppercase tracking-widest px-2 py-0.5 rounded bg-white/5 border border-white/5">
              {task.status}
            </span>
          </div>
          <h4 className="font-semibold text-sm tracking-wide text-slate-200 font-sans">{task.title}</h4>
          
          {task.output_data && Object.keys(task.output_data).length > 0 && (
            <details className="mt-2 text-xxs font-mono text-slate-400 bg-black/30 rounded-lg p-2 border border-white/5 cursor-pointer">
              <summary className="font-semibold hover:text-white transition">Output Payload</summary>
              <pre className="mt-1 overflow-x-auto max-w-full text-slate-300 leading-normal select-text">
                {JSON.stringify(task.output_data, null, 2)}
              </pre>
            </details>
          )}
        </div>
      </div>

      {children.map(child => (
        <TaskNode key={child.id} task={child} allTasks={allTasks} depth={depth + 1} />
      ))}
    </div>
  );
}
