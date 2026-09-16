import streamlit as st
import requests

# Page ka title aur icon set karna
st.set_page_config(page_title="ChatAT", page_icon="🤖")

st.title("🤖 ChatAT: MLOps & Hyper-Tuning Copilot")
st.markdown("Welcome! Main tumhara AI Assistant hoon. Mujhse ML models tune karne ya Docker se related kuch bhi pucho.")

# Chat history ko memory mein save rakhne ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

# Puraani chat history screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Naya message type karne ka box
prompt = st.chat_input("Apna ML ya deployment question yahan type karo...")

if prompt:
    # User ka message screen par dikhao
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Message ko memory mein save karo
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Backend API ko call lagao
    try:
        # FastAPI server ko request bhej rahe hain
        response = requests.post("http://backend:8000/chat", json={"prompt": prompt})
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
        
    # Reply ko memory mein save karo
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})