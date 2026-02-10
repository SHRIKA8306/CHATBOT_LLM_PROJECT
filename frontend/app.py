import streamlit as st
import requests
from Styles import apply_styles
import pyperclip

def copy_to_clipboard(text: str):
    pyperclip.copy(text)

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
st.session_state.setdefault("chat_id", None)
st.session_state.setdefault("renaming_chat", None)
st.session_state.setdefault("rename_text", "")


# ---------------- GOOGLE LOGIN CHECK ----------------
def _format_display_name(raw: str) -> str:
    if not raw:
        return ""
    if "@" in raw:
        raw = raw.split("@")[0]
    parts = raw.split()
    if len(parts) >= 2:
        first = parts[0]
        last_initial = parts[-1][0]
        return f"{first.lower()} {last_initial.lower()}"
    for sep in (".", "_"):
        if sep in raw:
            parts = raw.split(sep)
            if len(parts) >= 2:
                return f"{parts[0].lower()} {parts[-1][0].lower()}"
    return raw.lower()

def _get_qp():
    return st.query_params

def _set_qp(**kwargs):
    st.query_params.update(kwargs)

def _clear_qp():
    st.query_params.clear()

def _qp_first(key: str):
    v = st.query_params.get(key)
    if isinstance(v, list) and v:
        return v[0]
    return v

if _qp_first("google_login") == "1":
    google_user = _qp_first("user")
    google_name = _qp_first("name")
    if google_user:
        st.session_state.logged_in = True
        st.session_state.username = google_user
        st.session_state.display_name = _format_display_name(google_name or google_user)
        _clear_qp()
        st.success(f"✅ Google login successful! Welcome {st.session_state.display_name}!")
        st.rerun()

params = _get_qp()
if _qp_first("logged_in") == "1" and _qp_first("user"):
    st.session_state.logged_in = True
    st.session_state.username = _qp_first("user")
    st.session_state.display_name = _format_display_name(_qp_first("name") or _qp_first("user"))

if _qp_first("history"):
    st.session_state.selected_history = _qp_first("history")

st.session_state.setdefault("sources", {})

# Apply styles AFTER login state is determined
apply_styles()

# ---------------- HELPERS ----------------
def render_chat_from_history():
    for i, chat in enumerate(st.session_state.messages):
        role = "user" if chat["role"] == "user" else "assistant"
        avatar = "🧑" if role == "user" else "🛡️"

        with st.chat_message(role, avatar=avatar):

            # ---------- EDIT MODE ----------
            if role == "user" and st.session_state.get("editing") == i:
                edited = st.text_area(
                    "Edit message",
                    value=st.session_state.edit_text or chat.get("content", ""),
                    key=f"inline_edit_{i}",
                    height=100,
                    label_visibility="collapsed"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save", key=f"save_{i}", use_container_width=True):
                        # Keep ONLY messages that come BEFORE the message being edited
                        st.session_state.messages = st.session_state.messages[:i]
                        
                        # Clear ALL sources from this point onwards
                        st.session_state.sources = {k: v for k, v in st.session_state.sources.items() if k < i}
    
                        st.session_state.editing = None
                        st.session_state.edit_text = ""
                        
                        # Add the edited message
                        st.session_state.messages.append({"role": "user", "content": edited})
                        
                        # Clear old messages from backend (if chat exists)
                        if st.session_state.chat_id:
                            try:
                                requests.delete(f"{API_BASE_URL}/clear_messages_after/{st.session_state.chat_id}/{i}")
                            except:
                                pass  # Continue even if deletion fails
                        
                        # Get new response
                        with st.spinner("🛡️ Generating response..."):
                            reply, sources = api_chat(edited)
                            st.session_state.messages.append({"role": "assistant", "content": reply})
                            # Store sources at the new assistant message index
                            st.session_state.sources[len(st.session_state.messages) - 1] = sources
                        st.rerun()

                with col2:
                    if st.button("Cancel", key=f"cancel_{i}", use_container_width=True):
                        st.session_state.editing = None
                        st.session_state.edit_text = ""
                        st.rerun()

           # ---------- NORMAL MODE ----------
            else:
                st.markdown(chat.get("content", ""))
                if role == "user":
                    with st.container():
                        spacer, col_copy, col_edit = st.columns([10, 1, 1])
                        with col_copy:
                            if st.button("❐", key=f"copy_{i}", help="Copy message"):
                                copy_to_clipboard(chat.get("content", ""))
                                st.toast("Copied to clipboard!")
                        with col_edit:
                            if st.button("✎", key=f"edit_{i}", help="Edit message"):
                                st.session_state.editing = i
                                st.session_state.edit_text = chat.get("content", "")
                                st.rerun()
                elif role == "assistant":
                    with st.container():
                        spacer, col_copy = st.columns([10, 1])
                        with col_copy:
                            if st.button("❐", key=f"copy_{i}", help="Copy message"):
                               copy_to_clipboard(chat.get("content", ""))
                               st.toast("Copied to clipboard!")
   
def api_chat(prompt: str):
    data = {"message": prompt, "user": st.session_state.username}
    if st.session_state.chat_id:
        data["chat_id"] = st.session_state.chat_id
    res = requests.post(API_URL, json=data)
    if res.status_code == 200:
        response_data = res.json()
        if not st.session_state.chat_id:
            st.session_state.chat_id = response_data.get("chat_id")
        sources = response_data.get("sources", [])
        return response_data.get("reply", ""), sources
    return "Server error. Please try again.", []

def load_history_chat(history_id: str, history_list: list):
    for thread in history_list:
        if str(thread.get("id")) == str(history_id):
            st.session_state.messages = [
                {"role": msg["role"], "content": msg["content"]} for msg in thread.get("messages", [])
            ]
            st.session_state.selected_history = thread.get("id")
            st.session_state.chat_id = thread.get("id")
            return

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    # Use columns to center the content - styling will target the middle column
    dl, dc, dr = st.columns([1, 1.2, 1]) 
    
    with dc:
        # Marker for finding this column in CSS
        st.markdown('<div class="login-box-marker"></div>', unsafe_allow_html=True)
        
        # 1. Header (Centered Text Only)
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <div class="login-header">Women Safety Assistant</div>
                <div style="font-size: 15px; color: #666; line-height: 1.2;">Your trusted legal & safety companion</div>
            </div>
            """, unsafe_allow_html=True
        )

        # 2. Section Title "Login"
        if st.session_state.auth_mode == "login":
            # Removed redundant Login header if using the side-by-side header
            
            # 3. Inputs
            l_user = st.text_input("Username", key="l_user", placeholder="")
            l_pass = st.text_input("Password", type="password", key="l_pass", placeholder="")
            
            # 4. Action Row: [Login] [Create Account]
            col_btn1, col_btn2 = st.columns(2, vertical_alignment="bottom")
            
            with col_btn1:
                if st.button("Login", use_container_width=True):
                     res = requests.post(f"{API_BASE_URL}/login", json={"username": l_user, "password": l_pass})
                     if res.status_code == 200:
                        data = res.json()
                        email = data.get("email") or l_user
                        st.session_state.logged_in = True
                        st.session_state.username = email
                        st.session_state.display_name = l_user if "@" not in l_user else _format_display_name(email)
                        st.session_state.selected_history = None
                        _set_qp(logged_in="1", user=email, name=st.session_state.display_name)
                        st.rerun()
                     else:
                        st.error("Invalid credentials")

            with col_btn2:
                if st.button("Create Account", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()
            
            # 5. Forgot Password (Full width below buttons)
            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.forgot_mode = True
                st.rerun()

            st.markdown('<div style="font-size: 18px; font-weight: 500; color: black; text-align:center; margin-top: 0rem; margin-bottom: 0rem;">Or</div>', unsafe_allow_html=True)
            
            # 6. Google Login (Full Width at bottom)
            st.markdown('<div class="google-btn-container">', unsafe_allow_html=True)
            if st.button("Login with Google", use_container_width=True, key="google_login_main"):
                try:
                    res = requests.get(f"{API_BASE_URL}/auth/google")
                    if res.status_code == 200:
                        auth_url = res.json()["auth_url"]
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
                    else:
                        st.error("Connection error")
                except:
                    st.error("Backend not running")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Forgot Password Handling
            if st.session_state.forgot_mode:
                st.markdown('<div style="font-size: 20px; font-weight: 700; color: black; margin-top: 1rem; margin-bottom: 0.5rem;">Reset Password</div>', unsafe_allow_html=True)
                f_user = st.text_input("Username for Reset", key="f_user")
                f_new = st.text_input("New Password", type="password", key="f_new")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button("Update Password", use_container_width=True):
                        requests.post(f"{API_BASE_URL}/forgot_password", json={"username": f_user, "new_password": f_new})
                        st.success("Password updated!")
                        st.session_state.forgot_mode = False
                        st.rerun()
                with col2:
                    if st.button("Cancel", use_container_width=True, key="cancel_reset"): 
                        st.session_state.forgot_mode = False
                        st.rerun()

        # --- REGISTER MODE ---
        else:
            st.markdown('<div style="font-size: 20px; font-weight: 700; color: black; margin-bottom: 15px;">Create Account</div>', unsafe_allow_html=True)
            r_user = st.text_input("Username", key="r_user")
            r_email = st.text_input("Email", key="r_email")
            r_pass = st.text_input("Password", type="password", key="r_pass")
            
            st.write("")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                 if st.button("Register", use_container_width=True):
                     res = requests.post(f"{API_BASE_URL}/register", json={"username": r_user, "email": r_email, "password": r_pass})
                     if res.status_code == 200:
                         st.success("Created! Please login.")
                         st.session_state.auth_mode = "login"
                         st.rerun()
                     else:
                         st.error("Failed")
            with col_r2:
                 if st.button("Back to Login", use_container_width=True):
                     st.session_state.auth_mode = "login"
                     st.rerun()

# ---------------- LOGGED IN UI ----------------
else:
    _set_qp(logged_in="1", user=st.session_state.username, name=st.session_state.display_name)
    if st.session_state.selected_history:
        _set_qp(history=str(st.session_state.selected_history))

    with st.sidebar:
        display = st.session_state.display_name or _format_display_name(st.session_state.username)
        st.markdown(f"<h1 style='font-weight:700; font-size:30px';margin-top:0;>Hi {display}</h1>", unsafe_allow_html=True)
        if st.button(" New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.messages = []
            st.session_state.selected_history = None
            st.session_state.chat_id = None
            st.query_params.pop("history", None)
            st.rerun()
        
        st.markdown("<h3 style='font-weight:400; font-size:16px; color:#666;'>Your chats </h3>", unsafe_allow_html=True)

        try:
            response = requests.get(f"{API_BASE_URL}/chat_history/{st.session_state.username}")
            if response.status_code == 200:
                history = response.json().get("chat_history", [])

                hist = _qp_first("history")
                if hist:
                    load_history_chat(str(hist), history)

                with st.container(height=405):
                    for thread in history:
                        chat_id = thread["id"]
                        title = thread.get("title", "Untitled Chat")

                        row = st.columns([9, 1])

                        with row[0]:
                            is_active = (chat_id == st.session_state.selected_history)
                            if is_active:
                                st.markdown('<div class="sidebar-active-chat">', unsafe_allow_html=True)
                            
                            if st.button(title, key=f"chat_{chat_id}", use_container_width=True):
                                st.session_state.selected_history = chat_id
                                st.session_state.chat_id = chat_id
                                st.session_state.messages = [
                                    {"role": msg["role"], "content": msg["content"]}
                                    for msg in thread.get("messages", [])
                                ]
                                _set_qp(history=str(chat_id))
                                st.rerun()

                        with row[1]:
                            with st.popover("⋮"):
                                # Top Section
                                if st.button("Share", key=f"share_{chat_id}", use_container_width=True):
                                    share_link = f"http://localhost:8501/?history={chat_id}"
                                    st.info(f"Share link:\n{share_link}")
                                
                                if st.button("Rename", key=f"rename_btn_{chat_id}", use_container_width=True):
                                    st.session_state.renaming_chat = chat_id
                                    st.session_state.rename_text = title
                                    st.rerun()
                                
                                # Bottom Section
                                if st.button(" Delete", key=f"delete_{chat_id}", use_container_width=True):
                                    requests.delete(f"{API_BASE_URL}/delete_chat/{chat_id}")
                                    st.rerun()

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
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            st.session_state.clear()
            _clear_qp()
            st.rerun()

    # Header Area - Compact
    h_col1, h_col2 = st.columns([4, 1])
    with h_col1:
        st.markdown("<h1 style= 'color:#4c1d95'>Women's Safety AI Assistant</h1>", unsafe_allow_html=True)
    with h_col2:
        st.markdown('<div class="gradient-button-wrapper">', unsafe_allow_html=True)
        if st.button("Emergency", use_container_width=True, key="header_emergency"):
            st.session_state.messages.append({"role": "user", "content": "Emergency & helpline numbers"})
            reply, sources = api_chat("Give me all women's safety helpline numbers in India")
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.sources[len(st.session_state.messages)-1] = sources
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("") # Spacer

    body_l, body_r = st.columns([3, 1], gap="large")
    with body_l:
        if not st.session_state.messages:
            # Centered Welcome Screen for Empty Chat
            st.markdown(
                """
                    <h2 style='text-align:center;'>How can I help you today?</h2>
                    <p style='text-align:center'>Ask about laws, safety tips, or find immediate help.</p>
                """, unsafe_allow_html=True
            )
        else:
            render_chat_from_history()

    # Disable chat input while editing
    chat_disabled = st.session_state.get("editing") is not None
    
    if not chat_disabled:
        user_input = st.chat_input(
            "Ask about laws, safety, or emergencies...",
            disabled=False
        )

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("🛡️ Generating response..."):
                reply, sources = api_chat(user_input)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.sources[len(st.session_state.messages)-1] = sources
            st.rerun()