import streamlit as st
import requests
from streamlit_chat import message
from right_side import show_right_sidebar
from Styles import apply_styles
st.set_page_config(
    page_title="Women's Safety Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_BASE_URL = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("auth_mode", "login")
st.session_state.setdefault("forgot_mode", False)

# ---------------- ULTRA ATTRACTIVE STYLES ----------------
apply_styles()

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 style='text-align:center;'>👩‍⚖️ Women Safety Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#555;'>Your trusted legal & safety companion</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.subheader("Login")
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")

            # ---- SIDE BY SIDE BUTTONS ----
            col_login, col_register = st.columns(2)
            with col_login:
                if st.button("Login"):
                    res = requests.post(
                        f"{API_BASE_URL}/login",
                        json={"username": login_username, "password": login_password}
                    )
                    if res.status_code == 200:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.rerun()
                    else:
                        st.error("Invalid login details")
            with col_register:
                if st.button("Create Account"):
                    st.session_state.auth_mode = "register"
                    st.rerun()

            # ---- Forgot Password ----
            if st.button("Forgot Password?"):
                st.session_state.forgot_mode = True

            if st.session_state.forgot_mode:
                new_password = st.text_input("New Password", type="password")
                if st.button("Reset Password"):
                    res = requests.post(
                        f"{API_BASE_URL}/forgot_password",
                        json={"username": login_username, "new_password": new_password}
                    )
                    if res.status_code == 200:
                        st.success("Password updated successfully")
                        st.session_state.forgot_mode = False
                    else:
                        st.error("Reset failed")

        else:
            st.subheader("Register")
            reg_username = st.text_input("Username")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")

            # ---- SIDE BY SIDE BUTTONS (Register + Back) ----
            col_register, col_back = st.columns([1, 1])
            with col_register:
                if st.button("Register"):
                    res = requests.post(
                        f"{API_BASE_URL}/register",
                        json={
                            "username": reg_username,
                            "email": reg_email,
                            "password": reg_password
                        }
                    )
                    if res.status_code == 200:
                        st.success("Account created successfully")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error("User already exists")
            with col_back:
                if st.button("Back to Login"):
                    st.session_state.auth_mode = "login"
                    st.rerun()

# ---------------- LOGGED IN UI ----------------
else:
    with st.sidebar:
        st.markdown(f"## 👋 Hi, {st.session_state.username}")
        st.markdown("### Stay Safe. Stay Informed.")
        st.markdown("---")

        if st.button("➕ New Chat"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("### Chat History")

        try:
            response = requests.get(
                f"{API_BASE_URL}/chat_history/{st.session_state.username}"
            )
            if response.status_code == 200:
                history = response.json().get("chat_history", [])
                for chat in history:
                    with st.expander(chat["timestamp"][:19]):
                        st.write(chat["user_message"])
        except:
            pass

        st.markdown("<br><br><br><br>", unsafe_allow_html=True)

        if st.button(" Logout"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<h2> Women's Safety AI Assistant</h2>", unsafe_allow_html=True)
    left_col, right_col = st.columns([3, 1])

    API_URL = f"{API_BASE_URL}/chat"

    for i, chat in enumerate(st.session_state.messages):
        message(
            chat["content"],
            is_user=(chat["role"] == "user"),
            key=f"chat_{i}"
        )

    if st.button("📞 Emergency & Helpline Numbers"):
        res = requests.post(
            API_URL,
            json={
                "message": "Give me all women's safety helpline numbers in India",
                "user": st.session_state.username
            }
        )
        if res.status_code == 200:
            reply = res.json()["reply"]
            st.session_state.messages.append({"role": "bot", "content": reply})
            message(reply)

    user_input = st.chat_input("Ask about laws, safety, or emergencies...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)

        res = requests.post(
            API_URL,
            json={"message": user_input, "user": st.session_state.username}
        )
        if res.status_code == 200:
            reply = res.json()["reply"]
            st.session_state.messages.append({"role": "bot", "content": reply})
            message(reply)

    with right_col:
        show_right_sidebar()
