import random
import time
import json

with open('coins.json', 'r') as f:
    cryptocurrencies = json.load(f)

use_random_values = False
move_amount_high = 1  # Variable to control the amount the coins move by when high
move_amount_normal = 3  # Variable to control the amount the coins move by when normal

# Assign a bias category to each cryptocurrency
for crypto in cryptocurrencies:
    crypto['bias'] = random.choice(['mindshare', 'marketCap', 'liquidity', 'price', 'averageEngagementsCount'])

def update_values():
    for crypto in cryptocurrencies:
        crypto.setdefault("mindshare", 50)
        crypto.setdefault("marketCap", 50)
        crypto.setdefault("liquidity", 50)
        crypto.setdefault("price", 50)
        crypto.setdefault("averageEngagementsCount", 50)

        if use_random_values:
            for key in ['mindshare', 'marketCap', 'liquidity', 'price', 'averageEngagementsCount']:
                if crypto[key] > 90:
                    crypto[key] = max(1, min(100, crypto[key] - random.randint(0, move_amount_high)))
                elif key == crypto['bias']:
                    crypto[key] = max(1, min(100, crypto[key] + random.randint(0, move_amount_high)))
                else:
                    crypto[key] = max(1, min(100, crypto[key] + random.randint(-move_amount_normal, move_amount_normal)))
        else:
            # Set the bias value to 100 and all other values to 0 only once
            if not crypto.get('initialized', False):
                for key in ['mindshare', 'marketCap', 'liquidity', 'price', 'averageEngagementsCount']:
                    if key == crypto['bias']:
                        crypto[key] = 100
                    else:
                        crypto[key] = 0
                crypto['initialized'] = True

    #with open('cryptocurrencies.json', 'w') as f:
        #json.dump(cryptocurrencies, f)

if __name__ == "__main__":
    while True:
        update_values()
        time.sleep(0.5)
