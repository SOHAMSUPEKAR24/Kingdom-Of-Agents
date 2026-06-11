import React, { useEffect, useState } from 'react';
import { Terminal, FileCode, CheckCircle, XCircle, Clock, Zap, Activity } from 'lucide-react';
import { api } from '../utils/api';

interface MissionOutput {
  task_id: string;
  title: string;
  status: string;
  assigned_soldier: string | null;
  trace?: {
    status: string;
    stdout: string;
    time_ms: number;
    llm_bypassed?: boolean;
    model_calls?: number;
  };
  artifact?: {
    file: string;
    type: string;
    capability?: string;
  };
}

interface ActivityReport {
  hypotheses_generated: number;
  experiments_run: number;
  doctrines_created: number;
  specialist_promotions: number;
  model_calls_avoided?: number;
  status: string;
}

export default function MissionOutputCenter() {
  const [outputs, setOutputs] = useState<MissionOutput[]>([]);
  const [activity, setActivity] = useState<ActivityReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [outRes, actRes] = await Promise.all([
          api.getMissionOutputs(),
          api.getActivityReport()
        ]);
        setOutputs(outRes);
        setActivity(actRes);
      } catch (err) {
        console.error('Failed to fetch mission data', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 20000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-white/10 pb-4">
        <h2 className="text-2xl font-orbitron font-bold text-slate-100 flex items-center gap-3">
          <Terminal className="w-6 h-6 text-emerald-400" />
          Mission Output Center
        </h2>
        <div className="flex gap-4">
          <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono rounded-full flex items-center gap-2">
            <Zap className="w-3 h-3" /> HEARTBEAT: {activity?.status || 'UNKNOWN'}
          </span>
        </div>
      </div>

      {/* Activity Report Banner */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {[
          { label: "Hypotheses Generated", value: activity?.hypotheses_generated || 0, color: "text-blue-400" },
          { label: "Experiments Run", value: activity?.experiments_run || 0, color: "text-purple-400" },
          { label: "Doctrines Extracted", value: activity?.doctrines_created || 0, color: "text-emerald-400" },
          { label: "Specialists Promoted", value: activity?.specialist_promotions || 0, color: "text-amber-400" },
          { label: "Model Calls Avoided", value: activity?.model_calls_avoided || 0, color: "text-rose-400" }
        ].map((stat, i) => (
          <div key={i} className="bg-white/5 border border-white/10 rounded-xl p-4 flex flex-col justify-center items-center">
            <span className="text-xs text-slate-400 uppercase font-mono tracking-wider text-center">{stat.label}</span>
            <span className={`text-2xl font-bold font-orbitron mt-2 ${stat.color}`}>{stat.value}</span>
          </div>
        ))}
      </div>

      <div className="bg-[#0a0a0f] border border-white/10 rounded-2xl shadow-xl overflow-hidden">
        <div className="p-4 border-b border-white/10 bg-white/5">
          <h3 className="text-lg font-bold text-slate-200 flex items-center gap-2">
            <Activity className="w-5 h-5 text-slate-400" /> Comprehensive Execution Streams
          </h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-400">
            <thead className="text-xs text-slate-500 uppercase bg-black/40">
              <tr>
                <th className="px-6 py-4">Task / Objective</th>
                <th className="px-6 py-4">Specialist</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Execution Trace</th>
                <th className="px-6 py-4">Artifact Generated</th>
              </tr>
            </thead>
            <tbody>
              {loading && outputs.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500 font-mono animate-pulse">
                    Connecting to central civilization streams...
                  </td>
                </tr>
              )}
              {outputs.length === 0 && !loading && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500 font-mono">
                    No recent mission outputs. Awaiting heartbeat ticks.
                  </td>
                </tr>
              )}
              {outputs.map((out) => (
                <tr key={out.task_id} className="border-b border-white/5 bg-white/5 hover:bg-white/10 transition-colors">
                  <td className="px-6 py-4">
                    <div className="font-bold text-slate-300">{out.title || out.task_id}</div>
                    <div className="text-[10px] font-mono text-slate-500 mt-1">{out.task_id}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded font-mono text-xs">
                      {out.assigned_soldier || 'Unassigned'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {out.status === 'SUCCESS' ? (
                      <span className="flex items-center gap-2 text-emerald-400 text-xs font-bold"><CheckCircle className="w-4 h-4"/> SUCCESS</span>
                    ) : out.status === 'FAILED' ? (
                      <span className="flex items-center gap-2 text-red-400 text-xs font-bold"><XCircle className="w-4 h-4"/> FAILED</span>
                    ) : (
                      <span className="flex items-center gap-2 text-amber-400 text-xs font-bold"><Clock className="w-4 h-4"/> {out.status}</span>
                    )}
                  </td>
                  <td className="px-6 py-4 max-w-xs">
                    {out.trace ? (
                      <div className="bg-black/50 p-2 rounded border border-white/5">
                        <div className="text-[10px] text-emerald-500 font-mono flex items-center justify-between mb-1">
                          <span>{out.trace.time_ms.toFixed(0)}ms</span>
                          {out.trace.llm_bypassed && (
                            <span className="px-1 bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded">BYPASSED</span>
                          )}
                          <span>{out.trace.status}</span>
                        </div>
                        <pre className="text-[10px] text-slate-400 whitespace-pre-wrap overflow-hidden h-12">
                          {out.trace.stdout || 'No output.'}
                        </pre>
                      </div>
                    ) : (
                      <span className="text-slate-600 italic text-xs">No trace recorded.</span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    {out.artifact ? (
                      <div className="flex items-center gap-2 bg-blue-500/10 p-2 rounded border border-blue-500/20">
                        <FileCode className="w-4 h-4 text-blue-400" />
                        <div>
                          <div className="text-xs text-blue-300 font-mono truncate max-w-[150px]">{out.artifact.file.split('/').pop()}</div>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-[10px] text-blue-500/60 uppercase">{out.artifact.type}</span>
                            {out.artifact.capability && out.artifact.capability !== "UNKNOWN" && (
                              <span className="text-[10px] bg-indigo-500/20 text-indigo-300 px-1 rounded uppercase">{out.artifact.capability}</span>
                            )}
                          </div>
                        </div>
                      </div>
                    ) : (
                      <span className="text-slate-600 italic text-xs">No artifacts.</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
