import requests
import json

API_KEY = '******'
BASE_URL = 'https://api.cookie.fun/v2/agents/agentsPaged'
INTERVAL = '_7Days'
PAGE_SIZE = 25

def get_agents_paged(page):
    url = f"{BASE_URL}?interval={INTERVAL}&page={page}&pageSize={PAGE_SIZE}"
    headers = {'x-api-key': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def collect_all_coin_names():
    page = 1
    all_coins = []
    while True:
        data = get_agents_paged(page)
        if not data['success']:
            break
        agents = data['ok']['data']
        if not agents:
            break
        for agent in agents:
            all_coins.append(agent['agentName'])
        page += 1
        if page > data['ok']['totalPages']:
            break
    return all_coins

def save_to_json(data, filename='coins.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    coins = collect_all_coin_names()
    save_to_json(coins)
    print(f"Collected {len(coins)} coin names.")
