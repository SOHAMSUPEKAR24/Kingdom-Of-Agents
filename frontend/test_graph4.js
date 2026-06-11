const fs = require('fs');
const execSync = require('child_process').execSync;
const topology = JSON.parse(execSync('curl -s http://127.0.0.1:8000/api/v1/topology').toString());

const ids = topology.nodes.map(n => n.id);
const uniqueIds = new Set(ids);
console.log(`Total nodes: ${ids.length}, Unique IDs: ${uniqueIds.size}`);
