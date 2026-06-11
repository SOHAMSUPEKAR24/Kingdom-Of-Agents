const fs = require('fs');
const d3 = require('d3-force');
const execSync = require('child_process').execSync;
const topology = JSON.parse(execSync('curl -s http://127.0.0.1:8000/api/v1/topology').toString());

const simulationNodes = topology.nodes.map((n) => {
  return { id: n.id, x: 600, y: 450 };
});
const validNodeIds = new Set(simulationNodes.map(n => n.id));
const simulationLinks = topology.edges
  .filter(e => validNodeIds.has(e.source) && validNodeIds.has(e.target))
  .map(e => ({ source: e.source, target: e.target }));

const simulation = d3.forceSimulation(simulationNodes)
  .force('charge', d3.forceManyBody().strength(-800))
  .force('link', d3.forceLink(simulationLinks).id(d => d.id).distance(150).strength(0.5))
  .force('collide', d3.forceCollide().radius(d => 80).iterations(3))
  .stop();

for (let i = 0; i < 300; i++) simulation.tick();

let max_x = -Infinity;
let min_x = Infinity;
let max_y = -Infinity;
let min_y = Infinity;

simulationNodes.forEach(n => {
  if (n.x > max_x) max_x = n.x;
  if (n.x < min_x) min_x = n.x;
  if (n.y > max_y) max_y = n.y;
  if (n.y < min_y) min_y = n.y;
});
console.log(`X range: ${min_x} to ${max_x}`);
console.log(`Y range: ${min_y} to ${max_y}`);

