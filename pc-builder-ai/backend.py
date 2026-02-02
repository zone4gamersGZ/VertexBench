from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are a professional PC building assistant.
You help users understand PC components, compatibility,
performance, budgets, and recommend the best parts.
"""

@app.post("/chat")
def chat(query: UserQuery):
    print("✅ Backend received request:", query.message)

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": SYSTEM_PROMPT + "\nUser: " + query.message,
            "stream": False,
            "options": {
                "num_predict": 150
            }
        },
        timeout=120
    )

    data = r.json()
    print("📦 Ollama raw response:", data)

    if "response" not in data:
        return {
            "reply": "⚠️ AI did not generate a response. Please try a shorter or simpler question."
        }

    return {"reply": data["response"]}
