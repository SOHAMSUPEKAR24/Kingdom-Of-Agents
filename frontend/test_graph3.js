const fs = require('fs');
const execSync = require('child_process').execSync;
const topology = JSON.parse(execSync('curl -s http://127.0.0.1:8000/api/v1/topology').toString());

const nodesByType = {};
topology.nodes.forEach(n => {
  let nodeType = n.type;
  if (n.id.startsWith('genome_')) nodeType = 'GENOME';
  else if (n.id.includes('-') && (n.label.includes('DOCTRINE') || n.label.includes('Wisdom') || n.id.length > 25)) nodeType = 'DOCTRINE';
  
  if (!nodesByType[nodeType]) nodesByType[nodeType] = [];
  nodesByType[nodeType].push(n);
});

console.log('Types found:', Object.keys(nodesByType));

const hierarchy = [
  { types: ['KING'], radius: 0 },
  { types: ['HOUSE'], radius: 250 },
  { types: ['KNIGHT'], radius: 400 },
  { types: ['TASK', 'GENOME'], radius: 650 },
  { types: ['SOLDIER', 'QUARANTINED_SOLDIER', 'RETIRED_SOLDIER'], radius: 950 },
  { types: ['DOCTRINE', 'UNKNOWN'], radius: 1200 }
];

let added = 0;
hierarchy.forEach(layer => {
  layer.types.forEach(t => {
    if (nodesByType[t]) added += nodesByType[t].length;
  });
});

console.log('Nodes mapped:', added);
console.log('Total nodes:', topology.nodes.length);
