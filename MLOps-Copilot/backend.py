import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
from fastapi.middleware.cors import CORSMiddleware 

# .env file se API key aur DB URL load karo
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")
# Backend Auth Key (Agar env me nahi hai toh default use karega)
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "my_super_secret_key") 

# Database connection fail-fast logic (Agar MONGO_URI missing hai toh turant batayega)
if not mongo_uri:
    raise ValueError("🚨 MONGO_URI environment variable missing hai. Server start nahi ho sakta!")

# MongoDB Connection Setup
try:
    mongo_client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
    db = mongo_client["chatat_database"]      # Database ka naam
    chat_collection = db["chat_history"]      # Table (Collection) ka naam
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"🚨 MongoDB connection error: {e}")

app = FastAPI(title="MLOps Copilot API")

# ==========================================
# 🛡️ SECURITY SHIELD 2: CORS PROTECTION
# ==========================================
app.add_middleware(
    CORSMiddleware,
    # Local React testing aur Render dono ko allow kar diya
    allow_origins=["https://chatat-frontend.onrender.com", "http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], # GET aur POST dono easily pass honge
    allow_headers=["*"], # Custom headers (jaise x-api-key) ko allow karne ke liye
)
# ==========================================

# Request Body ka structure (Pydantic Model)
class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "MLOps Copilot Backend is running successfully! 🚀"}

# Route: Chat History nikalne ke liye
@app.get("/history")
def get_history():
    chats = []
    # Database se saari history nikalo (ID hata kar taaki error na aaye)
    for chat in chat_collection.find({}, {"_id": 0}):
        chats.append(chat)
    return {"history": chats}

# Naya Chat Endpoint with Backend Authentication
@app.post("/chat")
def chat_endpoint(request: ChatRequest, x_api_key: str = Header(None)): 
    
    # 🛡️ NEW: Backend Auth Shield - Sirf allowed frontend hi request bhej payega
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # Pydantic model se prompt nikalna (request.get ki jagah request.prompt)
    user_prompt = request.prompt.strip()

    # ==========================================
    # 🛡️ SECURITY SHIELD 3: PROMPT INJECTION DEFENSE (Level 1)
    # ==========================================
    dangerous_words = ["ignore previous", "ignore all", "system prompt", "act as", "forget everything", "bypass"]
    if any(word in user_prompt.lower() for word in dangerous_words):
        return {"response": "🚨 Security Alert: Main sirf MLOps aur Hyper-tuning ka assistant hoon. Main is tarah ke commands follow nahi kar sakta."}

    try:
        # 🟢 NAYA GEMINI SDK SYNTAX 
        client = genai.Client(api_key=api_key) 
        
        response = client.models.generate_content(
           model='gemini-3.8-flash',
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction="Tumhara naam ChatAT hai. Tum ek highly professional MLOps aur Hyperparameter Tuning Assistant ho. Tumhara kaam sirf Machine Learning, Data Science, Deployment (Docker, FastAPI, Render), aur Python coding se related sawalon ka jawab dena hai. Agar user koi aisi baat kare jo in topics se bahar ho (jaise politics, gaane, jokes, ya tumhe kuch aur banne ko kahe), toh use politely mana kar do aur kaho ki tum sirf ML Assistant ho."
            )
        )
        
        bot_reply = response.text
        
        # Chat ko Database mein Save karo
        chat_data = {
            "user_message": user_prompt, 
            "bot_response": bot_reply
        }
        chat_collection.insert_one(chat_data)
        
        return {"response": bot_reply}
        
    except Exception as e:
        error_msg = str(e)
        print(f"Backend Error: {error_msg}") # Asli error sirf terminal/Render logs me dikhega
        
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            return {"response": "⏳ AI Engine par abhi bahut traffic hai. Kripya 10-15 seconds baad dobara try karein!"}
        else:
            # User ko actual technical error na dikhayein 
            return {"response": "🚨 Ek technical issue aa gaya hai. Kripya baad mein try karein."}