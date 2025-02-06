document.addEventListener('DOMContentLoaded', async function() {
    const response = await fetch('https://api.blockchain.info/stats');
    const data = await response.json();
    displayBlockchainStats(data);
});

function displayBlockchainStats(stats) {
    const statsContainer = document.getElementById('blockchain-stats');
    statsContainer.innerHTML = `
        <p>Market Price USD: $${stats.market_price_usd}</p>
        <p>Hash Rate: ${stats.hash_rate} TH/s</p>
        <p>Total Fees BTC: ${stats.total_fees_btc} BTC</p>
        <p>Number of BTC Mined: ${stats.n_btc_mined} BTC</p>
        <p>Number of Transactions: ${stats.n_tx}</p>
        <p>Number of Blocks Mined: ${stats.n_blocks_mined}</p>
        <p>Minutes Between Blocks: ${stats.minutes_between_blocks}</p>
        <p>Total BTC: ${stats.totalbc / 100000000} BTC</p>
        <p>Total Blocks: ${stats.n_blocks_total}</p>
        <p>Estimated Transaction Volume USD: $${stats.estimated_transaction_volume_usd}</p>
        <p>Blocks Size: ${stats.blocks_size} bytes</p>
        <p>Miners Revenue USD: $${stats.miners_revenue_usd}</p>
        <p>Next Retarget: ${stats.nextretarget}</p>
        <p>Difficulty: ${stats.difficulty}</p>
        <p>Estimated BTC Sent: ${stats.estimated_btc_sent} BTC</p>
        <p>Miners Revenue BTC: ${stats.miners_revenue_btc} BTC</p>
        <p>Total BTC Sent: ${stats.total_btc_sent} BTC</p>
        <p>Trade Volume BTC: ${stats.trade_volume_btc} BTC</p>
        <p>Trade Volume USD: $${stats.trade_volume_usd}</p>
    `;
}
