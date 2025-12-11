import streamlit as st
import requests
from streamlit_chat import message

st.set_page_config(page_title="Women's Safety Assistant", layout="centered")
st.markdown("<h2 style='text-align:left;'>🤖 Women's Safety AI Assistant</h2>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# Display all previous messages
# --------------------------
for i, chat in enumerate(st.session_state.messages):
    role = chat["role"]
    content = chat["content"]
    if role == "user":
        message(content, is_user=True, key=f"user_{i}")
    else:
        message(content, key=f"bot_{i}")

st.markdown("---")

# --------------------------
# Helpline Button (AI-powered)
# --------------------------
if st.button("Show Women's Safety Helplines 📞"):
    try:
        response = requests.post(API_URL, json={"message": "Give me all women's safety helpline numbers in India"})
        if response.status_code == 200:
            bot_reply = response.json()["reply"]
            st.session_state.messages.append({"role": "bot", "content": bot_reply})
            message(bot_reply, key=f"bot_{len(st.session_state.messages)-1}")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")

# --------------------------
# User input for chat
# --------------------------
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user_{len(st.session_state.messages)-1}")
    try:
        response = requests.post(API_URL, json={"message": user_input})
        if response.status_code == 200:
            bot_reply = response.json()["reply"]
            st.session_state.messages.append({"role": "bot", "content": bot_reply})
            message(bot_reply, key=f"bot_{len(st.session_state.messages)-1}")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")
