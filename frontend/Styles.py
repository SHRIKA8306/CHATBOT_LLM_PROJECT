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

        img {
            width: 120px;
            height: auto;
            display: block;
            margin: 0 auto 1rem auto;
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
            border: 1px solid #A855F7 !important;
            box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2) !important;
            outline: none !important;
        }
        .stTextInput label {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: black !important;
            margin-bottom: 2px !important;
        }

        /* BUTTONS - Pill Shaped & Vibrant Purple Gradient - REDUCED HEIGHT */
        .stButton > button {
            background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important; /* Slightly more rounded */
            font-weight: 600 !important;
            font-size: 14px !important;
            height: 48px !important; /* Increased height to match image */
            width: 100% !important;
            box-shadow: 0 4px 10px rgba(147, 51, 234, 0.2) !important;
            transition: all 0.2s ease;
            margin-top: 0.1rem !important;
            margin-bottom: 0.1rem !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            filter: brightness(1.1);
            box-shadow: 0 6px 15px rgba(147, 51, 234, 0.3) !important;
        }
        
        /* Secondary / Google Button - Now using theme color to match user request */
        .google-btn-container button {
             background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
             color: #FFFFFF !important;
             box-shadow: 0 4px 10px rgba(147, 51, 234, 0.2) !important;
        }
        .google-btn-container button:hover {
             filter: brightness(1.1);
             transform: scale(1.02);
        }
        /* Ensure specific overrides for button contents */
        .google-btn-container button * {
             color: #FFFFFF !important;
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
        /* VERSION: 2024-UPDATE-V4 - FIXED CHAT INPUT & TEXT WRAPPING */
        :root{
          --ws-text: #000000;
          --ws-muted: #666666;

          --bg-main: #FFFFFF;
          --sidebar-bg: #FFFFFF;
          --white: #FFFFFF;

          --border-soft: #E5E5E5;
          --shadow: 0 4px 15px rgba(0, 0, 0, 0.05);

          /* Bottom/chat theme */
          --chat-input-bg: #FFFFFF;
          --chat-input-border: #E0E0E0;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
          background-color: var(--bg-main) !important;
          background-image: none !important;
          min-height: 100vh !important;
        }

        .main .block-container{
          max-width: 1200px;
          padding-top: 1.5rem !important; 
          padding-bottom: 1.2rem !important;
          padding-left: 2rem !important;
          padding-right: 2rem !important;
        }

        /* ===== Typography - Professional B&W ===== */
        [data-testid="stAppViewContainer"] * { color: #000000 !important; }
        
        h1, h2, h3, h4, h5, h6 { 
          color: #000000 !important; 
          font-weight: 700 !important; 
          background: none !important;
          -webkit-background-clip: initial !important;
          background-clip: initial !important;
          margin-top: 0.5rem !important;
          margin-bottom: 0.5rem !important;
        }
        
        [data-testid="stCaptionContainer"], .stCaptionContainer, small {
          color: #666666 !important;
          font-size: 0.85rem !important;
        }

        /* Ensure sidebar is distinct and visible in main view */
        [data-testid="stSidebar"] {
          display: flex !important;
          visibility: visible !important;
          border-right: 1px solid #D1D5DB !important;
          box-shadow: 2px 0 10px rgba(0,0,0,0.02) !important;
          width: 320px !important; /* Increased Breadth */
          min-width: 320px !important;
        }
        [data-testid="stSidebarContent"] {
          background-color: #FFFFFF !important;
        }

        /* Sidebar Navigation Items */
       

        /* =========================================================
           SIDEBAR (LEFT PANEL) + STICKY LOGOUT FOOTER
           ========================================================= */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"]{
          background-color: var(--sidebar-bg) !important;
          background-image: none !important;
          border-right: 1px solid var(--border-soft) !important;
          padding-top: 1.5rem !important;
          padding-bottom: 0 !important;
          padding-left: 1rem !important;
          padding-right: 1rem !important;
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

        /* ===== FIXED: Sidebar History Items - PROPER TEXT WRAPPING ===== */
        [data-testid="stSidebar"] div[data-testid="column"] .stButton > button {
          width: 100% !important;
          max-width: 220px !important; /* Constrain button width */
          text-align: left !important;
          justify-content: flex-start !important;
          border-radius: 8px !important;
          padding: 8px 12px !important;
          border: none !important;
          background-color: transparent !important;
          color: #000000 !important;
          font-size: 14px !important;
          font-weight: 400 !important;
          min-height: 40px !important;
          height: auto !important; /* Allow height to grow */
          margin: 1px 0 !important;
          box-shadow: none !important;
          transition: all 0.2s ease;
          overflow: hidden !important; /* Contain overflow */
          display: flex !important;
          align-items: flex-start !important; /* Align to top for multiline */
          white-space: normal !important; /* Allow wrapping */
          word-wrap: break-word !important;
          word-break: break-word !important;
        }

        /* FIXED: Allow text to wrap properly inside sidebar buttons */
        [data-testid="stSidebar"] div[data-testid="column"] .stButton > button div[data-testid="stMarkdownContainer"] p {
          white-space: normal !important; /* Allow text wrapping */
          overflow-wrap: break-word !important; /* Break long words */
          word-wrap: break-word !important; /* Break long words */
          word-break: break-word !important; /* Break long words */
          hyphens: auto !important; /* Add hyphenation for better breaks */
          max-width: 100% !important; /* Use full available width */
          width: 100% !important;
          display: block !important;
          margin: 0 !important;
          padding: 0 !important;
          color: #000000 !important;
          text-align: left !important;
          line-height: 1.3 !important; /* Tighter line spacing */
          overflow: hidden !important; /* Hide any overflow */
          text-overflow: clip !important;
        }
        
        /* Force the button content wrapper to respect width */
        [data-testid="stSidebar"] div[data-testid="column"] .stButton > button > div {
          max-width: 100% !important;
          overflow: hidden !important;
          word-wrap: break-word !important;
        }

        [data-testid="stSidebar"] div[data-testid="column"] .stButton > button:hover {
          background-color: #EEEEEE !important;
          border-color: #D1D5DB !important;
        }
        
        /* Highlight Active Chat */
        .sidebar-active-chat .stButton > button {
          background-color: rgba(168, 85, 247, 0.1) !important;
          border-color: #A855F7 !important;
          font-weight: 700 !important;
          color: #4C1D95 !important;
        }

        /* Popover "⋮" Styling */
        [data-testid="stSidebar"] [data-testid="stPopover"] > button {
          background: transparent !important;
          border: none !important;
          padding: 0 !important;
          margin: 0 !important;
          width: 20px !important;
          height: 40px !important;
          min-width: 20px !important;
          box-shadow: none !important;
          color: #666666 !important;
        }
        [data-testid="stSidebar"] [data-testid="stPopover"] > button:hover {
          background: #ECECEC !important;
          color: #000000 !important;
          border-radius: 4px !important;
        }
        /* HIDE the downward arrow in popover */
        [data-testid="stSidebar"] [data-testid="stPopover"] > button div[data-testid="stMarkdownContainer"] + svg {
          display: none !important;
        }
        [data-testid="stSidebar"] [data-testid="stPopover"] svg {
          display: none !important;
        }

        /* Primary Sidebar Buttons (New Chat, Logout) - Vibrant Purple Gradient */
        /* Using extremely high specificity to override Streamlit defaults */
        [data-testid="stSidebar"] div.sidebar-primary-btn .stButton > button {
          background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
          color: #FFFFFF !important;
          border: none !important;
          border-radius: 30px !important; /* Pill shape */
          font-weight: 700 !important;
          text-align: center !important;
          justify-content: center !important;
          padding: 12px 20px !important;
          margin: 10px 0 !important;
          box-shadow: 0 4px 12px rgba(147, 51, 234, 0.2) !important;
          display: flex !important;
          width: 100% !important;
        }
        [data-testid="stSidebar"] div.sidebar-primary-btn .stButton > button:hover {
          filter: brightness(1.1);
          box-shadow: 0 6px 16px rgba(168, 85, 247, 0.3) !important;
          transform: translateY(-1px);
        }
        [data-testid="stSidebar"] div.sidebar-primary-btn .stButton > button * {
          color: #FFFFFF !important;
        }

        .ws-sidebar-footer .stButton > button{
          background: #000000 !important;
          color: #FFFFFF !important;
          border-radius: 30px !important; /* Pill shape */
          height: 44px !important;
          font-size: 15px !important;
          font-weight: 600 !important;
          box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
        }
        .ws-sidebar-footer .stButton > button * {
            color: #FFFFFF !important;
        }

        /* Main page buttons (Emergency, etc.) */
        .stButton > button{
          background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
          color: #FFFFFF !important;
          border-radius: 12px !important;
          height: 48px !important;
          font-size: 16px !important;
          font-weight: 600 !important;
          border: none !important;
          box-shadow: 0 4px 10px rgba(147, 51, 234, 0.2);
          transition: 0.2s ease;
          padding: 0 25px !important;
        }
        /* CRITICAL: Force elements to be white on purple gradient */
        .stButton > button *, 
        .sidebar-primary-btn button * {
            color: #FFFFFF !important;
        }
        
        .stButton > button:hover {
          filter: brightness(1.1);
          transform: translateY(-2px);
          box-shadow: 0 6px 15px rgba(168, 85, 247, 0.3);
        }
        /* ===== Compact Popover Menu (Final Adjustment) ===== */

        /* Popover box — Extremely narrow and centered */
        [data-testid="stSidebar"] [data-testid="stPopoverBody"] {
          background-color: #F1F3F4 !important; /* Matches sidebar bg for seamless look */
          border-radius: 12px !important;
          box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
          border: 1px solid rgba(0,0,0,0.05) !important;
          padding: 2px 0 !important;
          width: 50px !important;
          min-width: 50px !important;
          max-width: 50px !important;
          display: flex !important;
          flex-direction: column !important;
          align-items: center !important;
        }

        /* Popover buttons — Black Pills, Centered, Narrow */
        [data-testid="stSidebar"] [data-testid="stPopoverBody"] .stButton {
          width: 100% !important;
          display: flex !important;
          justify-content: center !important;
          margin: 4px 0 !important;
        }

        /* Popover buttons — Vibrant Purple Gradient Pills, Centered, Narrow */
        [data-testid="stSidebar"] [data-testid="stPopoverBody"] .stButton > button {
          width: 50px !important;   /* Narrower buttons as set by user */
          height: 36px !important;
          padding: 0 !important;
          background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
          color: #FFFFFF !important;
          border-radius: 20px !important; /* Pill shape */
          border: none !important;
          box-shadow: 0 2px 8px rgba(147, 51, 234, 0.2) !important;
          font-size: 13px !important;
          font-weight: 500 !important;
          display: flex !important;
          align-items: center !important;
          justify-content: center !important;
          text-align: center !important;
          transition: all 0.2s ease !important;
        }

        [data-testid="stSidebar"] [data-testid="stPopoverBody"] .stButton > button:hover {
          filter: brightness(1.1);
          transform: translateY(-1px);
        }

        /* Ensure text inside buttons is centered and white */
        [data-testid="stSidebar"] [data-testid="stPopoverBody"] .stButton > button div[data-testid="stMarkdownContainer"] p {
            justify-content: center !important;
            color: #FFFFFF !important;
            margin: 0 !important;
        }

        /* Override any inherited coloring */
        [data-testid="stPopoverBody"] .stButton > button * {
          color: #FFFFFF !important;
        }
        
        /* Highlight for Selected Chat in Sidebar */
        /* Active Chat Pill Highlight */
        .sidebar-active-chat .stButton > button {
          background: #F0F0F0 !important;
          font-weight: 600 !important;
          border-radius: 8px !important;
        }
        [data-testid="stSidebar"] div[data-testid="column"] .stButton > button:hover {
          background: #F8F8F8 !important;
        }

        /* Ensure sidebar chat buttons wrap long titles */
        [data-testid="stSidebar"] .stButton > button {
          white-space: normal !important;
          word-break: break-word !important;
          text-align: left !important;
          height: auto !important;
          min-height: 38px !important;
        }

        /* Chat bubbles */
        [data-testid="stChatMessage"]{ background: transparent !important; padding: 14px 0 !important; }
        [data-testid="stChatMessage"] > div{
          border-radius: 18px !important;
          padding: 16px 18px !important;
          max-width: 85% !important;
          box-shadow: var(--shadow) !important;
          border: 1px solid var(--border-soft) !important;
          backdrop-filter: blur(10px);
          overflow-wrap: break-word !important;
          word-break: break-word !important;
          hyphens: auto !important;
        }
/* Ensure Save/Cancel remain roomy and don't wrap their text */
        [data-testid="stChatMessage"] .stButton > button[aria-label="Save"],
        [data-testid="stChatMessage"] .stButton > button[aria-label="Cancel"] {
          padding: 5px 12px !important;
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
        /* Chat bubbles - Further Refined Professional Look */
        [data-testid="stChatMessage"]{ background: transparent !important; padding: 12px 0 !important; }
        [data-testid="stChatMessage"] > div{
          border-radius: 12px !important;
          padding: 14px 18px !important;
          max-width: 85% !important;
          box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
          border: 1px solid #F3F4F6 !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="user"] > div{
          background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
          color: #FFFFFF !important;
          margin-left: auto !important;
          border: none !important;
          box-shadow: 0 4px 15px rgba(147, 51, 234, 0.1) !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="user"] * {
          color: #FFFFFF !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="assistant"] > div{
          background: #FFFFFF !important;
          color: #111827 !important;
          margin-right: auto !important;
          border: 1px solid #F3E8FF !important; /* Extremely subtle purple border */
          box-shadow: 0 2px 12px rgba(147, 51, 234, 0.03) !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="assistant"] * {
          color: #111827 !important;
        }

        /* =========================================================
           CHAT INPUT - FIXED VISIBILITY
           ========================================================= */
        /* Bottom block container */
        div[data-testid="stBottomBlockContainer"] {
          width: 100% !important;
          padding: 12px 24px !important;
          box-sizing: border-box !important;
          background: #FFFFFF !important;
          border-top: 1px solid #E5E5E5 !important;
        }

        /* Floating input container */
        .stChatFloatingInputContainer {
          background: #FFFFFF !important;
          width: 100% !important;
          max-width: 100% !important;
          padding: 12px 0 !important;
          box-sizing: border-box !important;
        }

        /* THE NUCLEAR OPTION - REMOVE ALL BORDERS BY DEFAULT */
        .stChatInput,
        div[data-testid="stChatInputContainer"],
        div[data-testid="stChatInputContainer"] > div,
        div[data-testid="stChatInputContainer"] > div > div,
        div[data-testid="stChatInputContainer"] > div > div > div {
          background-color: #FFFFFF !important;
          border: 1px solid transparent !important; /* NO BORDER */
          border-radius: 12px !important;
          box-shadow: none !important;
          outline: none !important;
          transition: all 0.2s ease !important;
        }

        /* Show border ONLY on hover */
        div[data-testid="stChatInputContainer"]:hover,
        div[data-testid="stChatInputContainer"]:hover > div,
        div[data-testid="stChatInputContainer"]:hover > div > div {
          border-color: #9333EA !important;
        }

        /* Focus state - Show purple border when active */
        .stChatInput:focus-within,
        div[data-testid="stChatInputContainer"]:focus-within,
        div[data-testid="stChatInputContainer"]:focus-within > div,
        div[data-testid="stChatInputContainer"]:focus-within > div > div {
          border-color: #9333EA !important;
          box-shadow: 0 0 0 1px #9333EA !important;
          outline: none !important;
        }

        /* Kill all default Streamlit focus rings */
        [data-testid="stChatInputContainer"] textarea:focus,
        [data-testid="stChatInputContainer"] textarea:active {
          border: none !important;
          box-shadow: none !important;
          outline: none !important;
        }

        /* The actual input field */
        div[data-testid="stChatInputContainer"] input,
        div[data-testid="stChatInputContainer"] textarea {
          color: #000000 !important;
          background: transparent !important;
          caret-color: #000000 !important;
          width: 100% !important;
          padding: 12px 8px !important;
          border: none !important;
          outline: none !important;
          box-shadow: none !important;
          font-size: 16px !important;
        }

        div[data-testid="stChatInputContainer"] input::placeholder,
        div[data-testid="stChatInputContainer"] textarea::placeholder {
          color: #9CA3AF !important;
        }

        /* Submit button */
        div[data-testid="stChatInputContainer"] button {
          background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
          border: none !important;
          color: #FFFFFF !important;
          font-weight: 700 !important;
          padding: 8px 16px !important;
          border-radius: 8px !important;
          transition: all 0.2s ease !important;
          box-shadow: 0 2px 5px rgba(147, 51, 234, 0.2) !important;
        }

        div[data-testid="stChatInputContainer"] button:hover {
          filter: brightness(1.1);
        }

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
  background: linear-gradient(135deg, #9333EA 0%, #7C3AED 100%) !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
  padding: 8px 18px !important;
  border-radius: 8px !important;
  border: none !important;
  box-shadow: 0 4px 10px rgba(147, 51, 234, 0.2) !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  white-space: nowrap !important;
}

/* Hover effect */
[data-testid="stChatMessage"] .stButton > button:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
[data-testid="stChatMessage"] > div {
  position: relative !important;
}

/* Popover buttons styling */
[data-testid="stPopover"] button {
  font-size: 16px !important;
  padding: 8px !important;
  min-width: 40px !important;
  width: 40px !important;
  height: 40px !important;
  border-radius: 6px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

        </style>
        """,
        unsafe_allow_html=True
    )