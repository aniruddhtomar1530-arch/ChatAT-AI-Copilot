import streamlit as st
import requests

# Backend URL ko ek variable mein rakh lete hain taaki baar-baar na likhna pade
BACKEND_URL = "https://chatat-ai-copilot.onrender.com"

# Page ka title aur icon set karna
st.set_page_config(page_title="ChatAT", page_icon="🤖")

st.title("🤖 ChatAT: MLOps & Hyper-Tuning Copilot")
st.markdown("Welcome! Main tumhara AI Assistant hoon. Mujhse ML models tune karne ya Docker se related kuch bhi pucho.")

# Chat history ko memory aur Database se load karna
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # 🟢 NAYA KAAM: Backend se purani history mangwana
    try:
        history_response = requests.get(f"{BACKEND_URL}/history")
        if history_response.status_code == 200:
            history_data = history_response.json().get("history", [])
            
            # Database ke messages ko Streamlit format mein set karna
            for chat in history_data:
                st.session_state.messages.append({"role": "user", "content": chat["user_message"]})
                st.session_state.messages.append({"role": "assistant", "content": chat["bot_response"]})
    except Exception as e:
        st.warning("⚠️ Backend se purani chats load nahi ho payin.")

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
        # Naye BACKEND_URL variable ka use kar rahe hain
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
        
    # Reply ko memory mein save karo
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})