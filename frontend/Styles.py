import streamlit as st

def apply_styles():
    """
    Applies CSS based on the login state.
    - If NOT logged in: Apply strict Black & White theme (Login Page).
    - If logged in: Apply original Pastel theme (Chatbot Page).
    """
    if st.session_state.get("logged_in", False):
        _apply_main_styles()
    else:
        _apply_login_styles()

def _apply_login_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg-color: #FFFFFF;
            --card-bg: #FFFFFF;
            --text-main: #000000;
            --button-bg: #000000;
            --button-text: #FFFFFF;
            --input-bg: #F3F3F3;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: var(--bg-color) !important;
            font-family: 'Inter', sans-serif !important;
            color: var(--text-main) !important;
        }
        
        /* Force white background on everything in login mode */
        [data-testid="stAppViewContainer"] {
            background: #FFFFFF !important;
        }

        div[data-testid="stColumn"]:has(div.login-box-marker) {
            background-color: var(--card-bg);
            padding: 25px 40px !important; /* Slightly more compact internal padding */
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.04);
            
            /* FIXED DIMENSIONS to prevent jumping */
            min-height: 520px !important; /* Reduced to fit without scrolling */
            width: 100% !important;
            max-width: 420px !important;
            margin: 0.5rem auto 0 auto !important; /* Reduced margin-top to 0.5rem */
            
            display: flex !important;
            flex-direction: column !important;
            overflow: hidden !important;
        }
        
        div[data-testid="stColumn"]:has(div.login-box-marker) > div {
             height: 100% !important;
             justify-content: flex-start !important;
             align-items: stretch !important;
             padding-top: 0 !important; /* Pull content to top */
             margin-top: 0 !important;
        }

        /* Scoped reset for vertical blocks inside the login box to remove top gaps */
        div[data-testid="stColumn"]:has(div.login-box-marker) div[data-testid="stVerticalBlock"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        /* ADDED: Logo and Title Container - Remove top spacing */
        .logo-title-container {
            margin-top: 0 !important;
            padding-top: 0 !important;
            margin-bottom: 0.8rem !important;  /* CHANGED: Reduced from 1rem to 0.8rem */
        }

        /* ADDED: Reduce spacing after logo/title section */
        div[data-testid="stColumn"]:has(div.login-box-marker) .stMarkdown {
            margin-bottom: 0.3rem !important;  /* CHANGED: Reduced from 0.5rem to 0.3rem */
        }

        /* ADDED: Control spacing for text inputs */
        .stTextInput {
            margin-top: 0.1rem !important;
            margin-bottom: 0.2rem !important;
        }

        /* Input Fields */
        div[data-baseweb="input"] {
            border: none !important;
            background-color: transparent !important;
        }
        .stTextInput > div > div {
             background-color: var(--input-bg) !important;
             border-radius: 12px !important;
             border: 1px solid transparent !important;
        }
        .stTextInput > div > div > input {
            background-color: transparent !important;
            border: none !important;
            color: black !important;
            padding: 8px 15px !important;
            height: 42px !important; /* Slightly clearer input */
            font-size: 14px !important;
            outline: none !important;
            box-shadow: none !important;
        }
        /* Focus State - Target the wrapper div, not the input itself */
        .stTextInput > div:first-child > div:first-child:focus-within {
            background-color: #FFFFFF !important;
            border: 1px solid black !important;
            box-shadow: none !important;
            outline: none !important;
        }
        .stTextInput label {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: black !important;
            margin-bottom: 2px !important;
        }

        /* BUTTONS - Pill Shaped & Black - REDUCED HEIGHT */
        .stButton > button {
            background-color: black !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important; /* Pill shape */
            font-weight: 600 !important;
            font-size: 13px !important;
            height: 40px !important; /* Reduced Height */
            width: 100% !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
            transition: transform 0.1s ease;
            margin-top: 0.1rem !important;
            margin-bottom: 0.1rem !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            background-color: #222 !important;
        }
        
        /* Secondary / Google Button - Grey to differentiate */
        .google-btn-container button {
             background-color: #EEEEEE !important;
             color: black !important;
             box-shadow: none !important;
        }
        .google-btn-container button:hover {
             background-color: #E0E0E0 !important;
        }

        /* Simple Text Styling */
        .login-header {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 5px;
            text-align: center;
        }
        .login-sub {
            font-size: 13px;
            color: #666;
            text-align: center;
            margin-bottom: 25px;
        }
        
        /* Hide sidebar on Login */
        [data-testid="stSidebar"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        
        /* App Container */
        .main .block-container {
            padding-top: 0rem !important;      /* CHANGED: from 1rem to 0rem - removes top space */
            padding-bottom: 2rem !important;   /* ADDED: explicit bottom padding */
            padding-left: 1rem !important;     /* ADDED: explicit left padding */
            padding-right: 1rem !important;    /* ADDED: explicit right padding */
            max-width: 1000px !important;      /* CHANGED: from 900px to 1000px */
            margin-top: 0 !important;          /* ADDED: Force no top margin */
        }
        
        /* ADDED: Remove ALL top spacing from containers */
        .main > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        .main > div:first-child > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* ADDED: Remove top spacing from main container */
        .main {
            padding-top: 0 !important;
        }
        
        header { 
            visibility: hidden !important;     /* CHANGED: added !important */
            height: 0 !important;              /* ADDED: collapse header height */
            padding: 0 !important;             /* ADDED: remove all padding */
            margin: 0 !important;              /* ADDED: remove all margin */
        }
        
        /* ADDED: Hide Streamlit toolbar */
        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* ADDED: Ensure no extra spacing at top of app */
        [data-testid="stAppViewContainer"] > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def _apply_main_styles():
    st.markdown(
        """
        <style>
        :root{
          --ws-text: #000000; /* Black color for text */
          --ws-muted: rgba(75, 63, 114, 0.55);

          --pastel-pink: #F8E1F4;
          --pastel-lav: #E3D7F7;
          --pastel-blue: #D6EAF8;
          --white: #FFFFFF;

          --border-soft: rgba(75, 63, 114, 0.10);
          --shadow: 0 8px 24px rgba(75, 63, 114, 0.08);

          /* Bottom/chat theme */
          --bottom-1: rgba(253, 228, 234, 0.96); /* blush */
          --bottom-2: rgba(230, 218, 248, 0.96); /* gold */
          --bottom-border: rgba(255,218,185,0.22); /* gold */
          --chat-input-bg: linear-gradient(135deg, var(--pastel-pink) 0%, var(--pastel-lav) 60%, var(--pastel-blue) 100%); /* keep gradient to match page */
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
          background: linear-gradient(120deg, var(--pastel-pink) 0%, var(--pastel-lav) 60%, var(--pastel-blue) 100%) !important;
          min-height: 100vh !important;
        }

        .main .block-container{
          max-width: 1200px;
          padding-top: 1rem !important;        /* CHANGED: from 0rem to 1rem */
          padding-bottom: 1.2rem !important;
          padding-left: 2rem !important;       /* ADDED: explicit left padding */
          padding-right: 2rem !important;      /* ADDED: explicit right padding */
        }

        /* ===== Default text ===== */
        [data-testid="stAppViewContainer"] * { color: var(--ws-text) !important; }
        [data-testid="stCaptionContainer"], .stCaptionContainer, small {
          color: var(--pastel-blue) !important;
        }
        h1, h2 {
          color: var(--pastel-lav) !important;
        }
        h3, h4, h5, h6 {
          color: var(--pastel-blue) !important;
        }

        /* ===== Headings ===== */
        h1, h2{
          background: linear-gradient(90deg, var(--pastel-pink), var(--pastel-blue));
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent !important;
          letter-spacing: 0.2px;
        }
        h3, h4, h5, h6{ color: var(--pastel-lav) !important; }

        /* Remove sidebar toggle + its reserved space */
        div[data-testid="collapsedControl"],
        div[data-testid="stSidebarCollapseButton"]{
          display: none !important;
          height: 0 !important;
          width: 0 !important;
          margin: 0 !important;
          padding: 0 !important;
        }
       

        /* =========================================================
           SIDEBAR (LEFT PANEL) + STICKY LOGOUT FOOTER
           ========================================================= */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"]{
          background: linear-gradient(135deg, var(--pastel-pink) 0%, var(--pastel-lav) 60%, var(--pastel-blue) 100%) !important;
          padding-top: 1rem !important;        /* CHANGED: from 0 to 1rem */
          padding-bottom: 0 !important;
          padding-left: 1rem !important;       /* ADDED: explicit left padding */
          padding-right: 1rem !important;      /* ADDED: explicit right padding */
          margin: 0 !important;
        }
          [data-testid="stSidebar"] *{
          background: transparent !important;
          color: var(--ws-text) !important;
          border: none !important;
          box-shadow: none !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6 {
          margin: 0 !important;
          padding: 0 !important;
        }
        [data-testid="stSidebar"] .stContainer {
          padding: 0 !important;
          margin: 0 !important;
        }
        [data-testid="stSidebar"] .stMarkdown {
          margin: 0 !important;
          padding: 0 !important;
        }
        [data-testid="stSidebar"] .stVerticalBlockBorderWrapper {
          padding: 0 !important;
          margin: 0 !important;
        }

        /* Additional rules to remove top and bottom space in sidebar */
        [data-testid="stSidebar"] > div {
          padding-top: 0 !important;
          padding-bottom: 0 !important;
          margin-top: 0 !important;
          margin-bottom: 0 !important;
        }
        [data-testid="stSidebar"] > div > div {
          padding-top: 0 !important;
          padding-bottom: 0 !important;
          margin-top: 0 !important;
          margin-bottom: 0 !important;
        }
        /* Force no top space on the first child of sidebar */
        [data-testid="stSidebar"] > div:first-child {
          padding-top: 0 !important;
          margin-top: 0 !important;
        }

        [data-testid="stSidebar"] .stButton > button{
          width: 100%;
          text-align: left !important;
          justify-content: flex-start !important;
          border-radius: 12px !important;
          padding: 12px 14px !important;
          border: none !important;
          background: var(--white) !important;
          color: var(--ws-text) !important;
          font-size: 15px !important;
          height: auto !important;
          margin: 0 !important;
          box-shadow: 0 2px 8px rgba(75, 63, 114, 0.07);
          transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease, background 140ms ease;
        }
        [data-testid="stSidebar"] .stButton > button:hover{
          background: linear-gradient(135deg, var(--pastel-pink), var(--pastel-blue)) !important;
          color: var(--ws-text) !important;
        }

        .ws-sidebar-footer{
          position: sticky;
          bottom: 0;
          padding-top: 0px;
          padding-bottom: 0px;
          margin-top: 0px;
          background: linear-gradient(180deg, rgba(255,232,244,0.0), rgba(255,232,244,0.92));
          backdrop-filter: blur(10px);
          border-top: 1px solid rgba(232, 74, 159, 0.18);
          z-index: 5;
        }

        .ws-sidebar-footer .stButton > button{
          text-align: center !important;
          justify-content: center !important;
          font-weight: 700 !important;
          border: none !important;
          background: linear-gradient(90deg, var(--peach), var(--lav)) !important;
          color: var(--ws-text) !important;
          border-radius: 30px !important;
          height: 50px !important;
          font-size: 17px !important;
          box-shadow: none !important;
        }

        /* Main page buttons */
        .stButton > button{
          background: linear-gradient(90deg, var(--pastel-pink), var(--pastel-blue)) !important;
          color: var(--ws-text) !important;
          border-radius: 30px !important;
          height: 50px !important;
          font-size: 17px !important;
          font-weight: 700 !important;
          border: none !important;
          box-shadow: 0 8px 24px rgba(75, 63, 114, 0.08);
          transition: 0.3s ease;
          padding: 25px !important;
        }
        .stButton > button:hover {
          background: linear-gradient(90deg, var(--pastel-blue), var(--pastel-pink));
          box-shadow: 0 8px 32px rgba(75, 63, 114, 0.18);
          transform: scale(1.04);
          color: var(--ws-text) !important;
        }

        /* Chat bubbles */
        [data-testid="stChatMessage"]{ background: transparent !important; padding: 14px 0 !important; }
        [data-testid="stChatMessage"] > div{
          border-radius: 18px !important;
          padding: 16px 18px !important;
          max-width: 92% !important;
          box-shadow: var(--shadow) !important;
          border: 1px solid var(--border-soft) !important;
          backdrop-filter: blur(10px);
        }
/* Ensure Save/Cancel remain roomy and don't wrap their text */
        [data-testid="stChatMessage"] .stButton > button[aria-label="Save"],
        [data-testid="stChatMessage"] .stButton > button[aria-label="Cancel"] {
          padding: 10px 28px !important;
          font-size: 16px !important;
          white-space: nowrap !important;
          min-height: 44px !important;
        }

        /* Make inline textarea inside chat bubble fill the available width */
        [data-testid="stChatMessage"] > div { position: relative !important; }

        /* Make inline textarea inside chat bubble fill the available width and match bubble padding */
        [data-testid="stChatMessage"] textarea {
          display: block !important;
          width: calc(100% - 36px) !important;
          max-width: calc(100% - 36px) !important;
          min-height: 160px !important;
          box-sizing: border-box !important;
          border-radius: 12px !important;
          padding: 16px !important;
          font-size: 16px !important;
          background: rgba(255,255,255,0.95) !important;
          border: 1px solid rgba(75,63,114,0.08) !important;
          outline: none !important;
          resize: vertical !important;
          margin: 0 18px !important;
        }

        /* Ensure the Streamlit textarea wrapper occupies full width inside the chat bubble */
        [data-testid="stChatMessage"] .stTextArea,
        [data-testid="stChatMessage"] .stTextArea > div,
        [data-testid="stChatMessage"] .stTextArea > div > div {
          width: 100% !important;
          padding: 0 !important;
          margin: 0 !important;
          box-sizing: border-box !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="user"] > div{
          background: rgba(255, 255, 255, 0.95) !important;
          margin-left: auto !important;
          border: 1px solid var(--lav) !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="assistant"] > div{
          background: rgba(246, 242, 255, 0.65) !important;
          margin-right: auto !important;
          border: 1px solid var(--lav) !important;
        }

        /* =========================================================
           REMOVE BLACK STRIP BEHIND CHAT INPUT
           (Make the chat input full width across the page)
           ========================================================= */
        /* Ensure the bottom block spans full width and uses box-sizing */
        div[data-testid="stBottomBlockContainer"] {
          width: 100% !important;
          padding: 12px 24px !important;
          box-sizing: border-box !important;
          background: transparent !important;
        }

        /* Make the floating input container and bottom block full width and padded */
        .stChatFloatingInputContainer,
        div[data-testid="stChatInputContainer"],
        div[data-testid="stBottomBlockContainer"] {
          /* Use a single solid color behind the chat input across the page */
          background: var(--chat-input-bg) !important;
          border: none !important;
          box-shadow: none !important;
          width: 100% !important;
          max-width: 100% !important;
          padding: 12px 24px !important;
          box-sizing: border-box !important;
          border-radius: 0 !important; /* match full-width strip look */
        }

        /* Apply minimal wrapper to the input so the strip behind remains a single color */
        div[data-testid="stChatInputContainer"] {
          border: none !important; /* keep wrapper clean */
          border-radius: 0 !important; /* no rounded box so it blends */
          background: transparent !important; /* transparent so the strip shows */
          box-shadow: none !important;
          padding: 0 24px !important; /* align with strip padding */
          color: var(--ws-text) !important;
          width: 100% !important;
          max-width: 100% !important;
          margin: 0 auto !important;
          box-sizing: border-box !important;
        }

        /* Make the text input blend with the strip and occupy full width */
        div[data-testid="stChatInputContainer"] input,
        div[data-testid="stChatInputContainer"] textarea {
          color: var(--ws-text) !important;
          background: transparent !important; /* show the strip color behind */
          caret-color: var(--ws-text) !important;
          width: 100% !important;
          padding: 18px 12px !important; /* comfortable vertical padding */
          border-radius: 0 !important; /* flat edges to match strip */
          border: none !important;
          box-shadow: none !important;
          font-size: 16px !important;
        }

        /* Style the submit/send button so it's visible on the strip */
        div[data-testid="stChatInputContainer"] button {
          background: transparent !important;
          border: none !important;
          color: var(--ws-text) !important;
          font-weight: 700 !important;
        }

        /* Also ensure the bottom floating wrapper keeps full width */
        .stChatFloatingInputContainer { width: 100% !important; padding: 8px 24px !important; box-sizing: border-box !important; }

/* No hover / focus box */
[data-testid="stChatMessage"] .stButton > button[aria-label="✎"]:hover,
[data-testid="stChatMessage"] .stButton > button[aria-label="✎"]:focus,
[data-testid="stChatMessage"] .stButton > button[aria-label="✎"]:active {
  background: var(--ws-text) !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  transform: none !important;
}
/* ===== EDIT ICON (✎) — STREAMLIT KEY-BASED BUTTON FIX ===== */
/* Target the edit button by its text content instead of aria-label */

[data-testid="stChatMessage"] .stButton {
  padding: 0 !important;
  margin: 0 !important;
  min-height: 0 !important;
  height: auto !important;
  display: inline-flex !important;
  align-items: center !important;
}

/* Place edit icon inside chat bubble, top-right corner */
[data-testid="stChatMessage"] > div {
  position: relative !important; /* ensure bubble is relative for absolute positioning */
}
/* ================= SAVE & CANCEL — FINAL FIX ================= */

/* Target Save & Cancel buttons INSIDE chat */
[data-testid="stChatMessage"] .stButton > button {
  background: linear-gradient(
    135deg,
    var(--pastel-pink),
    var(--pastel-lav),
    var(--pastel-blue)
  ) !important;

  color: var(--ws-text) !important;
  font-weight: 700 !important;
  padding: 10px 28px !important;
  border-radius: 22px !important;
  border: none !important;
  box-shadow: 0 6px 16px rgba(75, 63, 114, 0.18) !important;
  cursor: pointer !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
  white-space: nowrap !important;
}

/* Hover effect */
[data-testid="stChatMessage"] .stButton > button:hover {
  transform: scale(1.06);
  box-shadow: 0 10px 26px rgba(75, 63, 114, 0.28) !important;
}
[data-testid="stChatMessage"] > div {
  position: relative !important;
}
        </style>
        """,
        unsafe_allow_html=True
    )