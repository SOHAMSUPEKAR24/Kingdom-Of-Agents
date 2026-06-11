const fs = require('fs');
const d3 = require('d3-force');

// Read from curl directly instead of file, or just mock it:
const execSync = require('child_process').execSync;
const topology = JSON.parse(execSync('curl -s http://127.0.0.1:8000/api/v1/topology').toString());

const kingNodes = topology.nodes.filter(n => n.type === 'KING');
const knightNodes = topology.nodes.filter(n => n.type === 'KNIGHT');
const houseNodes = topology.nodes.filter(n => n.type === 'HOUSE');

const houseCount = houseNodes.length;
const houseRadius = 400;
const centerX = 600;
const centerY = 450;

const preCalculatedPositions = {};

kingNodes.forEach(n => preCalculatedPositions[n.id] = { x: centerX, y: centerY, fx: centerX, fy: centerY });

knightNodes.forEach((n, idx) => {
  const angle = (idx / Math.max(1, knightNodes.length)) * 2 * Math.PI;
  const nx = centerX + 200 * Math.cos(angle);
  const ny = centerY + 200 * Math.sin(angle);
  preCalculatedPositions[n.id] = { x: nx, y: ny, fx: nx, fy: ny };
});

houseNodes.forEach((n, idx) => {
  const angle = (idx / Math.max(1, houseCount)) * 2 * Math.PI;
  const nx = centerX + houseRadius * Math.cos(angle);
  const ny = centerY + houseRadius * Math.sin(angle);
  preCalculatedPositions[n.id] = { x: nx, y: ny, fx: nx, fy: ny };
});

const simulationNodes = topology.nodes.map((n) => {
  const pos = preCalculatedPositions[n.id] || { x: centerX, y: centerY };
  return {
    id: n.id,
    x: pos.x,
    y: pos.y,
    fx: pos.fx,
    fy: pos.fy
  };
});

const validNodeIds = new Set(simulationNodes.map(n => n.id));
const simulationLinks = topology.edges
  .filter(e => validNodeIds.has(e.source) && validNodeIds.has(e.target))
  .map(e => ({
    source: e.source,
    target: e.target
  }));

const simulation = d3.forceSimulation(simulationNodes)
  .force('charge', d3.forceManyBody().strength(-800))
  .force('link', d3.forceLink(simulationLinks).id(d => d.id).distance(150).strength(0.5))
  .force('collide', d3.forceCollide().radius(d => 80).iterations(3))
  .stop();

for (let i = 0; i < 300; i++) simulation.tick();

let nanCount = 0;
simulationNodes.forEach(n => {
  if (isNaN(n.x) || isNaN(n.y)) nanCount++;
});

console.log(`Total nodes: ${simulationNodes.length}`);
console.log(`NaN nodes: ${nanCount}`);
if (nanCount > 0) {
  console.log('Sample NaN node:', simulationNodes.find(n => isNaN(n.x)));
}

