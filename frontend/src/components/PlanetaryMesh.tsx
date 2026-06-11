'use client';

import React, { useState } from 'react';
import { useKingdomStore } from '../store/useKingdomStore';
import { 
  Network, Activity, Cpu, HardDrive, ShieldAlert, Globe, RefreshCw, Zap, 
  CheckCircle, AlertCircle, Server, Terminal, Flame, Shield, HelpCircle, Compass
} from 'lucide-react';

export default function PlanetaryMesh() {
  const { 
    cognitiveNodes, 
    memoryShards, 
    federatedGovernors, 
    civilizationState, 
    nervousReflexes,
    triggerRaftElection,
    scaleSwarmNode,
    triggerSimulatedAnomaly,
    loading
  } = useKingdomStore();

  const [scaleSpec, setScaleSpec] = useState<'STRATEGIC_REASONING' | 'WORLD_MODELING' | 'DOCTRINE_GENERATION' | 'TRUST_GOVERNANCE'>('WORLD_MODELING');
  const [chaosNodeId, setChaosNodeId] = useState('');
  const [chaosReason, setChaosReason] = useState('Critical buffer overflow in semantic shard partition');
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  // Setup default state in case backend isn't loaded yet
  const nodes = cognitiveNodes || [];
  const shards = memoryShards || [];
  const governors = federatedGovernors || [];
  const state = civilizationState || {
    total_compute_budget: 400.0,
    spent_compute_budget: 156.4,
    total_bandwidth_budget: 200.0,
    spent_bandwidth_budget: 48.2,
    synchronicity_index: 0.94,
    resilience_rating: 0.98,
    active_node_count: nodes.length || 4,
    last_global_sync: new Date().toISOString()
  };
  const reflexes = nervousReflexes || [];

  // Actions
  const handleElection = async () => {
    await triggerRaftElection();
  };

  const handleScale = async () => {
    await scaleSwarmNode(scaleSpec);
  };

  const handleChaos = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chaosNodeId) return;
    await triggerSimulatedAnomaly(chaosNodeId, chaosReason);
  };

  // Find leader governor
  const leaderGov = governors.find(g => g.raft_role === 'LEADER');
  const followerGovs = governors.filter(g => g.raft_role !== 'LEADER');

  // Node position mapping for topology SVG (Concentric Planetary Orbits)
  const width = 800;
  const height = 500;
  const centerX = width / 2;
  const centerY = height / 2;

  // Group nodes by specialization
  const groupedNodes = nodes.reduce((acc, node) => {
    const spec = node.specialization || 'UNKNOWN';
    if (!acc[spec]) acc[spec] = [];
    acc[spec].push(node);
    return acc;
  }, {} as Record<string, any[]>);

  const specializations = Object.keys(groupedNodes).sort();
  
  const nodePositions: Record<string, any> = {};
  const orbitRadii: Record<string, number> = {};
  const orbitColors = ['rgba(16, 185, 129, 0.3)', 'rgba(6, 182, 212, 0.3)', 'rgba(99, 102, 241, 0.3)', 'rgba(168, 85, 247, 0.3)', 'rgba(236, 72, 153, 0.3)'];

  specializations.forEach((spec, specIdx) => {
    const radius = 100 + specIdx * 70; // Inner orbit at 100, then +70 per orbit
    orbitRadii[spec] = radius;
    
    const specNodes = groupedNodes[spec];
    specNodes.forEach((node, nodeIdx) => {
      // Stagger initial angle per orbit for a more organic look
      const offset = (specIdx * Math.PI) / 4;
      const angle = offset + (nodeIdx * 2 * Math.PI) / (specNodes.length || 1) - Math.PI / 2;
      nodePositions[node.id] = {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        orbitIndex: specIdx,
        ...node
      };
    });
  });

  return (
    <div className="space-y-6">
      
      {/* 1. Global Civilization State Economics Terminal & Budget Gauges */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Economic Terminal */}
        <div className="lg:col-span-8 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl -z-10" />
          
          <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
                <Globe className="w-5 h-5 text-cyan-400" />
              </div>
              <div>
                <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-200">
                  Planetary Civilization Mesh Index
                </h3>
                <p className="text-xxs text-slate-400 font-mono">Consolidated telemetry & resource budgets</p>
              </div>
            </div>
            <div className="text-right font-mono">
              <span className="text-xxs text-slate-500 block">LAST GLOBAL SYNC</span>
              <span className="text-xs text-cyan-400 font-bold">
                {state.last_global_sync ? new Date(state.last_global_sync).toLocaleTimeString() : 'N/A'}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-2">
            <div className="bg-black/35 border border-white/5 rounded-xl p-4 text-center font-mono">
              <span className="text-slate-500 text-xxs block mb-1">SYNCHRONICITY</span>
              <span className="text-2xl font-bold text-cyan-400">
                {Math.round(state.synchronicity_index * 100)}%
              </span>
              <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-cyan-500 to-emerald-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${state.synchronicity_index * 100}%` }}
                />
              </div>
            </div>

            <div className="bg-black/35 border border-white/5 rounded-xl p-4 text-center font-mono">
              <span className="text-slate-500 text-xxs block mb-1">RESILIENCE RATING</span>
              <span className="text-2xl font-bold text-emerald-400">
                {Math.round(state.resilience_rating * 100)}%
              </span>
              <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-emerald-500 to-teal-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${state.resilience_rating * 100}%` }}
                />
              </div>
            </div>

            <div className="bg-black/35 border border-white/5 rounded-xl p-4 text-center font-mono">
              <span className="text-slate-500 text-xxs block mb-1">ACTIVE NODES</span>
              <span className="text-2xl font-bold text-indigo-400">
                {nodes.length} Nodes
              </span>
              <span className="text-xxs text-slate-500 block mt-1">Specialized Clusters</span>
            </div>

            <div className="bg-black/35 border border-white/5 rounded-xl p-4 text-center font-mono">
              <span className="text-slate-500 text-xxs block mb-1">MEMORY REPLICA</span>
              <span className="text-2xl font-bold text-purple-400">
                {shards.length} Shards
              </span>
              <span className="text-xxs text-slate-500 block mt-1">Strategically Placed</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 font-mono">
            {/* Compute budget */}
            <div className="bg-black/30 border border-white/5 rounded-xl p-4 flex flex-col justify-between">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xxs font-semibold text-slate-400 flex items-center gap-1.5">
                  <Cpu className="w-3.5 h-3.5 text-cyan-400" /> Compute Budget Spent
                </span>
                <span className="text-xxs text-slate-400 font-bold">
                  {state.spent_compute_budget.toFixed(1)} / {state.total_compute_budget.toFixed(1)} GFLOPS
                </span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mb-1">
                <div 
                  className="bg-cyan-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, (state.spent_compute_budget / state.total_compute_budget) * 100)}%` }}
                />
              </div>
              <span className="text-right text-[10px] text-slate-500">
                {Math.round((state.spent_compute_budget / state.total_compute_budget) * 100)}% Consumed
              </span>
            </div>

            {/* Bandwidth budget */}
            <div className="bg-black/30 border border-white/5 rounded-xl p-4 flex flex-col justify-between">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xxs font-semibold text-slate-400 flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5 text-purple-400" /> Bandwidth Band
                </span>
                <span className="text-xxs text-slate-400 font-bold">
                  {state.spent_bandwidth_budget.toFixed(1)} / {state.total_bandwidth_budget.toFixed(1)} MB/s
                </span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mb-1">
                <div 
                  className="bg-purple-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, (state.spent_bandwidth_budget / state.total_bandwidth_budget) * 100)}%` }}
                />
              </div>
              <span className="text-right text-[10px] text-slate-500">
                {Math.round((state.spent_bandwidth_budget / state.total_bandwidth_budget) * 100)}% Capacity Used
              </span>
            </div>
          </div>
        </div>

        {/* Autonomous Scaling Controller */}
        <div className="lg:col-span-4 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl -z-10" />
          
          <div>
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-200 flex items-center gap-2 mb-1">
              <Server className="w-4 h-4 text-indigo-400" /> Swarm Scaler
            </h3>
            <p className="text-xxs text-slate-400 font-mono mb-4 border-b border-white/5 pb-3">
              Deploy virtual cognitive resource instances
            </p>
            
            <div className="space-y-4">
              <div className="font-mono text-xs space-y-1.5">
                <label className="text-slate-400 block font-semibold">Specialization Specialty</label>
                <select
                  value={scaleSpec}
                  onChange={(e) => setScaleSpec(e.target.value as any)}
                  className="w-full bg-black/40 border border-white/10 text-slate-200 rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-indigo-500"
                >
                  <option value="STRATEGIC_REASONING">STRATEGIC_REASONING (Logic Swarm)</option>
                  <option value="WORLD_MODELING">WORLD_MODELING (Simulation Grid)</option>
                  <option value="DOCTRINE_GENERATION">DOCTRINE_GENERATION (Doctrine Hub)</option>
                  <option value="TRUST_GOVERNANCE">TRUST_GOVERNANCE (Compliance Guard)</option>
                </select>
              </div>
              
              <div className="bg-white/[0.02] border border-white/5 rounded-xl p-3 text-xxs font-mono text-slate-400 leading-normal">
                Scales virtual containerized agents with isolated CPU threads, dynamically routing task loads based on structural latency weights.
              </div>
            </div>
          </div>

          <button
            onClick={handleScale}
            disabled={loading}
            className="mt-6 w-full bg-indigo-500/10 border border-indigo-500/30 hover:bg-indigo-500/20 text-indigo-400 py-2.5 rounded-xl font-orbitron font-bold tracking-wider text-xs transition active:scale-[0.98] disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
          >
            <Zap className="w-3.5 h-3.5" /> Deploy Node Mesh
          </button>
        </div>
      </div>

      {/* 2. Planetary Swarm Topology Map (SVG Grid) & Live Node Details */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Interactive Topology Graph */}
        <div className="lg:col-span-8 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col justify-between min-h-[420px]">
          <div className="flex items-center justify-between border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-300 flex items-center gap-2">
              <Network className="w-4 h-4 text-cyan-400 animate-pulse" /> Planetary Swarm Topology
            </h3>
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">
              Live Mesh Connections
            </span>
          </div>

          <div className="flex-1 flex items-center justify-center py-4 relative">
            {nodes.length === 0 ? (
              <div className="text-center font-mono text-slate-500 text-xs">
                No active nodes found in swarm cluster state.
              </div>
            ) : (
              <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} className="w-full max-w-[800px] h-auto">
                {/* 1. Draw Concentric Orbit Rings */}
                {specializations.map((spec, specIdx) => (
                  <circle
                    key={`orbit-${spec}`}
                    cx={centerX}
                    cy={centerY}
                    r={orbitRadii[spec]}
                    fill="none"
                    stroke={orbitColors[specIdx % orbitColors.length]}
                    strokeWidth="1"
                    strokeDasharray="4 6"
                    className="animate-[spin_60s_linear_infinite]"
                    style={{ transformOrigin: `${centerX}px ${centerY}px` }}
                  />
                ))}

                {/* 2. Draw intra-orbit ring connections (instead of overlapping all-to-all) */}
                {specializations.map((spec) => {
                  const specNodes = groupedNodes[spec];
                  if (specNodes.length < 2) return null;
                  return specNodes.map((node, i) => {
                    const source = nodePositions[node.id];
                    const targetNode = specNodes[(i + 1) % specNodes.length];
                    const target = nodePositions[targetNode.id];
                    const isDegraded = source.status === 'FAILED' || target.status === 'FAILED';
                    
                    return (
                      <line
                        key={`ring-${source.id}-${target.id}`}
                        x1={source.x}
                        y1={source.y}
                        x2={target.x}
                        y2={target.y}
                        stroke={isDegraded ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255, 255, 255, 0.1)'}
                        strokeWidth="1.5"
                      />
                    );
                  });
                })}

                {/* 3. Central Core Sovereign Crown Node */}
                <circle 
                  cx={centerX} 
                  cy={centerY} 
                  r="24" 
                  fill="rgba(234, 179, 8, 0.05)" 
                  stroke="rgba(234, 179, 8, 0.4)" 
                  strokeWidth="2" 
                />
                <circle 
                  cx={centerX} 
                  cy={centerY} 
                  r="8" 
                  className="fill-yellow-500 animate-ping" 
                />
                <circle 
                  cx={centerX} 
                  cy={centerY} 
                  r="8" 
                  fill="#eab308" 
                />

                {/* 4. Connect nodes to central sovereign core */}
                {Object.keys(nodePositions).map((nodeId) => {
                  const node = nodePositions[nodeId];
                  const isFailed = node.status === 'FAILED';
                  return (
                    <line
                      key={`core-${nodeId}`}
                      x1={centerX}
                      y1={centerY}
                      x2={node.x}
                      y2={node.y}
                      stroke={isFailed ? 'rgba(239, 68, 68, 0.1)' : 'rgba(234, 179, 8, 0.15)'}
                      strokeWidth="1"
                      strokeDasharray="3 3"
                      className={isFailed ? '' : 'animate-dash'}
                      style={{ animation: 'dash 15s linear infinite' }}
                    />
                  );
                })}

                {/* 3. Draw active nodes */}
                {Object.keys(nodePositions).map((nodeId) => {
                  const node = nodePositions[nodeId];
                  const isSelected = selectedNodeId === node.id;
                  
                  let strokeColor = 'rgba(16, 185, 129, 0.5)'; // Active green
                  let fillColor = '#10b981';
                  if (node.status === 'DEGRADED') {
                    strokeColor = 'rgba(245, 158, 11, 0.5)';
                    fillColor = '#f59e0b';
                  } else if (node.status === 'FAILED') {
                    strokeColor = 'rgba(239, 68, 68, 0.5)';
                    fillColor = '#ef4444';
                  }

                  return (
                    <g 
                      key={node.id} 
                      className="cursor-pointer group"
                      onClick={() => {
                        setSelectedNodeId(isSelected ? null : node.id);
                        setChaosNodeId(node.id);
                      }}
                    >
                      {/* Pulse ring for active/degraded */}
                      {node.status !== 'FAILED' && (
                        <circle
                          cx={node.x}
                          cy={node.y}
                          r={isSelected ? "18" : "14"}
                          fill="none"
                          stroke={strokeColor}
                          strokeWidth="2"
                          className="animate-ping"
                          style={{ animationDuration: '3s' }}
                        />
                      )}
                      
                      <circle
                        cx={node.x}
                        cy={node.y}
                        r={isSelected ? "12" : "9"}
                        fill={fillColor}
                        stroke={isSelected ? '#ffffff' : 'rgba(0,0,0,0.6)'}
                        strokeWidth={isSelected ? '2' : '1.5'}
                        className="transition-all duration-300"
                      />
                      
                      {/* Node Label Text */}
                      <text
                        x={node.x}
                        y={node.y + 22}
                        textAnchor="middle"
                        fill="#f1f5f9"
                        fontSize="9"
                        fontWeight="bold"
                        className="font-mono bg-black/60 rounded select-none opacity-80 group-hover:opacity-100 transition"
                      >
                        {node.id.split('_').slice(-1)[0]}
                      </text>

                      {/* Small latency/status text */}
                      <text
                        x={node.x}
                        y={node.y - 16}
                        textAnchor="middle"
                        fill={node.status === 'FAILED' ? '#ef4444' : '#06b6d4'}
                        fontSize="8"
                        className="font-mono font-bold"
                      >
                        {node.status === 'FAILED' ? 'FAILED' : `${Math.round(node.latency_ms)}ms`}
                      </text>
                    </g>
                  );
                })}
              </svg>
            )}
          </div>
          
          <div className="border-t border-white/5 pt-3 flex items-center justify-between text-xxs font-mono text-slate-500">
            <span>ℹ Click any node to select it, inspect stats, or target for simulated failure tests.</span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" /> Active
              <span className="w-2 h-2 rounded-full bg-amber-500" /> Degraded
              <span className="w-2 h-2 rounded-full bg-red-500" /> Failed
            </span>
          </div>
        </div>

        {/* Selected Node Details OR System Overview */}
        <div className="lg:col-span-4 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col justify-between min-h-[420px]">
          <div className="border-b border-white/5 pb-3">
            <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-200">
              {selectedNodeId ? '🖥️ Node Inspector' : '📊 Swarm Mesh Metrics'}
            </h3>
            <p className="text-xxs text-slate-400 font-mono">
              {selectedNodeId ? `Details for ${selectedNodeId}` : 'Cluster network analysis stats'}
            </p>
          </div>

          <div className="flex-1 py-4 font-mono text-xs space-y-4">
            {selectedNodeId && nodePositions[selectedNodeId] ? (
              <>
                <div className="bg-black/30 border border-white/5 rounded-xl p-3.5 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-slate-500">NODE ID:</span>
                    <span className="font-bold text-slate-200">{selectedNodeId}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">SPECIALIZATION:</span>
                    <span className="font-bold text-cyan-400">{nodePositions[selectedNodeId].specialization}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">LATENCY:</span>
                    <span className="font-bold text-cyan-500">{nodePositions[selectedNodeId].latency_ms.toFixed(1)} ms</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">STATUS:</span>
                    <span className={`font-bold ${
                      nodePositions[selectedNodeId].status === 'ACTIVE' ? 'text-emerald-400' :
                      nodePositions[selectedNodeId].status === 'DEGRADED' ? 'text-amber-500' : 'text-red-500'
                    }`}>{nodePositions[selectedNodeId].status}</span>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-xxs mb-1">
                      <span className="text-slate-400">Node Compute Capacity</span>
                      <span className="text-slate-300 font-bold">{nodePositions[selectedNodeId].compute_budget}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-300 ${
                          nodePositions[selectedNodeId].status === 'FAILED' ? 'bg-red-500' : 'bg-emerald-400'
                        }`}
                        style={{ width: `${nodePositions[selectedNodeId].status === 'FAILED' ? 0 : nodePositions[selectedNodeId].compute_budget}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xxs mb-1">
                      <span className="text-slate-400">Node Bandwidth Cap</span>
                      <span className="text-slate-300 font-bold">{nodePositions[selectedNodeId].bandwidth_mb} MB/s</span>
                    </div>
                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-300 ${
                          nodePositions[selectedNodeId].status === 'FAILED' ? 'bg-red-500' : 'bg-indigo-400'
                        }`}
                        style={{ width: `${nodePositions[selectedNodeId].status === 'FAILED' ? 0 : (nodePositions[selectedNodeId].bandwidth_mb / 50) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="bg-red-500/5 border border-red-500/10 rounded-xl p-3 text-xxs text-red-400 leading-normal flex items-start gap-2">
                  <ShieldAlert className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                  <span>Simulating failure of this node triggers instant workload rebalancing and redirects memory shards onto surviving nodes.</span>
                </div>
              </>
            ) : (
              <div className="h-full flex flex-col justify-center items-center text-center p-4">
                <Compass className="w-12 h-12 text-slate-600 mb-3 animate-spin-slow" />
                <p className="text-slate-400 text-xs">No Node Selected</p>
                <p className="text-slate-600 text-xxs mt-1">
                  Click any colored node in the circular topology network graph to audit detailed active latency metrics, CPU thread scopes, and sharded storage bindings.
                </p>
              </div>
            )}
          </div>

          <div className="border-t border-white/5 pt-3">
            <button
              onClick={() => setSelectedNodeId(null)}
              disabled={!selectedNodeId}
              className="w-full bg-white/5 border border-white/10 hover:bg-white/10 text-slate-300 py-1.5 rounded-xl font-mono text-xxs transition disabled:opacity-50 cursor-pointer"
            >
              Clear Inspector Focus
            </button>
          </div>
        </div>

      </div>

      {/* 3. Federated Governor Network (RAFT Consensus Visualizer) & Distributed Memory Shards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Raft Governors network visualizer */}
        <div className="lg:col-span-5 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col justify-between min-h-[380px]">
          <div>
            <div className="flex items-center justify-between border-b border-white/5 pb-3 mb-4">
              <h3 className="font-orbitron text-md font-bold tracking-wider text-yellow-500 flex items-center gap-2">
                <Shield className="w-4 h-4 text-yellow-500" /> Federated RAFT Consensus
              </h3>
              <span className="text-xxs font-mono bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 px-2 py-0.5 rounded">
                Active Term {governors[0]?.current_term || 1}
              </span>
            </div>

            <div className="space-y-4">
              {/* Leader Node Card */}
              {leaderGov ? (
                <div className="bg-yellow-500/5 border border-yellow-500/25 rounded-2xl p-4 flex items-center justify-between shadow-[0_0_15px_rgba(234,179,8,0.08)]">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-yellow-500/10 border border-yellow-500/30 flex items-center justify-center text-xl shadow-[0_0_12px_rgba(234,179,8,0.2)]">
                      👑
                    </div>
                    <div className="font-mono">
                      <span className="text-xxs text-yellow-500 font-bold tracking-widest block">RAFT TERM LEADER</span>
                      <span className="text-sm font-bold text-slate-200 block truncate max-w-[160px]">
                        {leaderGov.id}
                      </span>
                    </div>
                  </div>
                  <div className="text-right font-mono">
                    <span className="text-xxs text-slate-500 block">VOTES CONSENT</span>
                    <span className="text-xs text-yellow-500 font-extrabold">{leaderGov.votes_received} (Unanimous)</span>
                  </div>
                </div>
              ) : (
                <div className="bg-red-500/5 border border-red-500/10 rounded-2xl p-4 text-center font-mono text-red-400 text-xs">
                  ⚠️ No Elected Leader! Consensus Partitioned.
                </div>
              )}

              {/* Followers List */}
              <div className="space-y-2.5 max-h-[160px] overflow-y-auto pr-1 scrollbar-thin">
                {followerGovs.length === 0 ? (
                  <p className="text-xxs font-mono text-slate-600 text-center py-4">No active followers connected.</p>
                ) : (
                  followerGovs.map(gov => (
                    <div key={gov.id} className="bg-black/30 border border-white/5 rounded-xl p-3 flex items-center justify-between font-mono text-xs">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${
                          gov.status === 'HEALTHY' ? 'bg-emerald-400 animate-pulse' :
                          gov.status === 'CONGESTED' ? 'bg-amber-500' : 'bg-red-500'
                        }`} />
                        <span className="text-slate-300 truncate max-w-[130px]">{gov.id}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-xxs text-slate-500 bg-white/5 border border-white/5 px-2 py-0.5 rounded">
                          {gov.raft_role}
                        </span>
                        <span className="text-slate-400 text-xxs font-semibold">
                          {gov.status}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <button
            onClick={handleElection}
            disabled={loading}
            className="mt-6 w-full bg-yellow-500/10 border border-yellow-500/30 hover:bg-yellow-500/20 text-yellow-500 py-2.5 rounded-xl font-orbitron font-bold tracking-wider text-xs transition active:scale-[0.98] disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Trigger Raft Election Cycle
          </button>
        </div>

        {/* Distributed memory shards grid */}
        <div className="lg:col-span-7 backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col justify-between min-h-[380px]">
          <div>
            <div className="flex items-center justify-between border-b border-white/5 pb-3 mb-4">
              <h3 className="font-orbitron text-md font-bold tracking-wider text-purple-400 flex items-center gap-2">
                <HardDrive className="w-4 h-4 text-purple-400" /> Memory Crypt Sharding
              </h3>
              <span className="text-xxs font-mono bg-purple-500/10 text-purple-400 border border-purple-500/20 px-2 py-0.5 rounded">
                Replicas Matrix
              </span>
            </div>

            {shards.length === 0 ? (
              <div className="flex flex-col items-center justify-center text-center p-8 py-12 font-mono text-slate-500">
                <HardDrive className="w-10 h-10 text-slate-700 mb-2" />
                <span className="text-xs">No active database sharded replicates.</span>
                <span className="text-xxs text-slate-600 mt-1">Issue an objective to spawn semantic memory shards automatically.</span>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-[220px] overflow-y-auto pr-1 scrollbar-thin">
                {shards.map(shard => {
                  const savings = Math.max(0, 1 - (shard.compressed_size_bytes / shard.original_size_bytes));
                  
                  return (
                    <div key={shard.id} className="bg-black/35 border border-white/5 rounded-xl p-3.5 font-mono text-xxs space-y-2 hover:border-purple-500/25 transition">
                      <div className="flex justify-between items-center">
                        <span className="font-bold text-slate-300">{shard.id.split('_').slice(-1)[0]}</span>
                        <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${
                          shard.status === 'HEALTHY' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                          shard.status === 'REPLICATING' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 animate-pulse' :
                          'bg-amber-500/10 text-amber-500 border border-amber-500/20'
                        }`}>
                          {shard.status}
                        </span>
                      </div>

                      <div className="space-y-1 text-slate-400">
                        <div className="flex justify-between">
                          <span>Shard Type:</span>
                          <span className="text-purple-400 font-bold">{shard.shard_type}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Host Host:</span>
                          <span className="text-slate-300 truncate max-w-[80px]">{shard.host_node_id}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Compression:</span>
                          <span className="text-emerald-400 font-semibold">-{Math.round(savings * 100)}% Savings</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Capacity:</span>
                          <span>{shard.compressed_size_bytes} / {shard.original_size_bytes} B</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="border-t border-white/5 pt-3 font-mono text-xxs text-slate-500">
            🔒 Mesh Memory Sharding replicates operating doctrine and strategic wisdom with cryptographic SHA-256 validation index anchors.
          </div>
        </div>

      </div>

      {/* 4. Self-Healing Diagnostics Console & Live Inject Chaos Module */}
      <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl space-y-6">
        
        <div className="flex items-center justify-between border-b border-white/5 pb-3">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-red-500/10 border border-red-500/30 flex items-center justify-center">
              <Terminal className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <h3 className="font-orbitron text-md font-bold tracking-wider text-slate-200">
                Self-Healing Infrastructure & Diagnostic Console
              </h3>
              <p className="text-xxs text-slate-400 font-mono">Observe automated quarantines & rebalancing, or inject simulated failures</p>
            </div>
          </div>
          <span className="text-xxs font-mono bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded">
            Chaos Reactor Engaged
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Active Reflexes scrolling console */}
          <div className="lg:col-span-7 flex flex-col justify-between min-h-[300px]">
            <span className="text-xxs font-mono text-slate-400 font-semibold uppercase tracking-wider block mb-2">
              Nervous System Reflex Telemetry Ticker
            </span>
            <div className="flex-1 bg-black/45 border border-white/5 rounded-xl p-4 font-mono text-xxs overflow-y-auto max-h-[240px] scrollbar-thin space-y-2">
              {reflexes.length === 0 ? (
                <div className="h-full flex items-center justify-center text-slate-600 text-center">
                  Waiting for distributed network events...
                </div>
              ) : (
                reflexes.map((ref) => (
                  <div 
                    key={ref.id} 
                    className={`border-l-2 pl-3 py-1.5 bg-white/[0.01] rounded-r flex flex-col md:flex-row md:items-center justify-between gap-2 ${
                      ref.priority === 'CRITICAL' ? 'border-red-500 bg-red-500/5' :
                      ref.priority === 'WARNING' ? 'border-amber-500 bg-amber-500/5' :
                      'border-cyan-500 bg-cyan-500/5'
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={`font-bold tracking-widest ${
                          ref.priority === 'CRITICAL' ? 'text-red-400' :
                          ref.priority === 'WARNING' ? 'text-amber-500' : 'text-cyan-400'
                        }`}>
                          [{ref.event}]
                        </span>
                        <span className="text-slate-300 leading-normal">{ref.message}</span>
                      </div>
                    </div>
                    <span className="text-[10px] text-slate-500 shrink-0 font-bold self-end md:self-center">
                      {ref.timestamp ? new Date(ref.timestamp).toLocaleTimeString() : ''}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Chaos Injection Tool */}
          <form onSubmit={handleChaos} className="lg:col-span-5 flex flex-col justify-between min-h-[300px] bg-black/25 border border-white/5 rounded-xl p-4">
            <div>
              <span className="text-xxs font-mono text-red-500 font-bold uppercase tracking-widest block mb-3 flex items-center gap-1.5">
                <Flame className="w-3.5 h-3.5" /> Simulated Anomaly Injector (Chaos Engineering)
              </span>

              <div className="space-y-3 font-mono text-xs">
                <div className="space-y-1">
                  <label className="text-slate-400 block font-semibold">Target Swarm Node ID</label>
                  <select
                    value={chaosNodeId}
                    onChange={(e) => setChaosNodeId(e.target.value)}
                    required
                    className="w-full bg-black/40 border border-white/10 text-slate-200 rounded-lg px-2.5 py-2 text-xs focus:outline-none focus:border-red-500 font-mono"
                  >
                    <option value="" disabled>Select Node from Mesh...</option>
                    {nodes.map(n => (
                      <option key={n.id} value={n.id}>
                        {n.id} ({n.specialization}) - {n.status}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-slate-400 block font-semibold">Simulated Stress/Failure Reason</label>
                  <textarea
                    value={chaosReason}
                    onChange={(e) => setChaosReason(e.target.value)}
                    required
                    rows={2}
                    className="w-full bg-black/40 border border-white/10 text-slate-200 rounded-lg px-2.5 py-2 text-xs focus:outline-none focus:border-red-500 font-mono resize-none"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !chaosNodeId}
              className="mt-6 w-full bg-red-500/10 border border-red-500/30 hover:bg-red-500/20 text-red-400 py-2.5 rounded-xl font-orbitron font-bold tracking-wider text-xs transition active:scale-[0.98] disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
            >
              <Flame className="w-4 h-4" /> Inject Chaos / Failover Target
            </button>
          </form>

        </div>
      </div>

    </div>
  );
}
