import requests
import json
import time
import sqlite3

def get_agent_data_by_twitter_username(twitter_username, interval):
    url = f'https://api.cookie.fun/v2/agents/twitterUsername/{twitter_username}?interval={interval}'
    headers = {'x-api-key': 'b8356b68-xxxx-xxxx-xxxx-ccf0fxxxced4'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_all_agents(interval, page=1, page_size=25):
    url = f'https://api.cookie.fun/v2/agents/agentsPaged?interval={interval}&page={page}&pageSize={page_size}'
    headers = {'x-api-key': 'b8356b68-33b6-487b-98e5-ccf0f0f2ced4'}
    response = requests.get(url, headers=headers)
    return response.json()

def print_agent_data(agent_data):
    if agent_data['success']:
        agent = agent_data['ok']
        print(f"Agent Name: {agent['agentName']}")
        print(f"Mindshare: {agent['mindshare']}")
        print(f"Market Cap: {agent['marketCap']}")
        print(f"Price: {agent['price']}")
        print(f"Liquidity: {agent['liquidity']}")
        print(f"Volume (24 Hours): {agent['volume24Hours']}")
        print(f"Holders Count: {agent['holdersCount']}")
        print(f"Followers Count: {agent['followersCount']}")
        print(f"Top Tweets: {agent['topTweets']}")
    else:
        print("Failed to retrieve agent data")

def save_agent_names_to_json(agents_data, filename='agents.json'):
    agent_names = [agent['agentName'] for agent in agents_data['ok']['data']]
    data = {
        "count": len(agent_names),
        "agents": agent_names
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def save_agent_data_to_db(agent_data, db_name='agents.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agents
                 (agentName TEXT, mindshare REAL, marketCap REAL, price REAL, liquidity REAL, volume24Hours REAL, holdersCount INTEGER, followersCount INTEGER)''')
    
    if agent_data['success']:
        agent = agent_data['ok']
        c.execute('''INSERT INTO agents (agentName, mindshare, marketCap, price, liquidity, volume24Hours, holdersCount, followersCount)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (agent['agentName'], agent['mindshare'], agent['marketCap'], agent['price'], agent['liquidity'], agent['volume24Hours'], agent['holdersCount'], agent['followersCount']))
        conn.commit()
    conn.close()

def get_top_agents_by_category(agents_data, category, top_n):
    sorted_agents = sorted(agents_data['ok']['data'], key=lambda x: x[category], reverse=True)
    return sorted_agents[:top_n]

def main():
    interval = "_7Days"
    page_size = 25
    all_agents = []

    while True:
        page = 1
        while True:
            agents_data = get_all_agents(interval, page, page_size)
            if agents_data['success']:
                all_agents.extend(agents_data['ok']['data'])
                if page >= agents_data['ok']['totalPages']:
                    break
                page += 1
            else:
                print("Failed to retrieve agents data")
                break

        categories = ['mindshare', 'marketCap', 'liquidity', 'price', 'averageEngagementsCount']
        top_agents = []
        for category in categories:
            top_agents.extend(get_top_agents_by_category({"ok": {"data": all_agents}}, category, 10))

        save_agent_names_to_json({"ok": {"data": top_agents}})
        for agent in top_agents:
            twitter_usernames = agent['twitterUsernames']
            for username in twitter_usernames:
                agent_data = get_agent_data_by_twitter_username(username, interval)
                print_agent_data(agent_data)
                save_agent_data_to_db(agent_data)
                print("\n")
        time.sleep(15)

if __name__ == "__main__":
    main()
