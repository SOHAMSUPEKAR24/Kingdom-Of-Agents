'use client';

import React, { useState, useEffect } from 'react';

import { api } from '../utils/api';

export default function ExpertiseEvolutionCenter() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    let isMounted = true;
    
    const fetchMetrics = async () => {
      try {
        const data = await api.getExpertiseEvolution();
        if (isMounted) setMetrics(data);
      } catch (err) {
        console.error("Failed to fetch expertise evolution metrics:", err);
      }
    };
    
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 20000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  if (!metrics) {
    return <div className="p-4 text-white">Loading Expertise Metrics...</div>;
  }

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 text-white font-mono mt-6 shadow-xl">
      <h2 className="text-xl font-bold text-blue-400 mb-4 tracking-wider flex items-center">
        <span className="mr-2">📈</span> EXPERTISE EVOLUTION CENTER
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Skill Scores */}
        <div className="bg-gray-800 p-4 rounded border border-gray-700">
          <h3 className="text-sm text-gray-400 mb-3 border-b border-gray-700 pb-2">DOMAIN PROFICIENCY (0-100)</h3>
          <ul className="space-y-3">
            {Object.entries(metrics.skillScores).map(([skill, score]: any) => (
              <li key={skill}>
                <div className="flex justify-between mb-1 text-sm">
                  <span className="font-semibold">{skill}</span>
                  <span className={score > 90 ? "text-green-400" : score > 80 ? "text-yellow-400" : "text-red-400"}>
                    {score.toFixed(1)}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${score}%` }}></div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Tool Mastery */}
        <div className="bg-gray-800 p-4 rounded border border-gray-700">
          <h3 className="text-sm text-gray-400 mb-3 border-b border-gray-700 pb-2">TOOL MASTERY METRICS</h3>
          <ul className="space-y-2">
            {Object.entries(metrics.tools).map(([tool, data]: any) => (
              <li key={tool} className="flex justify-between items-center text-sm bg-gray-900 p-2 rounded">
                <span className="font-semibold text-gray-300">{tool}</span>
                <span className="text-gray-400 text-xs text-right">
                  <span className="text-green-400 block">{data.successRate.toFixed(1)}% Success</span>
                  <span className="block">{data.runs} Executions</span>
                </span>
              </li>
            ))}
          </ul>
        </div>

        {/* Global Learning Stats */}
        <div className="bg-gray-800 p-4 rounded border border-gray-700 md:col-span-2 flex justify-between items-center text-sm">
           <div className="text-center">
             <div className="text-2xl text-purple-400 font-bold">{metrics.doctrinesDistilled}</div>
             <div className="text-gray-500 uppercase text-xs mt-1">Doctrines Distilled</div>
           </div>
           <div className="text-center">
             <div className="text-2xl text-green-400 font-bold">{metrics.benchmarksPassed}</div>
             <div className="text-gray-500 uppercase text-xs mt-1">Benchmarks Passed</div>
           </div>
           <div className="text-center">
             <div className="text-2xl text-yellow-400 font-bold">{metrics.activeSandboxes}</div>
             <div className="text-gray-500 uppercase text-xs mt-1">Active Cyber Labs</div>
           </div>
        </div>
      </div>
    </div>
  );
}
