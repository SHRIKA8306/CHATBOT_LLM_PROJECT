import streamlit as st
import requests
from streamlit_chat import message
from right_side import show_right_sidebar

st.set_page_config(
    page_title="Women's Safety Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("auth_mode", "login")
st.session_state.setdefault("forgot_mode", False)

# ---------------- ULTRA ATTRACTIVE STYLES ----------------
st.markdown("""
<style>

/* ---------- BACKGROUND ---------- */
.stApp {
    background: linear-gradient(135deg, #fbeaff, #f7d9ff, #fce4ec);
}

/* ---------- HEADINGS ---------- */
h1, h2, h3 {
    color: #5E2B97;
    font-weight: 800;
}

/* ---------- GLASS CARD ---------- */
.glass-card {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 20px 40px rgba(94, 43, 151, 0.25);
}

/* ---------- INPUT ---------- */
.stTextInput input {
    border-radius: 18px !important;
    height: 48px !important;
    border: none !important;
    padding-left: 15px !important;
    box-shadow: inset 0 0 0 1px #d6b4f0;
}

/* ---------- BUTTON ---------- */
.stButton button {
    background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
    color: white !important;
    border-radius: 30px !important;
    height: 50px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 10px 25px rgba(232, 74, 159, 0.45);
    transition: 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.04);
    box-shadow: 0 15px 35px rgba(232, 74, 159, 0.65);
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #5E2B97, #8E44AD);
    color: white;
}

[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] p {
    color: white;
}

/* ---------- CHAT INPUT ---------- */
.stChatInput textarea {
    border-radius: 20px !important;
    padding: 15px !important;
    border: 2px solid #e4c6ff !important;
}

/* ---------- EXPANDER ---------- */
.st-expander {
    background: white !important;
    border-radius: 15px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>👩‍⚖️ Women Safety Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#555;'>Your trusted legal & safety companion</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.subheader("Login")
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")

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

            if st.button("Create Account"):
                st.session_state.auth_mode = "register"
                st.rerun()

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

            if st.button("Back to Login"):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- LOGGED IN UI ----------------
else:
    with st.sidebar:
        st.markdown(f"## 👋 Hi, {st.session_state.username}")
        st.markdown("### Stay Safe. Stay Informed.")
        st.markdown("---")

        if st.button("➕ New Chat"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("### 🕘 Chat History")

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

        st.markdown("<br><br><br>", unsafe_allow_html=True)

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<h2>💬 Women's Safety AI Assistant</h2>", unsafe_allow_html=True)
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
