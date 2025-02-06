import os
import sys
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_plugins.cookie_api_plugin.cookie_api.cookie_api import fetch_from_cookie_api
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key is missing. Please add it to the .env file.")

app = FastAPI(
    title="Cookie API Plugin with LangChain",
    description="Integrating Cookie API with LangChain",
    version="1.1"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plugin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../langchain_plugins'))
sys.path.append(plugin_path)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key)

def query_langchain(prompt: str):
    try:
        response = llm.invoke(prompt)

        if hasattr(response, 'content'):
            return response.content 
        else:
            return str(response)  
    except Exception as e:
        return f"Error in LangChain query: {e}"

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Cookie API Plugin integrated with LangChain!"}

class QueryRequest(BaseModel):
    question: str

@app.get("/query")
@app.post("/query")
async def query_openai(request: Request, query_data: QueryRequest = None, question: str = None):
    try:
        if request.method == "POST":
            question = query_data.question
        elif request.method == "GET" and not question:
            raise HTTPException(status_code=400, detail="Missing 'question' parameter.")

        url = "v2/agents/agentsPaged"
        params = {"interval": "_7Days", "page": 1, "pageSize": 10}
        cookie_data = fetch_from_cookie_api(url, params)

        prompt = f"""Here is the data fetched from the Cookie API:
        {cookie_data}

        Based on this data, answer the following question: {question}

        Do not use any pre-trained knowledge; base your response solely on the provided data."""

        response = query_langchain(prompt)
        return {"openai_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying OpenAI: {str(e)}")

def generate_dynamic_prompt(data, query_type):
    if query_type == "price":
        price = data.get("price")
        return f"The current price of the token is {price}. What can you infer from this?"
    elif query_type == "volume":
        volume = data.get("volume24Hours")
        return f"The trading volume in the last 24 hours is {volume}. What insights can you gather from this?"
    elif query_type == "sentiment":
        sentiment = data.get("sentiment", "neutral")
        return f"The sentiment for this token is {sentiment}. What can you conclude from this?"
    else:
        return "Invalid query type."
    
def generate_graph_data(data, feature):
    labels = []
    data_points = []

    for item in data:
        labels.append(item.get("date", "N/A"))
        data_points.append(item.get(feature, 0))
    
    return {"labels": labels, "dataPoints": data_points}

@app.get("/cookie/twitter/{username}")
async def get_twitter_cookie(username: str, interval: str = "_7Days"):
    try:
        url = f"v2/agents/twitterUsername/{username}?interval={interval}"
        data = fetch_from_cookie_api(url)

        prompt = f"""Here is the Twitter data for {username} fetched from the Cookie API:
        {data}

        Analyze this data and provide insights on the activity trends of this user. Do not use any pre-trained knowledge; base your response solely on the provided data."""
        langchain_response = query_langchain(prompt)

        return {"cookie_data": data, "langchain_response": langchain_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/cookie/contract/{contract_address}")
async def get_contract_cookie(contract_address: str, interval: str = "_7Days"):
    try:
        url = f"v2/agents/contractAddress/{contract_address}?interval={interval}"
        data = fetch_from_cookie_api(url)

        prompt = f"""Here is the smart contract data fetched from the Cookie API:
        {data}

        Analyze this data and provide insights on usage trends. Do not use any pre-trained knowledge; base your response solely on the provided data."""
        langchain_response = query_langchain(prompt)

        return {"cookie_data": data, "langchain_response": langchain_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching contract data: {str(e)}")

@app.get("/cookie/agents")
async def get_agents(interval: str = "_7Days", page: int = 1, page_size: int = 10):
    try:
        params = {"interval": interval, "page": page, "pageSize": page_size}
        url = f"v2/agents/agentsPaged"
        data = fetch_from_cookie_api(url, params)

        prompt = f"""Here is the list of agents fetched from the Cookie API:
        {data}

        Summarize key trends among them. Do not use any pre-trained knowledge; base your response solely on the provided data."""
        langchain_response = query_langchain(prompt)

        return {"cookie_data": data, "langchain_response": langchain_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching agents: {str(e)}")

@app.get("/cookie/search")
async def search_cookie_token(query: str, from_date: str, to_date: str):
    try:
        params = {"from": from_date, "to": to_date}
        search_query = query.replace(' ', '%20')
        url = f"v1/hackathon/search/{search_query}"
        data = fetch_from_cookie_api(url, params)

        prompt = f"""Here is the cookie data fetched from the Cookie API:
        {data}

        Answer the following query about the token: {query}. Do not use any pre-trained knowledge; base your response solely on the provided data."""
        langchain_response = query_langchain(prompt)

        return {"cookie_data": data, "langchain_response": langchain_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in search: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
