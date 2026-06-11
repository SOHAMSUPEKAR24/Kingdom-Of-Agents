'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { Search, Database, HardDrive, RefreshCw, Zap } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function MemoryCrypt() {
  const [query, setQuery] = useState('');
  const { memories, fetchMemories, loading } = useKingdomStore();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchMemories(query);
  };

  const handleClear = () => {
    setQuery('');
    fetchMemories();
  };

  // Generate Recharts data for the Relevance Time-Decay curve
  // W = CosineSimilarity * e^(-lambda * dt)
  const decayData = useMemo(() => {
    const data = [];
    const lambda = 0.05; // Decay rate
    for (let dt = 0; dt <= 48; dt += 4) {
      const wHigh = parseFloat((1.0 * Math.exp(-lambda * dt)).toFixed(2));
      const wMed = parseFloat((0.7 * Math.exp(-lambda * dt)).toFixed(2));
      data.push({
        hour: `${dt}h`,
        'High Relevance (1.0)': wHigh,
        'Medium Relevance (0.7)': wMed,
      });
    }
    return data;
  }, []);

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="relative overflow-hidden backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl">
        <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl -z-10" />
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center">
              <span className="text-xl">🪦</span>
            </div>
            <div>
              <h2 className="font-orbitron text-xl font-bold tracking-wider text-purple-400">Shared Memory Crypt</h2>
              <p className="text-xs text-slate-400">Semantic vector storage and wisdom compression index</p>
            </div>
          </div>

          <form onSubmit={handleSearch} className="flex gap-2 w-full md:w-96">
            <div className="relative flex-1">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search semantic relationships..."
                className="w-full bg-black/40 border border-white/10 focus:border-purple-500/50 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-purple-500/20 font-mono transition"
              />
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-purple-500/10 border border-purple-500/30 hover:bg-purple-500/20 text-purple-400 px-4 py-2.5 rounded-xl text-xs font-orbitron tracking-wider transition cursor-pointer"
            >
              Query
            </button>
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="bg-white/5 border border-white/10 hover:bg-white/10 text-slate-400 px-3 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer"
              >
                Clear
              </button>
            )}
          </form>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Memories Directory (Col: 7) */}
        <div className="lg:col-span-7 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col min-h-[450px]">
          <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-300 flex items-center gap-2">
              <Database className="w-4 h-4 text-purple-400" /> Relational Memory Elements
            </h3>
            <span className="text-xxs font-mono bg-purple-500/10 text-purple-400 border border-purple-500/20 px-2 py-0.5 rounded">
              {memories.length} Records Loaded
            </span>
          </div>

          {memories.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
              <span className="text-3xl opacity-40 mb-3">🗄️</span>
              <p className="text-slate-400 text-sm font-mono">No stored memory elements found.</p>
              <p className="text-slate-600 text-xs font-mono mt-1">Submit an objective to generate experiential memory elements.</p>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto space-y-4 max-h-[460px] pr-2 scrollbar-thin">
              {memories.map((mem) => {
                // Determine memory badge colors
                const typeColors = {
                  EXPERIENCE: 'border-cyan-500/20 bg-cyan-500/5 text-cyan-400',
                  FAILURE: 'border-red-500/20 bg-red-500/5 text-red-400',
                  STRATEGY: 'border-yellow-500/20 bg-yellow-500/5 text-yellow-400',
                  INFRASTRUCTURE: 'border-purple-500/20 bg-purple-500/5 text-purple-400',
                };
                const badgeStyle = typeColors[mem.memory_type as keyof typeof typeColors] || 'border-white/5 bg-white/5 text-slate-300';
                
                // Parse compression ratio
                const originalSize = mem.compression_ratio?.original || mem.raw_content.length;
                const compressedSize = mem.compression_ratio?.compressed || mem.compressed_content?.length || originalSize;
                const savingsPct = originalSize > 0 
                  ? Math.max(0, Math.floor((1 - (compressedSize / originalSize)) * 100))
                  : 0;

                return (
                  <div key={mem.id} className="p-4 border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] rounded-xl space-y-2 transition duration-200">
                    <div className="flex items-center justify-between text-xxs font-mono">
                      <span className="font-semibold text-slate-500">{mem.id}</span>
                      <span className={`px-2 py-0.5 rounded font-bold ${badgeStyle}`}>{mem.memory_type}</span>
                    </div>

                    <h4 className="font-bold text-sm text-slate-200 tracking-wide">{mem.title}</h4>
                    
                    <p className="text-slate-400 text-xs font-sans leading-relaxed">{mem.raw_content}</p>

                    {mem.compressed_content && (
                      <div className="mt-3 bg-black/30 border border-white/5 p-3 rounded-lg space-y-2">
                        <div className="flex items-center justify-between text-xxs font-mono text-slate-500">
                          <span className="flex items-center gap-1"><HardDrive className="w-3.5 h-3.5" /> Compressed Wisdom</span>
                          <span className="text-purple-400 font-bold">-{savingsPct}% Compression</span>
                        </div>
                        <p className="text-slate-300 text-xs italic font-sans">“ {mem.compressed_content} ”</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Relevance Time-Decay curve (Col: 5) */}
        <div className="lg:col-span-5 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col justify-between min-h-[450px]">
          <div className="border-b border-white/5 pb-3 mb-4">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-purple-400 flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-purple-400" /> Relevance Time-Decay Curve
            </h3>
            <p className="text-xxs text-slate-400 font-mono">Visualization of exponential utility relevance decay over elapsed hours</p>
          </div>

          <div className="flex-1 w-full min-h-[220px] bg-black/40 border border-white/5 rounded-xl p-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={decayData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                <XAxis dataKey="hour" stroke="#94a3b8" fontSize={9} tickLine={false} />
                <YAxis stroke="#94a3b8" fontSize={9} tickLine={false} domain={[0, 1]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0a0a14', borderColor: '#8b5cf6', color: '#fff', fontSize: 10, fontFamily: 'monospace' }}
                  labelStyle={{ fontWeight: 'bold', color: '#8b5cf6' }}
                />
                <Line type="monotone" dataKey="High Relevance (1.0)" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="Medium Relevance (0.7)" stroke="#00f2fe" strokeWidth={1.5} dot={false} strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-4 bg-purple-500/5 border border-purple-500/10 p-3 rounded-lg space-y-2">
            <div className="flex items-center gap-1.5 text-purple-400 font-mono text-xxs font-bold uppercase tracking-wider">
              <Zap className="w-3.5 h-3.5" /> Adaptive Memory Decay
            </div>
            <p className="text-slate-400 text-xxs leading-relaxed font-mono">
              Memories decay in relevance cosine similarity factor based on exponential elapsed time intervals, unless refreshed by swarms retrieval hits which boost retrieval coefficient weights.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
