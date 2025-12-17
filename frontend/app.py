import streamlit as st
import requests
from streamlit_chat import message

st.set_page_config(page_title="Women's Safety Assistant", layout="centered")

API_BASE_URL = "http://127.0.0.1:8000"

# Session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for authentication
with st.sidebar:
    st.title("Authentication")

    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                try:
                    response = requests.post(f"{API_BASE_URL}/login", json={"username": login_username, "password": login_password})
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error(response.json().get("error", "Login failed"))
                except Exception as e:
                    st.error(f"Connection Error: {e}")

        with tab2:
            st.subheader("Register")
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            if st.button("Register"):
                try:
                    response = requests.post(f"{API_BASE_URL}/register", json={"username": reg_username, "email": reg_email, "password": reg_password})
                    if response.status_code == 200:
                        st.success("Registered successfully! Please login.")
                    else:
                        st.error(response.json().get("error", "Registration failed"))
                except Exception as e:
                    st.error(f"Connection Error: {e}")
    else:
        st.write(f"Welcome: {st.session_state.username}")
        
        # Navigation tabs for logged-in users
        nav_tab1, nav_tab2 = st.tabs(["Chat", "History"])
        
        with nav_tab1:
            st.write("**Current Chat**")
        
        with nav_tab2:
            if st.button("Load Chat History"):
                try:
                    response = requests.get(f"{API_BASE_URL}/chat_history/{st.session_state.username}")
                    if response.status_code == 200:
                        history_data = response.json()
                        st.session_state.chat_history = history_data.get("chat_history", [])
                    else:
                        st.error("Failed to load chat history")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
            
            if "chat_history" in st.session_state and st.session_state.chat_history:
                st.subheader("Your Chat History")
                for chat in st.session_state.chat_history:
                    with st.expander(f"Chat {chat['id']} - {chat['timestamp'][:19] if chat['timestamp'] else 'Unknown time'}"):
                        st.write(f"**You:** {chat['user_message']}")
                        if chat['bot_reply']:
                            st.write(f"**Assistant:** {chat['bot_reply']}")
            elif "chat_history" in st.session_state:
                st.info("No chat history found.")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.messages = []
            if "chat_history" in st.session_state:
                del st.session_state.chat_history
            st.rerun()

# Main content
if st.session_state.logged_in:
    # Check if Chat tab is selected (this is a bit tricky with sidebar tabs)
    # For now, show chat by default, history is in sidebar
    
    st.markdown("<h2 style='text-align:left;'>🤖 Women's Safety AI Assistant</h2>", unsafe_allow_html=True)

    API_URL = f"{API_BASE_URL}/chat"

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
            response = requests.post(API_URL, json={"message": "Give me all women's safety helpline numbers in India", "user": st.session_state.username})
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
            response = requests.post(API_URL, json={"message": user_input, "user": st.session_state.username})
            if response.status_code == 200:
                bot_reply = response.json()["reply"]
                st.session_state.messages.append({"role": "bot", "content": bot_reply})
                message(bot_reply, key=f"bot_{len(st.session_state.messages)-1}")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
