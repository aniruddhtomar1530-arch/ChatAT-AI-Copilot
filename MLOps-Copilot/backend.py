from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

# .env file se API key load karo
load_dotenv()

# Naya Gemini Client initialize karo
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("🚨 ERROR: API Key nahi mili! Kripya .env file check karein.")
else:
    print("✅ API Key successfully load ho gayi!")

client = genai.Client(api_key=api_key)

# FastAPI app initialize karo
app = FastAPI(title="MLOps Copilot API")

# Define karo ki user kis format mein data bhejega
class ChatRequest(BaseModel):
    prompt: str

# Test route
@app.get("/")
def home():
    return {"status": "MLOps Copilot Backend is running successfully! 🚀"}

# Main Chat Route
@app.post("/chat")
def chat_with_bot(request: ChatRequest):
    try:
        # Bot ko uski Identity (Role) batana
        system_prompt = """You are an expert MLOps and Hyperparameter Tuning Copilot. 
        Your job is to help users optimize Machine Learning models, write tuning code, and guide them on Docker and FastAPI deployments. 
        Always give professional, highly accurate, and industry-standard advice."""
        
        # Naye SDK se AI ko call karo (with System Instruction)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=request.prompt,
            config={"system_instruction": system_prompt}
        )
        return {"response": response.text}
        
    except Exception as e:
        error_msg = str(e)
        # Google ke traffic jam ko pyar se handle karna
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            return {"response": "⏳ AI Engine par abhi bahut traffic hai. Kripya 10-15 seconds baad dobara try karein!"}
        else:
            return {"response": f"🚨 Ek technical issue aa gaya: {error_msg}"}