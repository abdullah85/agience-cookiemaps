import time
import json
import requests
import math
import random
import os

use_random_values = False  # Set to False to use real data
move_amount_high = 1  # Variable to control the amount the coins move by when high
move_amount_normal = 3  # Variable to control the amount the coins move by when normal

# Division factors for scaling values
market_cap_divisor = 100000000000000
liquidity_divisor = 100000000
price_divisor = 1000
engagements_divisor = 100000

cookie_api_key = os.getenv("COOKIE_API_KEY")
base_url = "https://api.cookie.fun"

if not cookie_api_key:
    raise ValueError("Cookie API key is missing. Please add it to the .env file.")

class CachedPages:
    def __init__(self, duration=5, threshold=600):
        self.duration = duration
        self.threshold = threshold
        self.data = {}
        self.initTime = {} # time to live info

    def updateDuration(self):
        self.duration *= 2
        if(self.duration >= self.threshold):
            self.duration = 5 # reset the time to wait

    def set(self, page_number, response):
        self.data[page_number] = response
        self.initTime[page_number] = time.time()

    def get(self, page_number):
        if(page_number in self.initTime.keys()):
            currDuration = time.time() - self.initTime[page_number]
            if(page_number in self.data.keys() and currDuration <= self.duration):
                return self.data[page_number]
        url = f'https://api.cookie.fun/v2/agents/agentsPaged?interval=_7Days&page={page_number}&pageSize=25'
        headers = {'x-api-key': cookie_api_key}
        response = requests.get(url, headers=headers)
        # Make the request and send the response and the onus is on the invoker to verify and set
        return response

pages = CachedPages()

# Fetch data from CookieDAO API
def fetch_data(page_number=1):
    response = pages.get(page_number)
    if response.status_code == 200:
        pages.set(page_number, response)
        return response.json()['ok']['data']
    # Update duration and log the error message
    pages.updateDuration()
    print(response)
    # Return the empty list
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
