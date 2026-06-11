import React, { useState, useEffect } from 'react';

export default function LineageVisualizer() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/agents/persistent')
      .then(res => res.json())
      .then(data => {
        setAgents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch persistent agents:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="bg-gray-900 border border-green-500/30 p-6 rounded-lg text-white shadow-xl mt-8">
      <h2 className="text-2xl font-bold mb-4 text-green-400">🧬 Agent Lineage & Persistence Matrix</h2>
      <p className="text-sm text-gray-400 mb-6">
        Living, breathing autonomous entities that survive runtime termination.
      </p>

      {loading ? (
        <div className="text-center py-10">
          <div className="animate-spin h-8 w-8 border-t-2 border-green-500 rounded-full mx-auto"></div>
          <p className="mt-4 text-gray-500">Querying SQL Genome Matrix...</p>
        </div>
      ) : agents.length === 0 ? (
        <div className="text-center py-10 text-gray-600">
          No persistent agents discovered in the matrix.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div key={agent.id} className="bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-green-500/50 transition-colors">
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-semibold text-white">{agent.name}</h3>
                <span className={`text-xs px-2 py-1 rounded ${agent.status === 'ALIVE' ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400'}`}>
                  {agent.status}
                </span>
              </div>
              <div className="text-sm text-gray-400 mb-4">House: <span className="text-gray-200">{agent.house}</span></div>
              
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-500">Level:</span>
                  <span className="text-green-300">{agent.current_level}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">EXP:</span>
                  <span className="text-yellow-300">{agent.experience_points.toFixed(1)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Reliability:</span>
                  <span className="text-blue-300">{(agent.reliability_score * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Specialization:</span>
                  <span className="text-purple-300">{agent.specialization || "Generalist"}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
