import os
import sys
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
from update_values import update_values, cryptocurrencies
import threading
import time

from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
cookie_api_key = os.getenv("COOKIE_API_KEY")
base_url = "https://api.cookie.fun"

if not api_key:
    raise ValueError("OpenAI API key is missing. Please add it to the .env file.")

if not cookie_api_key:
    raise ValueError("Cookie API key is missing. Please add it to the .env file.")

app = Flask(__name__)

plugin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'llm_integration/langchain_plugins'))
sys.path.append(plugin_path)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key)

# Load coin names from JSON file
with open('coin_names.json', 'r') as file:
    coin_names = json.load(file)

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/chart')
def hello_world():
    regions = {"Popular on Social Media": [], "Large Market Value": [], "Easy to Buy/Sell": [], "Stable Price": [], "High Community Engagement": [], "Other": []}
    for crypto in cryptocurrencies:
        crypto_regions = determine_region(crypto)
        for region in crypto_regions:
            regions[region].append(crypto)
    return render_template('index.html', regions=regions)

@app.route('/data')
def data():
    #print("Serving data:", cryptocurrencies)  # Log the data being served
    return jsonify(cryptocurrencies)

@app.route('/update', methods=['POST'])
def update():
    market_cap_divisor = 100000000000000
    liquidity_divisor = 100000000
    price_divisor = 1000
    engagements_divisor = 100000
    data = request.json
    for crypto in cryptocurrencies:
        if crypto['agentName'] == data['name']:
            crypto['mindshare'] = data['mindshare']
            crypto['marketCap'] = data['marketCap'] / market_cap_divisor
            crypto['liquidity'] = data['liquidity'] / liquidity_divisor
            crypto['price'] = data['price']
            crypto['averageEngagementsCount'] = data['averageEngagementsCount']
            return jsonify(crypto)
    return jsonify({'error': 'Crypto not found'}), 404

@app.route('/dashboard_update')
def dashboard_update():
    return render_template('Dashboard_Update.html')

@app.route('/check_update')
def check_update():
    with open('update_flag.json', 'r') as f:
        update_flag = json.load(f)
    if update_flag.get("updated"):
        with open('update_flag.json', 'w') as f:
            json.dump({"updated": False}, f)
        return jsonify({"updated": True})
    return jsonify({"updated": False})

@app.route('/get_btc_price')
def get_btc_price():
    # Dummy data for BTC price. Replace this with real API calls later.
    return jsonify({"price": "$45,000"})
def query_langchain(prompt: str):
    try:
        response = llm.invoke(prompt)
        if hasattr(response, 'content'):
            return response.content 
        else:
            return str(response)  
    except Exception as e:
        return f"Error in LangChain query: {e}"

def fetch_from_cookie_api(endpoint: str, params: dict = None):
    headers = {"x-api-key": cookie_api_key}
    try:
        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()  
        data = response.json()
        print("Fetched data from Cookie API:")  
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error: {http_err}"}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"error": f"An error occurred while fetching data from the Cookie API: {err}"}

@app.route("/chat")
def index():
    return render_template("agience_llmflask.html")
@app.route("/Tutorial")
def Tutorial():
    return render_template("Tutorial.html")

class CachedCoins:
    def __init__(self, duration=5, threshold=600):
        self.duration = duration
        self.threshold = threshold
        self.data = {}
        self.initTime = {} # time to live info

    def updateDuration(self):
        self.duration *= 2
        if(self.duration >= self.threshold):
            self.duration = 5 # reset the time to wait

    def set(self, coin_name, response):
        self.data[coin_name] = response
        self.initTime[coin_name] = time.time()

    def get(self, coin_name):
        if(coin_name in self.initTime.keys()):
            currDuration = time.time() - self.initTime[coin_name]
            if(coin_name in self.data.keys() and currDuration <= self.duration):
                return self.data[coin_name]
        url = f"https://api.cookie.fun/v1/hackathon/search/{coin_name.replace(' ', '%20')}"
        headers = {'x-api-key': cookie_api_key}
        today = datetime.today()
        prevDate = today - timedelta(days=30)
        params = {"from": prevDate.strftime('%Y-%mm-%d'), "to": today.strftime('%Y-%mm-%d')}
        # response = requests.get(url, headers=headers)
        response = requests.get(url, headers=headers, params=params)
        # Make the request and send the response and the onus is on the invoker to verify and set
        return response

coins = CachedCoins()

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

def get_coin_value(coin_name):
    try:
        # url = f"v1/hackathon/search/{coin_name.replace(' ', '%20')}"
        # params = {"from": "2025-01-01", "to": "2025-01-20"}
        # data = fetch_from_cookie_api(url, params)
        data = coins.get(coin_name)
        if(data.status_code != 200):
            coins.updateDuration()
        else:
            data=data.json()
        return data
    except Exception as e:
        print(f"Error fetching value for {coin_name}: {e}")
        return None

@app.route("/query", methods=["GET", "POST"])
def query_openai():
    try:
        if request.method == "POST":
            question = request.json.get("question")
        elif request.method == "GET":
            question = request.args.get("question")
            if not question:
                return jsonify({"error": "Missing 'question' parameter."}), 400

        # Check if the question contains any coin names
        mentioned_coins = [coin for coin in coin_names if coin.lower() in question.lower()]
        coin_values = {}
        if mentioned_coins:
            print("Mentioned coins:", mentioned_coins)
            for coin in mentioned_coins:
                coin_value = get_coin_value(coin)
                coin_values[coin] = coin_value
                print(f"Value for {coin}: {coin_value}")

        # Filter data for mentioned coins
        filtered_data = {
            "ok": {
                "data": [
                    {
                        **crypto,
                        "topTweets": crypto.get("topTweets", [])[:4]  # Limit to 3-4 tweets
                    }
                    for crypto in cryptocurrencies
                    if crypto["agentName"].lower() in [coin.lower() for coin in mentioned_coins]
                ]
            },
            "success": True,
            "error": None
        }

        prompt = f"""Here is the data fetched from the Cookie API:
        {filtered_data}

        Here are the values for the mentioned coins:
        {coin_values}

        Based on this data, answer the following question: {question}

        Do not use any pre-trained knowledge; base your response solely on the provided data. Keep your responses short and concise, while still being helpful and professional. Do not show any thinking processes and don't mention you are using Cookie API or LangChain. Round all values to nearest 10th if above 10 and nearest thousandth if below."""

        response = query_langchain(prompt)
        return jsonify({"openai_response": response})
    except Exception as e:
        return jsonify({"error": f"Error querying OpenAI: {str(e)}"}), 500

@app.route("/cookie/twitter/<username>")
def get_twitter_cookie(username):
    try:
        interval = request.args.get("interval", "_7Days")
        url = f"v2/agents/twitterUsername/{username}?interval={interval}"
        data = fetch_from_cookie_api(url)

        prompt = f"""Here is the Twitter data for {username} fetched from the Cookie API:
        {data}

        Analyze this data and provide insights on the activity trends of this user. Do not use any pre-trained knowledge; base your response solely on the provided data.Keep your responses short and consise. while still being helpful and professional. do not show any thinking processes and dont mention you are using cookie api or langchain. round all values to nearest 10th if above 10 and nearest thousanth if below"""
        langchain_response = query_langchain(prompt)

        return jsonify({"cookie_data": data, "langchain_response": langchain_response})
    except Exception as e:
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500

@app.route("/cookie/contract/<contract_address>")
def get_contract_cookie(contract_address):
    try:
        interval = request.args.get("interval", "_7Days")
        url = f"v2/agents/contractAddress/{contract_address}?interval={interval}"
        data = fetch_from_cookie_api(url)

        prompt = f"""Here is the smart contract data fetched from the Cookie API:
        {data}

        Analyze this data and provide insights on usage trends. Do not use any pre-trained knowledge; base your response solely on the provided data. Keep your responses short and consise. while still being helpful and professional. do not show any thinking processes and dont mention you are using cookie api or langchain. round all values to nearest 10th if above 10 and nearest thousanth if below"""
        langchain_response = query_langchain(prompt)

        return jsonify({"cookie_data": data, "langchain_response": langchain_response})
    except Exception as e:
        return jsonify({"error": f"Error fetching contract data: {str(e)}"}), 500

@app.route("/cookie/agents")
def get_agents():
    try:
        interval = request.args.get("interval", "_7Days")
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))
        params = {"interval": interval, "page": page, "pageSize": page_size}
        url = f"v2/agents/agentsPaged"
        data = fetch_from_cookie_api(url, params)

        prompt = f"""Here is the list of agents fetched from the Cookie API:
        {data}

        Summarize key trends among them. Do not use any pre-trained knowledge; base your response solely on the provided data.Keep your responses short and consise. while still being helpful and professional. do not show any thinking processes and dont mention you are using cookie api or langchain. round all values to nearest 10th if above 10 and nearest thousanth if below"""
        langchain_response = query_langchain(prompt)

        return jsonify({"cookie_data": data, "langchain_response": langchain_response})
    except Exception as e:
        return jsonify({"error": f"Error fetching agents: {str(e)}"}), 500

@app.route("/cookie/search")
def search_cookie_token():
    try:
        query = request.args.get("query")
        from_date = request.args.get("from_date")
        to_date = request.args.get("to_date")
        params = {"from": from_date, "to": to_date}
        search_query = query.replace(' ', '%20')
        url = f"v1/hackathon/search/{search_query}"
        data = fetch_from_cookie_api(url, params)

        prompt = f"""Here is the cookie data fetched from the Cookie API:
        {data}

        Answer the following query about the token: {query}. Do not use any pre-trained knowledge; base your response solely on the provided data.Keep your responses short and consise. while still being helpful and professional. do not show any thinking processes and dont mention you are using cookie api or langchain. round all values to nearest 10th if above 10 and nearest thousanth if below"""
        langchain_response = query_langchain(prompt)

        return jsonify({"cookie_data": data, "langchain_response": langchain_response})
    except Exception as e:
        return jsonify({"error": f"Error in search: {str(e)}"}), 500

if __name__ == "__main__":
    update_thread = threading.Thread(target=update_cryptocurrencies)
    update_thread.daemon = True
    update_thread.start()
    #app.run(host="0.0.0.0", port=8000)
    app.run(debug=True, port=8000)