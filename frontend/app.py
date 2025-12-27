import streamlit as st
import requests
from streamlit_chat import message
from right_side import show_right_sidebar

st.set_page_config(page_title="Women's Safety Assistant", layout="wide")  # wide for sidebar

API_BASE_URL = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # "login" or "register"
if "forgot_mode" not in st.session_state:
    st.session_state.forgot_mode = False

# ---------------- LOGIN / REGISTER BOX ----------------
if not st.session_state.logged_in:
    # Use columns to center the content
    col1, col2, col3 = st.columns([1, 2, 1])  # Middle column for centering

    with col2:
            st.markdown("""
            <style>
            .login-title {
                text-align:center;
                font-size:30px;
                font-weight:700;
                color:black;
                padding:10px;
            }
            .stTextInput input {
                border-radius:12px !important;
                height:45px !important;
                border:none !important;
                margin-bottom:20px !important;
            }
            .stButton button {
                width:200px !important;
                height:48px !important;
                border-radius:14px !important;
                font-size:18px !important;
                font-weight:700 !important;
                margin:5px !important;
                color:white !important;
                background:#333333 !important;  /* Light black color for buttons */
            }
            .forgot-btn {
                background: none !important;
                color: #0d3c91 !important;
                text-decoration: underline !important;
                border: none !important;
                width: auto !important;
                height: auto !important;
                font-size: 14px !important;
                font-weight: normal !important;
                margin-top: 10px !important;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="login-title">WELCOME</div>', unsafe_allow_html=True)
            if st.session_state.auth_mode == "login":
                st.subheader("Login")
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Login", key="login_btn", help="Click to login"):
                        try:
                            res = requests.post(
                                f"{API_BASE_URL}/login",
                                json={"username": login_username, "password": login_password}
                            )
                            if res.status_code == 200:
                                st.session_state.logged_in = True
                                st.session_state.username = login_username
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error(res.json().get("error", "Login failed"))
                        except Exception as e:
                            st.error(f"Connection Error: {e}")
                with col2:
                    if st.button("Register", key="register_btn", help="Switch to register"):
                        st.session_state.auth_mode = "register"
                        st.rerun()

                # Forgot password as a link-style button
                if st.button("Forgot Password?", key="forgot_btn", help="Click to reset password"):
                    st.session_state.forgot_mode = True
                    st.rerun()

                if st.session_state.forgot_mode:
                    new_password = st.text_input("Enter new password", type="password", key="new_pass")
                    if st.button("Reset Password", key="reset_btn"):
                        try:
                            res = requests.post(
                                f"{API_BASE_URL}/forgot_password",
                                json={"username": login_username, "new_password": new_password}
                            )
                            if res.status_code == 200:
                                st.success("Password reset successfully! Please login.")
                                st.session_state.forgot_mode = False
                            else:
                                st.error(res.json().get("error", "Reset failed"))
                        except Exception as e:
                            st.error(f"Connection Error: {e}")

            else:  # register mode
                st.subheader("Register")
                reg_username = st.text_input("Username", key="reg_username")
                reg_email = st.text_input("Email", key="reg_email")
                reg_password = st.text_input("Password", type="password", key="reg_password")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Register", key="register_btn", help="Click to register"):
                        try:
                            res = requests.post(
                                f"{API_BASE_URL}/register",
                                json={"username": reg_username, "email": reg_email, "password": reg_password}
                            )
                            if res.status_code == 200:
                                st.success("Registered successfully! Please login.")
                                st.session_state.auth_mode = "login"
                                st.rerun()
                            else:
                                st.error(res.json().get("error", "Registration failed or user already exists"))
                        except Exception as e:
                            st.error(f"Connection Error: {e}")
                with col2:
                    if st.button("Login", key="login_btn", help="Switch to login"):
                        st.session_state.auth_mode = "login"
                        st.rerun()
# ---------------- LOGGED-IN UI WITH SIDEBAR ----------------
else:
    # -------- Sidebar --------
    with st.sidebar:
        st.write(f"### Welcome: {st.session_state.username}")

        if st.button("➕ New Chat"):
            st.session_state.messages = []  # clear current chat
            st.rerun()

        if st.button("History"):
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
            st.session_state.auth_mode = "login"
            st.session_state.forgot_mode = False
            if "chat_history" in st.session_state:
                del st.session_state.chat_history

    # -------- Main Page --------
    st.markdown("<h2>Women's Safety AI Assistant</h2>", unsafe_allow_html=True)
    left_col, right_col = st.columns([3, 1])  # main chat | right info

    API_URL = f"{API_BASE_URL}/chat"

    for i, chat in enumerate(st.session_state.messages):
        if chat["role"] == "user":
            message(chat["content"], is_user=True, key=f"user_{i}")
        else:
            message(chat["content"], key=f"bot_{i}")


    if st.button("Show Women's Safety Helplines 📞"):
        try:
            response = requests.post(
                API_URL,
                json={"message": "Give me all women's safety helpline numbers in India", "user": st.session_state.username},
            )
            if response.status_code == 200:
                bot_reply = response.json()["reply"]
                st.session_state.messages.append({"role": "bot", "content": bot_reply})
                message(bot_reply)
        except Exception as e:
            st.error(f"Connection Error: {e}")

    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)

        try:
            response = requests.post(
                API_URL,
                json={"message": user_input, "user": st.session_state.username},
            )
            if response.status_code == 200:
                bot_reply = response.json()["reply"]
                st.session_state.messages.append({"role": "bot", "content": bot_reply})
                message(bot_reply)
        except Exception as e:
            st.error(f"Connection Error: {e}")
    with right_col:
        show_right_sidebar()
