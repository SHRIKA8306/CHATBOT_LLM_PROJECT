import streamlit as st
import requests
from streamlit_chat import message

st.set_page_config(page_title="Chatbot (FastAPI + Groq)", layout="centered")
st.markdown("<h2 style='text-align:center;'>🤖 AI Chatbot with FastAPI + MySQL + Groq</h2>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for chat in st.session_state.messages:
    role = chat["role"]
    content = chat["content"]
    if role == "user":
        message(content, is_user=True, key=f"user_{content}")
    else:
        message(content, key=f"bot_{content}")
st.markdown("---")
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    try:
        response = requests.post(API_URL, json={"message": user_input})
        if response.status_code == 200:
            bot_reply = response.json()["reply"]
            st.session_state.messages.append({"role": "bot", "content": bot_reply})
            message(bot_reply)
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")
