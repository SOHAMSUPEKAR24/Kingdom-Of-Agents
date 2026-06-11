'use client';

import React, { useEffect, useState, useMemo } from 'react';
import ReactFlow, {
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Handle,
  Position,
  NodeProps,
  Edge,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { forceSimulation, forceLink, forceManyBody, forceCenter, forceCollide, forceX, forceY } from 'd3-force';
import { useKingdomStore } from '../store/useKingdomStore';
import { Shield, Hammer, Users, Cpu, Ban, AlertTriangle, Play, HelpCircle } from 'lucide-react';

// Custom Node Renderer with Glassmorphism, glows, and theme colors
const CustomNode = ({ data }: NodeProps) => {
  const type = data.type as string;
  const trust = data.trust as number | undefined;

  const nodeStyles = {
    KING: 'border-yellow-500 bg-yellow-500/20 text-yellow-400 shadow-[0_0_25px_rgba(212,175,55,0.4)] px-6 py-4 border-2',
    KNIGHT: 'border-amber-500 bg-amber-950/20 text-amber-300 shadow-[0_0_15px_rgba(245,158,11,0.2)]',
    HOUSE: 'border-cyan-400 bg-cyan-950/30 text-cyan-300 shadow-[0_0_20px_rgba(6,182,212,0.3)] px-5 py-3 border-2',
    SOLDIER: 'border-teal-500 bg-teal-950/20 text-teal-400 shadow-[0_0_10px_rgba(20,184,166,0.15)]',
    RETIRED_SOLDIER: 'border-slate-800 bg-slate-950/40 text-slate-500 border-dashed opacity-60',
    QUARANTINED_SOLDIER: 'border-red-500 bg-red-950/20 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.3)] animate-pulse',
    TASK: 'border-yellow-500/50 bg-yellow-950/10 text-yellow-500',
    GENOME: 'border-emerald-500/80 bg-emerald-950/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]',
    DOCTRINE: 'border-fuchsia-500/80 bg-fuchsia-950/20 text-fuchsia-400 shadow-[0_0_15px_rgba(217,70,239,0.2)]',
    UNKNOWN: 'border-slate-700 bg-slate-900 text-slate-300',
  };

  const icons = {
    KING: <span className="text-2xl">👑</span>,
    KNIGHT: <Shield className="w-5 h-5 text-amber-400" />,
    HOUSE: <Cpu className="w-6 h-6 text-cyan-400" />,
    SOLDIER: <Users className="w-4 h-4 text-teal-400" />,
    RETIRED_SOLDIER: <Users className="w-4 h-4 text-slate-500" />,
    QUARANTINED_SOLDIER: <Ban className="w-4 h-4 text-red-500 animate-spin" />,
    TASK: <Play className="w-4 h-4 text-yellow-500" />,
    GENOME: <span className="text-sm">🧬</span>,
    DOCTRINE: <span className="text-sm">📖</span>,
    UNKNOWN: <HelpCircle className="w-4 h-4 text-slate-400" />,
  };

  let style = nodeStyles[type as keyof typeof nodeStyles] || nodeStyles.UNKNOWN;
  const icon = icons[type as keyof typeof icons] || icons.UNKNOWN;

  // Apply real-time genetic trust glows and warning rings
  if (trust !== undefined) {
    if (trust >= 0.8) {
      style = `${style} shadow-[0_0_20px_rgba(16,185,129,0.5)] border-emerald-400/90`;
    } else if (trust < 0.6) {
      style = `${style} shadow-[0_0_20px_rgba(245,158,11,0.5)] border-amber-500/90 animate-pulse`;
    }
  }

  const isMain = type === 'KING' || type === 'HOUSE';

  return (
    <div className={`backdrop-blur-md rounded-xl flex items-center gap-3 font-mono tracking-wide ${isMain ? 'text-sm' : 'text-xs px-4 py-2 border'} ${style}`}>
      <Handle type="target" position={Position.Top} className="opacity-0" />
      
      <div className="flex-shrink-0">{icon}</div>
      <div className="text-left">
        <div className={`font-orbitron ${isMain ? 'font-black text-sm tracking-widest uppercase' : 'font-bold text-[10px]'}`}>
          {data.label}
        </div>
        <div className={`${isMain ? 'text-[10px]' : 'text-[9px]'} opacity-60 truncate max-w-[150px]`}>
          {trust !== undefined ? `Trust: ${Math.round(trust * 100)}%` : (data.details || type)}
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="opacity-0" />
    </div>
  );
};

// Define custom node types mapping for React Flow outside component to prevent re-renders
const nodeTypes = { customNode: CustomNode };

export default function GraphEngine() {
  const { topology, genomes } = useKingdomStore();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  useEffect(() => {
    if (!topology.nodes || topology.nodes.length === 0) return;

    // Deterministic Top-Down Hierarchical Layout (bypassing physical simulations for perfect structure)
    const nodesByType: Record<string, any[]> = {};
    topology.nodes.forEach(n => {
      let nodeType = n.type;
      if (n.id.startsWith('genome_')) nodeType = 'GENOME';
      else if (n.id.includes('-') && (n.label.includes('DOCTRINE') || n.label.includes('Wisdom') || n.id.length > 25)) nodeType = 'DOCTRINE';
      
      if (!nodesByType[nodeType]) nodesByType[nodeType] = [];
      nodesByType[nodeType].push({ ...n, computedType: nodeType });
    });

    const hierarchy = [
      { types: ['KING'], radius: 0 },
      { types: ['HOUSE'], radius: 150 },
      { types: ['KNIGHT'], radius: 250 },
      { types: ['TASK', 'GENOME'], radius: 400 },
      { types: ['SOLDIER', 'QUARANTINED_SOLDIER', 'RETIRED_SOLDIER'], radius: 550 },
      { types: ['DOCTRINE', 'UNKNOWN'], radius: 700 }
    ];

    const flowNodes: any[] = [];
    const centerX = 0;
    const centerY = 0;
    
    hierarchy.forEach((layer, layerIdx) => {
      let layerNodes: any[] = [];
      layer.types.forEach(t => {
        if (nodesByType[t]) layerNodes.push(...nodesByType[t]);
      });
      
      const nodeCount = layerNodes.length;
      
      layerNodes.forEach((n, idx) => {
        const genome = genomes.find((g) => g.id === n.id);
        const trust = genome?.trust_metric;
        
        let x = centerX;
        let y = centerY;
        
        if (layer.radius > 0 && nodeCount > 0) {
          // Stagger initial angle per orbit for a more organic "planetary swarm" look
          const offset = (layerIdx * Math.PI) / 4;
          const angle = offset + (idx * 2 * Math.PI) / nodeCount - Math.PI / 2;
          
          x = centerX + layer.radius * Math.cos(angle);
          y = centerY + layer.radius * Math.sin(angle);
        }
        
        flowNodes.push({
          id: String(n.id),
          type: 'customNode',
          data: { 
            id: n.id, 
            label: n.label, 
            type: n.computedType, 
            details: n.details, 
            trust 
          },
          position: { x, y },
        });
      });
    });

    const validNodeIds = new Set(flowNodes.map(n => n.id));

    // Build beautiful particle-dash flowing edges representing real-time system flow
    const flowEdges: Edge[] = topology.edges
      .filter((e: any) => validNodeIds.has(e.source) && validNodeIds.has(e.target))
      .map((e: any, idx: number) => {
      const isCritical = e.type === 'GOVERNS' || e.type === 'AUDITS' || e.type === 'QUARANTINES';
      const isEvolution = e.type === 'MUTATED_FROM' || e.type === 'CONSOLIDATED_INTO' || e.type === 'HAS_GENOME';
      const isAnomaly = e.type === 'TRUST_ANOMALY' || e.type === 'FAILURE_PATH';
      
      let edgeColor = '#00f2fe'; // Default: cyan
      if (isCritical) edgeColor = '#f43f5e'; // Rose
      else if (isEvolution) edgeColor = '#10b981'; // Emerald
      else if (isAnomaly) edgeColor = '#f59e0b'; // Amber
      
      return {
        id: `e-${idx}`,
        source: e.source,
        target: e.target,
        type: 'smoothstep',
        animated: isEvolution || isAnomaly || isCritical, // Animated flow
        label: e.type,
        labelStyle: { fill: '#94a3b8', fontSize: 8, fontFamily: 'monospace', fontWeight: 'bold' },
        labelBgStyle: { fill: '#0a0a14', fillOpacity: 0.8 },
        style: {
          stroke: edgeColor,
          strokeWidth: isCritical || isAnomaly ? 2 : 1.5,
          opacity: 0.75,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: edgeColor,
          width: 10,
          height: 10,
        },
      };
    });

    setNodes(flowNodes);
    setEdges(flowEdges);
  }, [topology, genomes, setNodes, setEdges]);

  // Node hover drawer detail handler
  const handleNodeClick = (_: any, node: any) => {
    const originalNode = topology.nodes.find((n) => n.id === node.id);
    setSelectedNode(originalNode || node);
  };

  return (
    <div className="relative backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl p-6 shadow-2xl h-[550px] flex flex-col">
      {/* Topology Title Overlay */}
      <div className="absolute top-6 left-6 z-10 space-y-1 pointer-events-none select-none">
        <h2 className="font-orbitron text-md font-bold tracking-wider text-cyan-400 flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" /> Kingdom Topology Engine
        </h2>
        <p className="text-xxs text-slate-400 font-mono">Force-directed map of persistent civilization relationships</p>
      </div>

      <div className="flex-1 w-full bg-black/40 border border-white/5 rounded-xl overflow-hidden mt-8">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          onNodeClick={handleNodeClick}
          fitView
          minZoom={0.1}
          maxZoom={2.0}
        >
          <Background color="#00f2fe" style={{ opacity: 0.03 }} gap={16} />
          <Controls className="bg-black/60 border border-white/10 rounded-lg text-slate-300 fill-slate-300" />
        </ReactFlow>
      </div>

      {/* Node Details Slide-Out Drawer Panel */}
      {selectedNode && (
        <div className="absolute bottom-6 right-6 top-20 w-80 z-20 backdrop-blur-lg bg-black/85 border border-white/15 rounded-xl p-5 shadow-2xl flex flex-col animate-slide-up">
          <div className="flex items-center justify-between border-b border-white/10 pb-3 mb-4">
            <h3 className="font-orbitron font-bold text-sm tracking-wider text-slate-200">Node Cognition Drawer</h3>
            <button 
              onClick={() => setSelectedNode(null)}
              className="text-xs text-slate-400 hover:text-white font-mono"
            >
              Close ✕
            </button>
          </div>

          <div className="space-y-4 overflow-y-auto pr-1 flex-1 font-mono text-xs scrollbar-thin">
            <div className="space-y-1">
              <span className="text-xxs text-slate-500 uppercase tracking-widest block">Node Address</span>
              <span className="font-semibold text-cyan-400">{selectedNode.id}</span>
            </div>
            
            <div className="space-y-1">
              <span className="text-xxs text-slate-500 uppercase tracking-widest block">Role Type</span>
              <span className={`px-2 py-0.5 rounded text-xxs font-bold inline-block border ${
                selectedNode.type === 'KING' ? 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400' :
                selectedNode.type === 'KNIGHT' ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
                selectedNode.type === 'HOUSE' ? 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400' :
                selectedNode.type === 'QUARANTINED_SOLDIER' ? 'bg-red-500/10 border-red-500/20 text-red-500 animate-pulse' :
                'bg-white/5 border-white/5 text-slate-300'
              }`}>
                {selectedNode.type}
              </span>
            </div>

            <div className="space-y-1">
              <span className="text-xxs text-slate-500 uppercase tracking-widest block">Identity Label</span>
              <span className="text-slate-300">{selectedNode.label}</span>
            </div>

            <div className="space-y-1">
              <span className="text-xxs text-slate-500 uppercase tracking-widest block">Operational Description</span>
              <p className="text-slate-400 bg-white/[0.02] border border-white/5 p-2 rounded-lg leading-normal">
                {selectedNode.details || 'No detailed descriptor recorded.'}
              </p>
            </div>

            {selectedNode.type.includes('SOLDIER') && (
              <div className="pt-2 border-t border-white/5 space-y-2">
                <span className="text-xxs text-slate-500 uppercase tracking-widest block">Trust Integrity Log</span>
                <div className="bg-red-500/5 border border-red-500/10 rounded-lg p-3 text-red-400/90 leading-relaxed text-xxs flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-500 flex-shrink-0" />
                  <span>
                    Disposable runtime node subject to constitutional governance quarantines and garbage collection.
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
