"use client";

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCpu, FiGlobe, FiDatabase, FiTrendingUp } from 'react-icons/fi';

export default function ExecutiveThroneRoomV2() {
  const [ascensionMetrics, setAscensionMetrics] = useState<any[]>([]);
  const [experienceVectors, setExperienceVectors] = useState<any[]>([]);
  const [worldInteractions, setWorldInteractions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ascRes, expRes, intRes] = await Promise.all([
          fetch('http://localhost:8000/api/v1/knight/ascension'),
          fetch('http://localhost:8000/api/v1/experience/vectors'),
          fetch('http://localhost:8000/api/v1/experience/interactions')
        ]);
        
        if (ascRes.ok) setAscensionMetrics(await ascRes.json());
        if (expRes.ok) setExperienceVectors(await expRes.json());
        if (intRes.ok) setWorldInteractions(await intRes.json());
      } catch (err) {
        console.error("Failed to fetch Executive Throne Room data", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 20000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full bg-[#030712] rounded-xl border border-gray-800 shadow-2xl overflow-hidden p-6 text-gray-200">
      <div className="flex items-center space-x-3 mb-6 pb-4 border-b border-gray-800">
        <FiCpu className="text-4xl text-fuchsia-500" />
        <div>
          <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-400 to-indigo-500">
            Knight-0 Sovereign Cognition & Ascension
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            Real-time telemetry of experience distillation, real-world execution, and autonomous intelligence evolution.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-24 bg-gray-800 rounded"></div>
          <div className="h-64 bg-gray-800 rounded"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Ascension Metrics */}
          <div className="col-span-1 bg-[#0a0f1c] p-5 rounded-lg border border-gray-800">
            <h3 className="text-xl font-semibold text-indigo-400 mb-4 flex items-center">
              <FiTrendingUp className="mr-2" /> Current Ascension Level
            </h3>
            {ascensionMetrics.length > 0 ? (
              <div className="space-y-4">
                <div className="p-4 bg-gray-900 rounded border border-gray-700">
                  <p className="text-sm text-gray-400">Reasoning Depth</p>
                  <p className="text-3xl font-bold text-fuchsia-400">{ascensionMetrics[0].reasoning_depth.toFixed(3)}</p>
                </div>
                <div className="p-4 bg-gray-900 rounded border border-gray-700">
                  <p className="text-sm text-gray-400">World Model Accuracy</p>
                  <p className="text-3xl font-bold text-emerald-400">{(ascensionMetrics[0].world_model_accuracy * 100).toFixed(1)}%</p>
                </div>
                <div className="p-4 bg-gray-900 rounded border border-gray-700">
                  <p className="text-sm text-gray-400">Strategic Foresight</p>
                  <p className="text-3xl font-bold text-blue-400">{ascensionMetrics[0].strategic_foresight.toFixed(3)}</p>
                </div>
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No ascension metrics recorded yet.</p>
            )}
          </div>

          {/* World Interactions */}
          <div className="col-span-1 lg:col-span-2 bg-[#0a0f1c] p-5 rounded-lg border border-gray-800">
            <h3 className="text-xl font-semibold text-emerald-400 mb-4 flex items-center">
              <FiGlobe className="mr-2" /> Recent World Interactions
            </h3>
            <div className="h-64 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent">
              <AnimatePresence>
                {worldInteractions.map((log) => (
                  <motion.div
                    key={log.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`p-3 rounded border text-sm flex flex-col ${log.success ? 'bg-emerald-900/20 border-emerald-500/30' : 'bg-red-900/20 border-red-500/30'}`}
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold">{log.interaction_type} | {log.agent_id}</span>
                      <span className={log.success ? 'text-emerald-400' : 'text-red-400'}>
                        {log.success ? 'SUCCESS' : 'FAILED'}
                      </span>
                    </div>
                    <span className="text-gray-400 text-xs font-mono break-all">{log.target}</span>
                    {log.outcome_summary && (
                      <span className="text-gray-300 mt-2 p-2 bg-black/30 rounded font-mono text-xs max-h-20 overflow-y-auto">
                        {log.outcome_summary.substring(0, 150)}{log.outcome_summary.length > 150 ? '...' : ''}
                      </span>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </div>

          {/* Experience Vectors */}
          <div className="col-span-1 lg:col-span-3 bg-[#0a0f1c] p-5 rounded-lg border border-gray-800">
            <h3 className="text-xl font-semibold text-blue-400 mb-4 flex items-center">
              <FiDatabase className="mr-2" /> Distilled Experience Memory (Hot)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {experienceVectors.slice(0, 6).map((vec) => (
                <div key={vec.id} className="p-4 bg-gray-900 rounded border border-gray-700 hover:border-blue-500/50 transition-colors">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-mono text-gray-500">{vec.id}</span>
                    <span className="px-2 py-1 bg-blue-900/50 text-blue-300 rounded text-xs">
                      Weight: {vec.strategic_weight.toFixed(1)}
                    </span>
                  </div>
                  <p className="text-sm font-semibold mb-2">Agent: {vec.agent_id}</p>
                  <div className="space-y-1">
                    {vec.extracted_lessons.map((lesson: string, idx: number) => (
                      <p key={idx} className="text-xs text-gray-400 flex items-start">
                        <span className="mr-2">•</span> {lesson}
                      </p>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
