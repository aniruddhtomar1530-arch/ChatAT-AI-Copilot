from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

# .env file se API key aur DB URL load karo
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

# MongoDB Connection Setup
try:
    mongo_client = MongoClient(mongo_uri,tlsCAFile=certifi.where())
    db = mongo_client["chatat_database"]      # Database ka naam
    chat_collection = db["chat_history"]      # Table (Collection) ka naam
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"🚨 MongoDB connection error: {e}")

client = genai.Client(api_key=api_key)
app = FastAPI(title="MLOps Copilot API")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "MLOps Copilot Backend is running successfully! 🚀"}

# Naya Route: Chat History nikalne ke liye
@app.get("/history")
def get_history():
    chats = []
    # Database se saari history nikalo (ID hata kar taaki error na aaye)
    for chat in chat_collection.find({}, {"_id": 0}):
        chats.append(chat)
    return {"history": chats}

@app.post("/chat")
def chat_with_bot(request: ChatRequest):
    try:
        system_prompt = """You are an expert MLOps and Hyperparameter Tuning Copilot. 
        Your job is to help users optimize Machine Learning models, write tuning code, and guide them on Docker and FastAPI deployments. 
        Always give professional, highly accurate, and industry-standard advice."""
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=request.prompt,
            config={"system_instruction": system_prompt}
        )
        
        bot_reply = response.text
        
        # 🟢 NAYA KAAM: Chat ko Database mein Save karo
        chat_data = {
            "user_message": request.prompt,
            "bot_response": bot_reply
        }
        chat_collection.insert_one(chat_data)
        
        return {"response": bot_reply}
        
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            return {"response": "⏳ AI Engine par abhi bahut traffic hai. Kripya 10-15 seconds baad dobara try karein!"}
        else:
            return {"response": f"🚨 Ek technical issue aa gaya: {error_msg}"}