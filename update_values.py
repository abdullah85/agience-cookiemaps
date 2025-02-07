import time
import json
import requests
import math
import random

use_random_values = False  # Set to False to use real data
move_amount_high = 1  # Variable to control the amount the coins move by when high
move_amount_normal = 3  # Variable to control the amount the coins move by when normal

# Division factors for scaling values
market_cap_divisor = 100000000000000
liquidity_divisor = 100000000
price_divisor = 1000
engagements_divisor = 100000

# Fetch data from CookieDAO API
def fetch_data():
    url = 'https://api.cookie.fun/v2/agents/agentsPaged?interval=_7Days&page=1&pageSize=25'
    headers = {'x-api-key': 'b8356b68-33b6-487b-98e5-ccf0f0f2ced4'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['ok']['data']
    else:
        return []

cryptocurrencies = fetch_data()

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def scale_value(value, min_value, max_value):
    normalized_value = (value - min_value) / (max_value - min_value)
    return sigmoid(normalized_value * 12 - 6) * 100

def notify_frontend():
    with open('update_flag.json', 'w') as f:
        json.dump({"updated": True}, f)

def update_values():
    global cryptocurrencies
    if use_random_values:
        for crypto in cryptocurrencies:
            crypto['mindshare'] = random.uniform(0, 100)
            crypto['marketCap'] = random.uniform(0, 1000000000)
            crypto['liquidity'] = random.uniform(0, 100000000)
            crypto['price'] = random.uniform(0, 1000)
            crypto['averageEngagementsCount'] = random.uniform(0, 100000)
    else:
        cryptocurrencies = fetch_data()  # Fetch new data each time
        for crypto in cryptocurrencies:
            crypto['mindshare'] = scale_value(crypto['mindshare'], 0, 100)
            crypto['marketCap'] = scale_value(crypto['marketCap'] / market_cap_divisor, 0, 100)
            crypto['liquidity'] = scale_value(crypto['liquidity'] / liquidity_divisor, 0, 100)
            crypto['price'] = scale_value(crypto['price'] / price_divisor, 0, 100)
            crypto['averageEngagementsCount'] = scale_value(crypto['averageEngagementsCount'] / engagements_divisor, 0, 100)

    notify_frontend()

if __name__ == "__main__":
    while True:
        update_values()
        time.sleep(15)
