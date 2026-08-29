from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from guardrails import handle_query_guardrails
from rag_pipeline import generate_answer

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mutual Fund FAQ API")

# Configure CORS
# In production, you might want to restrict this to your actual Vercel domain.
# For ease of deployment out of the box, we allow all origins.
frontend_url = os.environ.get("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url] if frontend_url != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    error: bool = False

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received query: {request.query}")
    
    # 1. Check API Key configuration
    if "GROQ_API_KEY" not in os.environ or os.environ["GROQ_API_KEY"] == "your_groq_api_key_here":
        return ChatResponse(
            response="⚠️ **Configuration Error**: `GROQ_API_KEY` is not set in the `.env` file or environment variables. Please configure it.",
            error=True
        )
    
    # 2. Check Guardrails
    refusal = handle_query_guardrails(request.query)
    if refusal:
        return ChatResponse(response=refusal)
    
    # 3. Generate Answer
    try:
        response_text = generate_answer(request.query)
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return ChatResponse(response=f"An error occurred: {str(e)}", error=True)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Mutual Fund FAQ Backend"}
