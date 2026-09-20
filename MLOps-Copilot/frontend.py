import streamlit as st
import requests
from gtts import gTTS
import os
from streamlit_mic_recorder import speech_to_text

# Backend URL ko ek variable mein rakh lete hain taaki baar-baar na likhna pade
BACKEND_URL = "https://chatat-ai-copilot.onrender.com"

# Page ka title aur icon set karna
st.set_page_config(page_title="ChatAT", page_icon="🤖")

st.title("🤖 ChatAT: MLOps & Hyper-Tuning Copilot")
st.markdown("Welcome! Main tumhara AI Assistant hoon. Mujhse ML models tune karne ya Docker se related kuch bhi pucho.")

# Chat history ko memory aur Database se load karna
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    try:
        history_response = requests.get(f"{BACKEND_URL}/history")
        if history_response.status_code == 200:
            history_data = history_response.json().get("history", [])
            
            for chat in history_data:
                st.session_state.messages.append({"role": "user", "content": chat["user_message"]})
                st.session_state.messages.append({"role": "assistant", "content": chat["bot_response"]})
    except Exception as e:
        st.warning("⚠️ Backend se purani chats load nahi ho payin.")

# Puraani chat history screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# 🟢 NAYA KAAM: Mic aur Type karne dono ka option add kiya
# ---------------------------------------------------------
st.markdown("🎤 **Bol kar sawaal poochne ke liye Mic dabayein:**")
# Mic button jisse user bol sake
spoken_text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

# Naya message type karne ka box
typed_text = st.chat_input("Apna ML ya deployment question yahan type karo...")

# Dono mein se jo bhi input aaye (type kiya hua ya bola hua), usko prompt maan lo
prompt = typed_text or spoken_text

if prompt:
    # User ka message screen par dikhao
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Message ko memory mein save karo
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Backend API ko call lagao
    try:
        response = requests.post(f"{BACKEND_URL}/chat", json={"prompt": prompt})
        response_data = response.json()
        
        if "response" in response_data:
            bot_reply = response_data["response"]
        else:
            bot_reply = f"❌ Error: {response_data.get('error', 'Kuch galat ho gaya.')}"
            
    except requests.exceptions.ConnectionError:
        bot_reply = "❌ Backend se connect nahi ho pa raha hai. Kya FastAPI server chal raha hai?"

    # Bot ka reply screen par dikhao
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
        try:
            # lang='hi' ka matlab Hindi/Hinglish accent
            tts = gTTS(text=bot_reply, lang='hi') 
            tts.save("bot_voice.mp3")
            
            # Streamlit mein audio play karne ka widget
            audio_file = open("bot_voice.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        except Exception as e:
            pass # Agar audio mein koi dikkat aaye toh chat break na ho
        
    # Reply ko memory mein save karo
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})