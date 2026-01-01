import streamlit as st
import requests
import base64
from right_side import show_right_sidebar
from Styles import apply_styles

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Women's Safety Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- APPLY STYLES ----------------
apply_styles()

API_BASE_URL = "http://127.0.0.1:8000"

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("auth_mode", "login")
st.session_state.setdefault("forgot_mode", False)
st.session_state.setdefault("selected_history", None)

# ---------------- QUERY PARAM HELPERS ----------------
def _get_qp():
    return st.query_params

def _set_qp(**kwargs):
    st.query_params.update(kwargs)

def _clear_qp():
    st.query_params.clear()

params = _get_qp()

if params.get("logged_in") == "1" and params.get("user"):
    st.session_state.logged_in = True
    st.session_state.username = params.get("user")

if params.get("history"):
    st.session_state.selected_history = params.get("history")

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        img_base64 = base64.b64encode(open("logo.png", "rb").read()).decode()

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;justify-content:center;margin:20px;">
                <img src="data:image/jpeg;base64,{img_base64}"
                     style="width:150px;height:150px;object-fit:cover;" />
                <div style="margin-left:15px;">
                    <h1 style="margin:0;">Women Safety Assistant</h1>
                    <p style="margin:0;color:#555;">
                        Your trusted legal & safety companion
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.auth_mode == "login":
            st.subheader("Login")

            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")

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
                        _set_qp(logged_in="1", user=login_username)
                        st.rerun()
                    else:
                        st.error("Invalid login details")

            with col_register:
                if st.button("Create Account"):
                    st.session_state.auth_mode = "register"
                    st.rerun()

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

# ---------------- LOGGED-IN UI ----------------
else:
    with st.sidebar:
        st.markdown(f"## 👋 Hi, {st.session_state.username}")
        st.markdown("---")

        if st.button("➕ New Chat"):
            st.session_state.messages = []
            st.session_state.selected_history = None
            _clear_qp()
            st.rerun()

        st.markdown("### Chat History")

        try:
            response = requests.get(
                f"{API_BASE_URL}/chat_history/{st.session_state.username}"
            )
            if response.status_code == 200:
                history = response.json().get("chat_history", [])

                with st.container(height=450):
                    for chat in history:
                        preview = chat["user_message"][:70]
                        if st.button(preview, key=f"chat_{chat['id']}"):
                            st.session_state.messages = [
                                {"role": "user", "content": chat["user_message"]},
                                {"role": "assistant", "content": chat["bot_reply"]}
                            ]
                            _set_qp(history=str(chat["id"]))
                            st.rerun()
        except:
            pass

        if st.button("Logout"):
            st.session_state.clear()
            _clear_qp()
            st.rerun()

    # ---------------- MAIN CHAT ----------------
    st.markdown("<h2>Women's Safety AI Assistant</h2>", unsafe_allow_html=True)

    left_col, right_col = st.columns([3, 1])
    API_URL = f"{API_BASE_URL}/chat"

    # -------- CHAT (NATIVE, BACKGROUND-BLENDED) --------
    for chat in st.session_state.messages:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    user_input = st.chat_input("Ask about laws, safety, or emergencies...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        res = requests.post(
            API_URL,
            json={"message": user_input, "user": st.session_state.username}
        )
        if res.status_code == 200:
            reply = res.json()["reply"]
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
            with st.chat_message("assistant"):
                st.markdown(reply)

    with right_col:
        show_right_sidebar()
