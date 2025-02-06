from flask import Flask, render_template, jsonify, request
from update_values import update_values, cryptocurrencies
import threading
import time

app = Flask(__name__)

def update_cryptocurrencies():
    while True:
        update_values()
        time.sleep(0.5)

def determine_region(crypto):
    regions = []
    if "mindshare" in crypto and crypto["mindshare"] > 7:
        regions.append("Popular on Social Media")
    if "marketCap" in crypto and crypto["marketCap"] > 7:
        regions.append("Large Market Value")
    if "liquidity" in crypto and crypto["liquidity"] > 7:
        regions.append("Easy to Buy/Sell")
    if "price" in crypto and crypto["price"] > 7:
        regions.append("Stable Price")
    if "averageEngagementsCount" in crypto and crypto["averageEngagementsCount"] > 7:
        regions.append("High Community Engagement")
    if not regions:
        regions.append("Other")
    return regions

@app.route('/')
def hello_world():
    regions = {"Popular on Social Media": [], "Large Market Value": [], "Easy to Buy/Sell": [], "Stable Price": [], "High Community Engagement": [], "Other": []}
    for crypto in cryptocurrencies:
        crypto_regions = determine_region(crypto)
        for region in crypto_regions:
            regions[region].append(crypto)
    return render_template('index.html', regions=regions)

@app.route('/data')
def data():
    return jsonify(cryptocurrencies)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    for crypto in cryptocurrencies:
        if crypto['name'] == data['name']:
            crypto['mindshare'] = data['mindshare']
            crypto['marketCap'] = data['marketCap']
            crypto['liquidity'] = data['liquidity']
            crypto['price'] = data['price']
            crypto['averageEngagementsCount'] = data['averageEngagementsCount']
            return jsonify(crypto)
    return jsonify({'error': 'Crypto not found'}), 404

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    update_thread = threading.Thread(target=update_cryptocurrencies)
    update_thread.daemon = True
    update_thread.start()
    app.run(debug=True, port=5008)