import React, { useState, useEffect } from 'react';

export default function ExecutiveCommandCenter() {
  const [responses, setResponses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/executive/responses')
      .then(res => res.json())
      .then(data => {
        setResponses(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch executive responses:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="bg-gray-900 border border-purple-500/30 p-6 rounded-lg text-white shadow-xl">
      <h2 className="text-2xl font-bold mb-4 text-purple-400">👑 Executive Command Center</h2>
      <p className="text-sm text-gray-400 mb-6">
        Synthesized final intelligence, stripped of telemetry noise. Designed for the King.
      </p>

      {loading ? (
        <div className="text-center py-10">
          <div className="animate-spin h-8 w-8 border-t-2 border-purple-500 rounded-full mx-auto"></div>
          <p className="mt-4 text-gray-500">Awaiting Executive Synthesis...</p>
        </div>
      ) : responses.length === 0 ? (
        <div className="text-center py-10 text-gray-600">
          No executive responses have been generated yet.
        </div>
      ) : (
        <div className="space-y-8">
          {responses.map((resp) => (
            <div key={resp.id} className="bg-gray-800 p-6 rounded-lg border border-gray-700 hover:border-purple-500/50 transition-colors">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-white">Objective: {resp.objective_id}</h3>
                <span className="bg-purple-900/50 text-purple-300 text-xs px-2 py-1 rounded">
                  Confidence: {(resp.confidence_score * 100).toFixed(1)}%
                </span>
              </div>
              
              <div className="mb-4">
                <h4 className="text-sm uppercase tracking-wider text-gray-400 mb-2">1. Input Objective</h4>
                <div className="bg-gray-900/50 p-3 rounded border border-gray-700 text-slate-300 font-mono text-sm">
                  {resp.objective_id}
                </div>
              </div>

              {resp.plan && resp.plan.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm uppercase tracking-wider text-cyan-400 mb-2">2. Execution Plan</h4>
                  <ul className="list-decimal list-inside space-y-1 text-cyan-200/80 text-sm font-mono bg-cyan-900/10 p-3 rounded border border-cyan-500/20">
                    {resp.plan.map((step: string, idx: number) => (
                      <li key={idx}>{step}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="mb-4">
                <h4 className="text-sm uppercase tracking-wider text-emerald-400 mb-2">3. Agents Used</h4>
                <div className="flex flex-wrap gap-2">
                  {resp.primary_specialists.map((spec: string, idx: number) => (
                    <span key={idx} className="bg-emerald-900/30 text-emerald-400 text-xs px-2 py-1 rounded border border-emerald-500/30">
                      {spec}
                    </span>
                  ))}
                  {resp.primary_specialists.length === 0 && <span className="text-gray-600 text-xs">None</span>}
                </div>
              </div>

              {resp.tools_used && resp.tools_used.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm uppercase tracking-wider text-orange-400 mb-2">4. Tools Used</h4>
                  <div className="flex flex-wrap gap-2">
                    {resp.tools_used.map((tool: string, idx: number) => (
                      <span key={idx} className="bg-orange-900/30 text-orange-400 text-xs px-2 py-1 rounded border border-orange-500/30">
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {resp.supporting_evidence && resp.supporting_evidence.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm uppercase tracking-wider text-blue-400 mb-2">5. Execution Logs</h4>
                  <div className="space-y-2 max-h-40 overflow-y-auto scrollbar-thin">
                    {resp.supporting_evidence.map((log: string, idx: number) => (
                      <div key={idx} className="bg-blue-900/10 p-2 rounded text-blue-200/80 text-xs font-mono whitespace-pre-wrap">
                        {log}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="mb-4">
                <h4 className="text-sm uppercase tracking-wider text-pink-400 mb-2">6. Artifacts Generated</h4>
                <ul className="list-disc list-inside text-pink-200/80 text-xs">
                  {resp.generated_artifacts.map((art: string, idx: number) => (
                    <li key={idx}>{art}</li>
                  ))}
                  {resp.generated_artifacts.length === 0 && <span className="text-gray-600">No artifacts generated.</span>}
                </ul>
              </div>

              <div className="mb-4">
                <h4 className="text-sm uppercase tracking-wider text-yellow-400 mb-2">7. Benchmarks</h4>
                <div className="flex gap-4">
                  <span className="bg-yellow-900/30 text-yellow-400 text-xs px-3 py-1.5 rounded border border-yellow-500/30 font-mono">
                    Score: {resp.benchmark_score ? (resp.benchmark_score * 100).toFixed(1) : 'N/A'}%
                  </span>
                  <span className="bg-purple-900/30 text-purple-400 text-xs px-3 py-1.5 rounded border border-purple-500/30 font-mono">
                    Confidence: {(resp.confidence_score * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-700">
                <h4 className="text-sm uppercase tracking-wider text-gray-400 mb-2">8. Final Output & Summary</h4>
                <div className="bg-gray-950 p-4 rounded border border-gray-800 whitespace-pre-wrap font-mono text-sm text-green-400 mb-4">
                  {resp.final_answer}
                </div>
                <p className="text-gray-400 text-sm leading-relaxed border-l-2 border-gray-600 pl-3">
                  {resp.executive_summary}
                </p>
                {resp.debate_summary && (
                  <p className="text-indigo-300/80 text-xs italic mt-3">
                    Debate Note: {resp.debate_summary}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
