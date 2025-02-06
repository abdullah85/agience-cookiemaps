import time
import json

use_random_values = False  # Set to False to use real data
move_amount_high = 1  # Variable to control the amount the coins move by when high
move_amount_normal = 3  # Variable to control the amount the coins move by when normal

# Predefined dictionary with coin values
cryptocurrencies = [
    {
        "agentName": "Bitcoin",
        "mindshare": 90,
        "marketCap": 1000000000,
        "liquidity": 800000000,
        "price": 50000,
        "averageEngagementsCount": 100000
    },
    {
        "agentName": "Ethereum",
        "mindshare": 85,
        "marketCap": 500000000,
        "liquidity": 400000000,
        "price": 3000,
        "averageEngagementsCount": 80000
    },
    # Add more predefined coins as needed
]

def scale_value(value, min_value, max_value):
    return max(1, min(100, ((value - min_value) / (max_value - min_value)) * 100))

def notify_frontend():
    with open('update_flag.json', 'w') as f:
        json.dump({"updated": True}, f)

def update_values():
    for crypto in cryptocurrencies:
        crypto['mindshare'] = scale_value(crypto['mindshare'], 0, 100)
        crypto['marketCap'] = scale_value(crypto['marketCap'], 0, 1000000000)
        crypto['liquidity'] = scale_value(crypto['liquidity'], 0, 100000000)
        crypto['price'] = scale_value(crypto['price'], 0, 1000)
        crypto['averageEngagementsCount'] = scale_value(crypto['averageEngagementsCount'], 0, 100000)

    notify_frontend()

    #with open('cryptocurrencies.json', 'w') as f:
        #json.dump(cryptocurrencies, f)

if __name__ == "__main__":
    while True:
        update_values()
        time.sleep(15)
