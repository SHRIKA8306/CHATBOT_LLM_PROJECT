import streamlit as st
import requests
import base64
from right_side import show_right_sidebar
from Styles import apply_styles

st.set_page_config(
    page_title="Women's Safety Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{API_BASE_URL}/chat"

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("auth_mode", "login")
st.session_state.setdefault("forgot_mode", False)
# Track which chat history item is currently selected (keeps sidebar static)
st.session_state.setdefault("selected_history", None)

apply_styles()

# ---------------- QUERY PARAMS ----------------
def _get_qp():
    return st.query_params

def _set_qp(**kwargs):
    st.query_params.update(kwargs)

def _clear_qp():
    st.query_params.clear()

# Restore login from query params
params = _get_qp()
if params.get("logged_in") == "1" and params.get("user"):
    st.session_state.logged_in = True
    st.session_state.username = params.get("user")

if params.get("history"):
    st.session_state.selected_history = params.get("history")

# ---------------- HELPERS ----------------
def render_chat_from_history():
    for chat in st.session_state.messages:
        role = "user" if chat["role"] == "user" else "assistant"
        avatar = "🧑" if role == "user" else "🛡️"
        with st.chat_message(role, avatar=avatar, width="content"):
            st.markdown(chat["content"])

def api_chat(prompt: str) -> str:
    res = requests.post(API_URL, json={"message": prompt, "user": st.session_state.username})
    if res.status_code == 200:
        return res.json().get("reply", "")
    return "Server error. Please try again."

def load_history_chat(history_id: str, history_list: list):
    for chat in history_list:
        if str(chat.get("id")) == str(history_id):
            st.session_state.messages = [
                {"role": "user", "content": chat.get("user_message", "")},
                {"role": "assistant", "content": chat.get("bot_reply", "")},
            ]
            st.session_state.selected_history = chat.get("id")
            return

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # -------- HEADER (IMAGE + TITLE SAME LINE) --------
        img_base64 = base64.b64encode(
            open("logo.png", "rb").read()
        ).decode()

        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                margin-top:20px;
                margin-bottom:20px;
                gap:16px;
            ">
                <img src="data:image/jpeg;base64,{img_base64}"
                     style="width:150px;height:150px;object-fit:cover;border-radius:20px;" />
                <div>
                    <h1 style="margin:0;">Women Safety Assistant</h1>
                    <p style="margin:0;color:#555;">Your trusted legal & safety companion</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------- LOGIN --------
        if st.session_state.auth_mode == "login":
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            col_login, col_register = st.columns(2)

            with col_login:
                if st.button("Login", use_container_width=True):
                    res = requests.post(
                        f"{API_BASE_URL}/login",
                        json={
                            "username": login_username,
                            "password": login_password
                        }
                    )
                    if res.status_code == 200:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.selected_history = None
                        _set_qp(logged_in="1", user=login_username)
                        st.rerun()
                    else:
                        st.error("Invalid login details")

            with col_register:
                if st.button("Create Account", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()

            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.forgot_mode = True

            if st.session_state.forgot_mode:
                new_password = st.text_input("New Password", type="password", key="new_password")
                if st.button("Reset Password", use_container_width=True):
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
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")

            col_register, col_back = st.columns(2)

            with col_register:
                if st.button("Register", use_container_width=True):
                    res = requests.post(
                        f"{API_BASE_URL}/register",
                        json={"username": reg_username, "email": reg_email, "password": reg_password}
                    )
                    if res.status_code == 200:
                        st.success("Account created successfully")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error("User already exists")

            with col_back:
                if st.button("Back to Login", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()

# ---------------- LOGGED IN UI ----------------
else:
    with st.sidebar:
        st.markdown(f"## Hi, {st.session_state.username}")
        st.markdown("---")

        if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("### Chat History")

        try:
            response = requests.get(f"{API_BASE_URL}/chat_history/{st.session_state.username}")
            if response.status_code == 200:
                history = response.json().get("chat_history", [])

                if params.get("history"):
                    load_history_chat(params.get("history"), history)

                with st.container(height=450):
                    for chat in history:
                        preview = (chat.get("user_message", "").split("\n")[0])[:70]
                        if st.button(preview, key=f"chat_{chat['id']}", use_container_width=True):
                            st.session_state.selected_history = chat["id"]
                            st.session_state.messages = [
                                {"role": "user", "content": chat.get("user_message", "")},
                                {"role": "assistant", "content": chat.get("bot_reply", "")},
                            ]
                            _set_qp(history=str(chat["id"]))
                            st.rerun()
        except Exception:
            pass

        st.markdown('<div class="ws-sidebar-footer">', unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            st.session_state.clear()
            _clear_qp()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    top_l, top_r = st.columns([4, 2], vertical_alignment="center")
    with top_l:
        st.markdown("## Women's Safety AI Assistant")
        st.caption("Ask about laws, safety tips, emergencies, and immediate help.")

    with top_r:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Clear chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.selected_history = None
                _clear_qp()
                st.rerun()
        with c2:
            if st.button("Emergency", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Emergency & helpline numbers"})
                reply = api_chat("Give me all women's safety helpline numbers in India")
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    st.markdown("---")

    body_l, body_r = st.columns([3, 1], gap="large")
    with body_l:
        render_chat_from_history()
    with body_r:
        show_right_sidebar()

    user_input = st.chat_input("Ask about laws, safety, or emergencies...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        reply = api_chat(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
