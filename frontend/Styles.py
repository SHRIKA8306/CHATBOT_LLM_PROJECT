import streamlit as st

def apply_styles():
    """
    Applies CSS based on the login state.
    """
    if st.session_state.get("logged_in", False):
        _apply_main_styles()
    else:
        _apply_login_styles()

def _apply_login_styles():
    # EXACTLY AS PROVIDED - NO CHANGES MADE HERE
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
          border: 1px solid transparent !important;
          box-shadow: none !important;
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
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important; /* Slightly more rounded */
            font-weight: 600 !important;
            font-size: 14px !important;
            height: 48px !important; /* Increased height to match image */
            width: 100% !important;
            box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
            transition: all 0.2s ease;
            margin-top: 0.1rem !important;
            margin-bottom: 0.1rem !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            filter: brightness(1.1);
            box-shadow: 0 6px 15px rgba(124, 58, 237, 0.3) !important;
        }
        
        /* Secondary / Google Button - Now using theme color to match user request */
        .google-btn-container button {
             background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
             color: #FFFFFF !important;
             box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
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
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 5px;
            text-align: center;
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Hide sidebar on Login */
        [data-testid="stSidebar"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        
        /* App Container */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 1000px !important;
            margin-top: 0 !important;
        }
        
        header { 
            visibility: hidden !important;
            height: 0 !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
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
          --bg-main: #FFFFFF;
          --sidebar-bg: #FFFFFF;
          --border-soft: #E5E5E5;
          /* --- CHAT INPUT FINAL FIX --- */

        /* 1. Remove the outer red border entirely */
        [data-testid="stChatInput"] {
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
        }

        /* 2. Style the main box - This becomes your SINGLE border */
        [data-testid="stChatInput"] > div {
            border: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important; /* Purple border */
            border-radius: 14px !important;
            background-color: #F8F9FA !important;
            padding: 4px !important;
        }

        /* 3. Remove borders from the inner text box so they don't double up */
        [data-testid="stChatInput"] textarea {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        /* 4. Ensure the Send Button uses your gradient */
        [data-testid="stChatInput"] button {
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
            border: none !important;
            border-radius: 10px !important;
            color: white !important;
        }

        /* 5. Handle Focus (when typing) - stay purple, no red! */
        [data-testid="stChatInput"] > div:focus-within {
            border-color: #d946ef !important; /* Changes to pinkish on click */
            box-shadow: 0 0 10px rgba(124, 58, 237, 0.2) !important;
        }
        /* --- 1. THE 3-DOTS TRIGGER BUTTON (SIDEBAR) --- */
        /* Remove the background box, border, and shadows */
        [data-testid="stSidebar"] [data-testid="stPopover"] > button {
          background: transparent !important;
          background-color: transparent !important;
          border: none !important;
          box-shadow: none !important;
          padding: 0 !important;
          min-height: unset !important;
          height: 30px !important;
          width: 30px !important;
          display: flex !important;
          align-items: center !important;
          justify-content: center !important;
        }
        /* HIDE THE ARROW ICON (Targeting all possible icon containers) */
        [data-testid="stSidebar"] [data-testid="stPopover"] button svg,
        [data-testid="stSidebar"] [data-testid="stPopover"] button [data-testid="stIconChevronDown"],
        [data-testid="stSidebar"] [data-testid="stPopover"] button div:nth-child(2) {
          display: none !important;
          visibility: hidden !important;
          width: 0 !important;
        }

        /* Center and style the 3 dots text */
        [data-testid="stSidebar"] [data-testid="stPopover"] p {
          font-size: 24px !important;
          font-weight: bold !important;
          color: #333 !important;
          margin: 0 !important;
          padding: 0 !important;
          line-height: 1 !important;
          text-align: center !important;
          width: 100% !important;
        }

        /* --- 2. THE ACTION MENU (SHARE/RENAME/DELETE) --- */

         /* We remove the [data-testid="stSidebar"] prefix because popovers float in a portal */
        div[data-testid="stPopoverBody"] {
          width: 150px !important; 
          min-width: 120px !important;
          max-width: 120px !important;
          padding: 8px !important;
          border-radius: 6px !important;
          background-color: white !important;
        }

        /* Target the vertical spacing inside the popover */
        div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlock"] {
            gap: 4px !important;
            padding: 0 !important;
        }

        /* Style the internal buttons to be very small */
        div[data-testid="stPopoverBody"] .stButton > button {
          height: 30px !important;
          min-height: 12px !important;
          font-size: 12px !important;
          padding:  8px !important;
          border-radius: 6px !important;
          background:white !important;
          border: 1px solid #white !important;
          color: #444 !important;
          width: 100% !important;
          margin: 0 !important;
        }
        }
/* --- ADD THIS TO Styles.py --- */
        
        /* Targets every message container (Both User and AI) */
        [data-testid="stChatMessage"] {
            background-color: #F9FAFB !important; /* Light grey box */
            border: 1px solid #E5E7EB !important; /* Soft border */
            border-radius: 15px !important;       /* Rounded corners */
            padding: 1.5rem !important;           /* Inner spacing */
            margin-bottom: 1rem !important;       /* Space between boxes */
            box-shadow: 0 2px 5px rgba(0,0,0,0.03) !important;
        }

        /* Specifically changes the AI (Output) box color to pure white */
        [data-testid="stChatMessageAssistant"] {
            background-color: #FFFFFF !important;
            border-color: #D1D5DB !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        }

        /* Styling the small copy/edit buttons inside the boxes */
        [data-testid="stChatMessage"] button {
            border-radius: 8px !important;
            border: 1px solid #eee !important;
            background: white !important;
            color: #666 !important;
            padding: 2px 8px !important;
        }

        /* --- GRADIENT BUTTONS: New Chat, Logout, Emergency ONLY --- */
        
        /* Override chat message buttons back to default */
        [data-testid="stChatMessage"] button {
            border-radius: 8px !important;
            border: 1px solid #eee !important;
            background: white !important;
            color: #666 !important;
            padding: 2px 8px !important;
            height: auto !important;
            box-shadow: none !important;
            transform: none !important;
        }
        
        /* Protect chat history buttons - keep them white/default */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has(.element-container) .stButton button {
            background: white !important;
            color: #333 !important;
            border: 1px solid #ddd !important;
            box-shadow: none !important;
            height: auto !important;
            transform: none !important;
        }
        
        /* Target New Chat button specifically (appears after "Hi" greeting) */
        [data-testid="stSidebar"] > div > div > div > div > div:nth-child(2) .stButton button {
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            height: 48px !important;
            box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        
        /* Target Logout button at bottom of sidebar */
        [data-testid="stSidebar"] > div:last-child .stButton:last-child button,
        [data-testid="stSidebar"] .element-container:last-child .stButton button {
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            height: 48px !important;
            box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        
        /* Target Emergency button in header column */
        div[data-testid="column"]:last-child > div > div .stButton button,
        div[data-testid="column"]:nth-child(2) .stButton button,
        [data-testid="stVerticalBlock"] div[data-testid="column"]:last-child .stButton button {
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            height: 48px !important;
            box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        
        /* Hover effects for gradient buttons only */
        [data-testid="stSidebar"] > div > div > div > div > div:nth-child(2) .stButton button:hover,
        [data-testid="stSidebar"] > div:last-child .stButton:last-child button:hover,
        [data-testid="stSidebar"] .element-container:last-child .stButton button:hover,
        div[data-testid="column"]:last-child > div > div .stButton button:hover,
        div[data-testid="column"]:nth-child(2) .stButton button:hover,
        [data-testid="stVerticalBlock"] div[data-testid="column"]:last-child .stButton button:hover {
            transform: scale(1.02) !important;
            filter: brightness(1.1) !important;
            box-shadow: 0 6px 15px rgba(124, 58, 237, 0.3) !important;
        }
        
        /* Make sure popover buttons stay white */
        div[data-testid="stPopoverBody"] .stButton > button {
            background: white !important;
        }
        
        div[data-testid="stPopoverBody"] .stButton > button:hover {
            transform: none !important;
            filter: none !important;
            background: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )