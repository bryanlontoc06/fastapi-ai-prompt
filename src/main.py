import os
from fastapi import Depends, FastAPI
from dotenv import load_dotenv
from src.auth.dependencies import get_user_identifier
from src.auth.throttling import apply_rate_limit
from .ai.gemini import Gemini
from src.models import ChatRequest, ChatResponse
from .auth.dependencies import get_user_identifier
from typing import Annotated

# --- App Initialization ---
load_dotenv()
app = FastAPI()

# --- AI Configuration ---
def load_system_prompt():
    try:
        with open("src/prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)

# --- API Endpoints ---
@app.get("/")
def root():
    return {"message": "Welcome to the AI Prompt API!"}

@app.post("/chat", response_model=ChatResponse, tags=["Chat Service"], operation_id="chatWithAI")
def chat(request: ChatRequest, user_id: Annotated[str, Depends(get_user_identifier)]):
    print(f"Received chat request from user_id: {user_id}")
    apply_rate_limit(user_id)
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)
