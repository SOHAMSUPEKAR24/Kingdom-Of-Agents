'use client';

import { useState, useEffect } from 'react';
import { api } from '../utils/api';

// Domain models
interface Objective {
  id: string;
  title: string;
  description: string;
  priority_score: number;
  status: string;
  origin_source: string;
  created_at: string;
}

interface Gap {
  id: string;
  domain: string;
  identified_weakness: string;
  severity_score: number;
  created_at: string;
}

interface Roadmap {
  id: string;
  phase_name: string;
  objectives: string[];
  status: string;
  created_at: string;
}

interface Dynasty {
  id: string;
  dynasty_name: string;
  domain: string;
  current_generation: number;
  inherited_doctrines: string[];
  created_at: string;
}

export default function SovereignStrategicThroneRoom() {
  const [objectives, setObjectives] = useState<Objective[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [roadmaps, setRoadmaps] = useState<Roadmap[]>([]);
  const [dynasties, setDynasties] = useState<Dynasty[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSovereignData = async () => {
      try {
        const [objRes, gapRes, rmRes, dynRes] = await Promise.all([
          api.getSovereignObjectives().catch(() => []),
          api.getCapabilityGaps().catch(() => []),
          api.getCivilizationRoadmaps().catch(() => []),
          api.getSpecialistDynasties().catch(() => []),
        ]);

        setObjectives(objRes);
        setGaps(gapRes);
        setRoadmaps(rmRes);
        setDynasties(dynRes);
      } catch (err) {
        console.error("Failed to fetch sovereign data", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSovereignData();
    const interval = setInterval(fetchSovereignData, 20000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="text-center p-12 text-white">Loading Sovereign Architecture...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white uppercase tracking-wider flex items-center gap-3">
          <span className="text-blue-500">👑</span> Sovereign Strategic Throne Room
        </h2>
        <div className="flex gap-2 text-sm text-gray-400">
          <span className="bg-gray-800/50 px-3 py-1 rounded-full border border-gray-700">Evolution Active</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-bold text-white mb-2">Autonomous Objectives</h3>
          <p className="text-3xl font-mono text-purple-400">{objectives.length}</p>
        </div>
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-bold text-white mb-2">Identified Gaps</h3>
          <p className="text-3xl font-mono text-red-400">{gaps.length}</p>
        </div>
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-bold text-white mb-2">Roadmap Phases</h3>
          <p className="text-3xl font-mono text-emerald-400">{roadmaps.length}</p>
        </div>
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-bold text-white mb-2">Specialist Dynasties</h3>
          <p className="text-3xl font-mono text-orange-400">{dynasties.length}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden flex flex-col">
          <div className="bg-gray-900 px-4 py-3 border-b border-gray-700">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-purple-400">🎯</span> Active Objectives
            </h3>
          </div>
          <div className="p-4 space-y-4 flex-1 overflow-y-auto max-h-[400px]">
            {objectives.length === 0 ? (
              <p className="text-gray-500 italic text-sm">No objectives detected.</p>
            ) : (
              objectives.map((obj) => (
                <div key={obj.id} className="bg-gray-900 rounded p-3 border border-gray-700">
                  <div className="flex justify-between items-start mb-1">
                    <span className="text-sm font-bold text-white">{obj.title}</span>
                    <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded uppercase">{obj.status}</span>
                  </div>
                  <p className="text-xs text-gray-400 mb-2">{obj.description}</p>
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Priority: {obj.priority_score.toFixed(2)}</span>
                    <span>Source: {obj.origin_source}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden flex flex-col">
          <div className="bg-gray-900 px-4 py-3 border-b border-gray-700">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="text-red-400">⚠️</span> Capability Gaps
            </h3>
          </div>
          <div className="p-4 space-y-4 flex-1 overflow-y-auto max-h-[400px]">
            {gaps.length === 0 ? (
              <p className="text-gray-500 italic text-sm">No capability gaps identified.</p>
            ) : (
              gaps.map((gap) => (
                <div key={gap.id} className="bg-gray-900 rounded p-3 border border-gray-700">
                  <div className="flex justify-between items-start mb-1">
                    <span className="text-sm font-bold text-white">{gap.domain}</span>
                    <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">Severity: {gap.severity_score}</span>
                  </div>
                  <p className="text-xs text-gray-400">{gap.identified_weakness}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
