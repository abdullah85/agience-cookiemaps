from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

load_dotenv()

app = FastAPI(title="Chat with LLM", description="Chatbot using OpenAI via LangChain", version="1.0")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("⚠️ OpenAI API key is missing. Please add it to the .env file.")

def query_langchain(prompt):
    """Query OpenAI's LLM via LangChain."""
    try:
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)
        response = llm(prompt)
        return response
    except Exception as e:
        return f"Error in LangChain query: {e}"
@app.get("/")
async def read_root():
    return {"message": "Welcome to the LLM Chat API!"}

@app.post("/chat/")
async def chat_with_llm(prompt: str):
    """Chat with the LLM by sending a prompt."""
    try:
        response = query_langchain(prompt)
        return {"response": response}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)