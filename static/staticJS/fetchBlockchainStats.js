const fs = require('fs');
const fetch = require('node-fetch');

async function fetchBlockchainStats() {
    const response = await fetch('https://api.blockchain.info/stats');
    const data = await response.json();
    fs.writeFileSync('static/data/blockchainStats.json', JSON.stringify(data, null, 2));
}

fetchBlockchainStats();
