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
st.session_state.setdefault("display_name", "")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("auth_mode", "login")
st.session_state.setdefault("forgot_mode", False)
st.session_state.setdefault("selected_history", None)
st.session_state.setdefault("editing", None)
st.session_state.setdefault("edit_text", "")
st.session_state.setdefault("chat_id", None)  # Track current chat thread ID for continuation
st.session_state.setdefault("renaming_chat", None)
st.session_state.setdefault("rename_text", "")

apply_styles()

# ---------------- GOOGLE LOGIN CHECK (NEW - FIXED) ----------------
def _format_display_name(raw: str) -> str:
    if not raw:
        return ""
    # If an email was provided, use the local part
    if "@" in raw:
        raw = raw.split("@")[0]
    # If name contains spaces (e.g., 'Suja Khatri'), take first name and last initial
    parts = raw.split()
    if len(parts) >= 2:
        first = parts[0]
        last_initial = parts[-1][0]
        return f"{first.lower()} {last_initial.lower()}"
    # If local part uses separators like '.' or '_', split and use first and last initial
    for sep in (".", "_"):
        if sep in raw:
            parts = raw.split(sep)
            if len(parts) >= 2:
                return f"{parts[0].lower()} {parts[-1][0].lower()}"
    # Otherwise return the single token lowercased
    return raw.lower()
# Query-param helpers (define before use)
def _get_qp():
    return st.query_params

def _set_qp(**kwargs):
    st.query_params.update(kwargs)

def _clear_qp():
    st.query_params.clear()


def _qp_first(key: str):
    """Return the first value for a query-param key (Streamlit may store lists)."""
    v = st.query_params.get(key)
    if isinstance(v, list) and v:
        return v[0]
    return v


if _qp_first("google_login") == "1":
    google_user = _qp_first("user")
    google_name = _qp_first("name")
    if google_user:
        st.session_state.logged_in = True
        # keep username as email for backend/chat storage
        st.session_state.username = google_user
        # store a friendly display name for UI
        st.session_state.display_name = _format_display_name(google_name or google_user)
        _clear_qp()
        st.success(f"✅ Google login successful! Welcome {st.session_state.display_name}!")
        st.rerun()

# ---------------- QUERY PARAMS ----------------

# Restore login from query params (BOTH username/password + Google)
params = _get_qp()
if _qp_first("logged_in") == "1" and _qp_first("user"):
    st.session_state.logged_in = True
    st.session_state.username = _qp_first("user")
    # restore display name if provided or derive from username
    st.session_state.display_name = _format_display_name(_qp_first("name") or _qp_first("user"))

if _qp_first("history"):
    st.session_state.selected_history = _qp_first("history")

# ---------------- HELPERS ----------------
def render_chat_from_history():
    for i, chat in enumerate(st.session_state.messages):
        role = "user" if chat["role"] == "user" else "assistant"
        avatar = "🧑" if role == "user" else "🛡️"

        with st.chat_message(role, avatar=avatar):

            # ---------- EDIT MODE ----------
            if role == "user" and st.session_state.get("editing") == i:
                edited = st.text_area(
                    "",
                    value=st.session_state.edit_text or chat.get("content", ""),
                    key=f"inline_edit_{i}",
                    height=100,
                    label_visibility="collapsed"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save", key=f"save_{i}", use_container_width=True):
                        st.session_state.messages[i]["content"] = edited
                        st.session_state.messages = st.session_state.messages[: i + 1]
                        # Call API again with edited message
                        reply = api_chat(edited)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        st.session_state.editing = None
                        st.session_state.edit_text = ""
                        st.rerun()

                with col2:
                    if st.button("Cancel", key=f"cancel_{i}", use_container_width=True):
                        st.session_state.editing = None
                        st.session_state.edit_text = ""
                        st.rerun()

            # ---------- NORMAL MODE ----------
            else:
                st.markdown(chat.get("content", ""))

                # Edit icon inside bubble (right aligned)
                if role == "user":
                    edit_col = st.columns([8, 1])[1]
                    with edit_col:
                        if st.button("✎", key=f"edit_{i}", help="Edit message"):
                            st.session_state.editing = i
                            st.session_state.edit_text = chat.get("content", "")
                            st.rerun()

          
def api_chat(prompt: str) -> str:
    data = {"message": prompt, "user": st.session_state.username}
    if st.session_state.chat_id:
        data["chat_id"] = st.session_state.chat_id  # Include chat_id if continuing a thread
    res = requests.post(API_URL, json=data)
    if res.status_code == 200:
        response_data = res.json()
        # Update chat_id if it's a new thread
        if not st.session_state.chat_id:
            st.session_state.chat_id = response_data.get("chat_id")
        return response_data.get("reply", "")
    return "Server error. Please try again."

def load_history_chat(history_id: str, history_list: list):
    for thread in history_list:
        if str(thread.get("id")) == str(history_id):
            st.session_state.messages = [
                {"role": msg["role"], "content": msg["content"]} for msg in thread.get("messages", [])
            ]
            st.session_state.selected_history = thread.get("id")
            st.session_state.chat_id = thread.get("id")  # Set chat_id for continuation
            return

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # -------- HEADER --------
        img_base64 = base64.b64encode(open("logo.png", "rb").read()).decode()
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

        # -------- GOOGLE LOGIN BUTTON (NEW - FIXED) --------
        if st.button("🔐 Login with Google", use_container_width=True, type="primary"):
            try:
                res = requests.get(f"{API_BASE_URL}/auth/google")
                if res.status_code == 200:
                    auth_url = res.json()["auth_url"]
                    st.markdown(f'[Click here to continue Google login]({auth_url})')

                else:
                    st.error("Backend error - check if backend is running on port 8000")
            except:
                st.error("Backend not running. Start with: `uvicorn backend:app --host 127.0.0.1 --port 8000`")

        st.markdown("---")
        st.caption("OR use username/password:")

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
                        data = res.json()
                        email = data.get("email") or login_username
                        st.session_state.logged_in = True
                        # Use email as canonical username so chat history is shared
                        st.session_state.username = email
                        # Show the literal username entered when logging in via username/password
                        # If the user entered a username (not an email), prefer that for display.
                        if login_username and "@" not in login_username:
                            st.session_state.display_name = login_username
                        else:
                            st.session_state.display_name = _format_display_name(email)
                        st.session_state.selected_history = None
                        _set_qp(logged_in="1", user=email, name=st.session_state.display_name)
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

        # -------- REGISTER --------
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
    # Ensure query params are set for persistence
    _set_qp(logged_in="1", user=st.session_state.username, name=st.session_state.display_name)
    if st.session_state.selected_history:
        _set_qp(history=str(st.session_state.selected_history))

    with st.sidebar:
        display = st.session_state.display_name or _format_display_name(st.session_state.username)
        st.markdown(f"<h2 style='font-weight:600; font-size:30px'>Hi {display}</h2>", unsafe_allow_html=True)
        if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.messages = []
            st.session_state.selected_history = None
            st.session_state.chat_id = None  # Reset chat_id
            st.query_params.pop("history", None)
            st.rerun()
            st.markdown("### Chat History")

        try:
            response = requests.get(f"{API_BASE_URL}/chat_history/{st.session_state.username}")
            if response.status_code == 200:
                history = response.json().get("chat_history", [])

                hist = _qp_first("history")
                if hist:
                    load_history_chat(str(hist), history)

                with st.container(height=450):
                    for thread in history:
                        chat_id = thread["id"]
                        title = thread.get("title", "Untitled Chat")

                        row = st.columns([8, 1])

                        # --- Chat select ---
                        with row[0]:
                            if st.button(title, key=f"chat_{chat_id}", use_container_width=True):
                                st.session_state.selected_history = chat_id
                                st.session_state.chat_id = chat_id
                                st.session_state.messages = [
                                    {"role": msg["role"], "content": msg["content"]}
                                    for msg in thread.get("messages", [])
                                ]
                                _set_qp(history=str(chat_id))
                                st.rerun()

                        # --- 3 dots menu ---
                        with row[1]:
                            with st.popover("⋮"):
                                if st.button("🔗 Share", key=f"share_{chat_id}", use_container_width=True):
                                    share_link = f"http://localhost:8501/?history={chat_id}"
                                    st.info(f"Share link:\n{share_link}")

                                if st.button("✏️ Rename", key=f"rename_btn_{chat_id}", use_container_width=True):
                                    st.session_state.renaming_chat = chat_id
                                    st.session_state.rename_text = title
                                    st.rerun()

                                if st.button("🗑️ Delete", key=f"delete_{chat_id}", use_container_width=True):
                                    requests.delete(f"{API_BASE_URL}/delete_chat/{chat_id}")
                                    st.rerun()

                        # --- Rename UI ---
                        if st.session_state.renaming_chat == chat_id:
                            new_title = st.text_input(
                                "Rename chat",
                                value=st.session_state.rename_text,
                                key=f"rename_input_{chat_id}"
                            )

                            c1, c2 = st.columns(2)
                            with c1:
                                if st.button("Save", key=f"save_{chat_id}", use_container_width=True):
                                    requests.put(
                                        f"{API_BASE_URL}/rename_chat/{chat_id}",
                                        json={"title": new_title}
                                    )
                                    st.session_state.renaming_chat = None
                                    st.rerun()

                            with c2:
                                if st.button("Cancel", key=f"cancel_{chat_id}", use_container_width=True):
                                    st.session_state.renaming_chat = None
                                    st.rerun()

        except Exception as e:
            st.error(f"History load failed: {e}")

        # Logout outside loop
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            st.session_state.clear()
            _clear_qp()
            st.rerun()


        

    top_l, top_r = st.columns([4, 2], vertical_alignment="center")
    with top_l:
        st.markdown("## Women's Safety AI Assistant")
        st.caption("Ask about laws, safety tips, emergencies, and immediate help.")

    with top_r:
        c1, c2 = st.columns(2)

        with c2:
            if st.button("Emergency", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Emergency & helpline numbers"})
                reply = api_chat("Give me all women's safety helpline numbers in India")
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    body_l, body_r = st.columns([3, 1], gap="large")
    with body_l:
        render_chat_from_history()
    with body_r:
        show_right_sidebar()

    # (Inline editing is handled inside render_chat_from_history)

    user_input = st.chat_input("Ask about laws, safety, or emergencies...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        reply = api_chat(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()