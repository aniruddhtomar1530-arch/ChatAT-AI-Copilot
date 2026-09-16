# 🤖 ChatAT: MLOps & Hyper-Tuning Copilot

> 🔴 **Live Demo is LIVE:** [Click here to try ChatAT](https://chatat-frontend.onrender.com)

An enterprise-grade, microservices-based AI Copilot designed to assist Data Scientists...
# 🤖 ChatAT: MLOps & Hyper-Tuning Copilot

An enterprise-grade, microservices-based AI Copilot designed to assist Data Scientists and Machine Learning Engineers. It provides expert guidance on Hyperparameter Tuning (using frameworks like Optuna), MLOps best practices, and Docker containerization.

## 🌟 Key Features
- **Domain Expert Persona:** Powered by Google's latest Gemini 3.6 Flash model, fine-tuned with a system prompt to act as a Senior MLOps Engineer.
- **Microservices Architecture:** Decoupled Backend (FastAPI) and Frontend (Streamlit) for maximum scalability.
- **100% Dockerized:** Containerized environments using `docker-compose` to eliminate "it works on my machine" issues.
- **Secure Configuration:** Environment variables and API keys are securely managed via `.env` files.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python 3.10
- **Frontend:** Streamlit
- **AI Engine:** Google GenAI SDK (Gemini 3.6 Flash)
- **Infrastructure:** Docker, Docker Compose

## 🚀 How to Run the Project

1. **Clone the repository** (if downloaded from GitHub).
2. **Add your API Key:** Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here