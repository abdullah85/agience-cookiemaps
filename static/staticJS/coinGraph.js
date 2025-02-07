// document.getElementById('search-input').addEventListener('input', async function() {
//     const query = this.value.toLowerCase();
//     if (query.length > 0) {
//         const response = await fetch(`https://api.coingecko.com/api/v3/search?query=${query}`);
//         const data = await response.json();
//         displaySearchResults(data.coins);
//     } else {
//         clearSearchResults();
//     }
// });

// function displaySearchResults(coins) {
//     const searchResults = document.getElementById('search-results');
//     searchResults.innerHTML = '';
//     coins.forEach(coin => {
//         const li = document.createElement('li');
//         li.textContent = coin.name;
//         li.dataset.coinId = coin.id;
//         searchResults.appendChild(li);
//     });
//     searchResults.style.display = 'block';
// }

// function clearSearchResults() {
//     const searchResults = document.getElementById('search-results');
//     searchResults.innerHTML = '';
//     searchResults.style.display = 'none';
// }

// document.getElementById('search-results').addEventListener('click', function(e) {
//     if (e.target.tagName === 'LI') {
//         const coinId = e.target.dataset.coinId;
//         fetchCoinData(coinId, '1D');
//         clearSearchResults();
//     }
// });

// document.querySelectorAll('.time-range button').forEach(button => {
//     button.addEventListener('click', function() {
//         const range = this.dataset.range;
//         const coinId = document.querySelector('.coin-card[data-coin-id]').dataset.coinId;
//         fetchCoinData(coinId, range);
//     });
// });



// async function fetchCoinData(coinId, range) {
//     const interval = {
//         '1D': '1d',
//         '1W': '1w',
//         '1M': '1M',
//         'YTD': '1y',
//         'All': 'max'
//     }[range];
//     if (!interval) {
//         console.error('Invalid range:', range);
//         return;
//     }
//     const proxyUrl = 'https://api.allorigins.win/get?url=';
//     const targetUrl = `https://api.binance.com/api/v3/klines?symbol=${coinId.toUpperCase()}USDT&interval=${interval}`;
//     const response = await fetch(proxyUrl + encodeURIComponent(targetUrl));
//     if (!response.ok) {
//         console.error('Failed to fetch data:', response.statusText);
//         return;
//     }
//     const data = await response.json();
//     let parsedData;
//     try {
//         parsedData = JSON.parse(data.contents);
//     } catch (error) {
//         console.error('Failed to parse data:', error);
//         return;
//     }
//     if (!Array.isArray(parsedData)) {
//         console.error('Invalid data format:', parsedData);
//         return;
//     }
//     updateChart(parsedData);
// }

// function updateChart(data) {
//     const ctx = document.getElementById('cryptoChart').getContext('2d');
//     if (window.cryptoChart && typeof window.cryptoChart.destroy === 'function') {
//         window.cryptoChart.destroy();
//     }
//     window.cryptoChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: data.map(value => new Date(value[0]).toLocaleDateString()),
//             datasets: [{
//                 label: 'Price',
//                 data: data.map(value => value[4]), // Closing price
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 borderWidth: 1,
//                 fill: false
//             }]
//         },
//         options: {
//             scales: {
//                 x: {
//                     type: 'time',
//                     time: {
//                         unit: 'day'
//                     }
//                 },
//                 y: {
//                     beginAtZero: false
//                 }
//             }
//         }
//     });
// }
