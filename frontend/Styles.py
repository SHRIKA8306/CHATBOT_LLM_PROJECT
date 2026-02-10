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
<<<<<<< HEAD
          border: 1px solid transparent !important;
          box-shadow: none !important;
=======
          border: 1px solid #374151 !important;
          box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.45) !important;
>>>>>>> 21ee670 (emergency button removed)
          outline: none !important;
        }
        .stTextInput label {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: black !important;
            margin-bottom: 2px !important;
        }

        /* BUTTONS - Pill Shaped & Theme Gradient - REDUCED HEIGHT */
        .stButton > button {
<<<<<<< HEAD
            background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
=======
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
>>>>>>> 21ee670 (emergency button removed)
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important; /* Slightly more rounded */
            font-weight: 600 !important;
            font-size: 14px !important;
            height: 48px !important; /* Increased height to match image */
            width: 100% !important;
<<<<<<< HEAD
            box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
=======
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.45) !important;
>>>>>>> 21ee670 (emergency button removed)
            transition: all 0.2s ease;
            margin-top: 0.1rem !important;
            margin-bottom: 0.1rem !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            filter: brightness(1.1);
<<<<<<< HEAD
            box-shadow: 0 6px 15px rgba(124, 58, 237, 0.3) !important;
        }
        
        /* Secondary / Google Button - Now using theme color to match user request */
        .google-btn-container button {
             background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #d946ef 100%) !important;
             color: #FFFFFF !important;
             box-shadow: 0 4px 10px rgba(124, 58, 237, 0.2) !important;
        }
=======
          box-shadow: 0 6px 15px rgba(0, 0, 0, 0.45) !important;
        }
        
        /* Secondary / Google Button - Now using theme color to match user request */
           .google-btn-container button {
             background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
             color: #FFFFFF !important;
             box-shadow: 0 4px 10px rgba(0, 0, 0, 0.45) !important;
           }
>>>>>>> 21ee670 (emergency button removed)
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
<<<<<<< HEAD
        /* --- 1. THE 3-DOTS TRIGGER BUTTON (SIDEBAR) --- */
        /* Remove the background box, border, and shadows */
=======
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
          background-color: rgba(0, 0, 0, 0.45) !important;
          border-color: #374151 !important;
          font-weight: 700 !important;
          color: #4C1D95 !important;
        }

        /* Popover "⋮" Styling */
>>>>>>> 21ee670 (emergency button removed)
        [data-testid="stSidebar"] [data-testid="stPopover"] > button {
          background: transparent !important;
          background-color: transparent !important;
          border: none !important;
          box-shadow: none !important;
<<<<<<< HEAD
          padding: 0 !important;
          min-height: unset !important;
          height: 30px !important;
          width: 30px !important;
=======
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

        /* Primary Sidebar Buttons (New Chat, Logout) - Theme Gradient */
        /* Using extremely high specificity to override Streamlit defaults */
        [data-testid="stSidebar"] div.sidebar-primary-btn .stButton > button {
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
          color: #FFFFFF !important;
          border: none !important;
          border-radius: 30px !important; /* Pill shape */
          font-weight: 700 !important;
          text-align: center !important;
          justify-content: center !important;
          padding: 12px 20px !important;
          margin: 10px 0 !important;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45) !important;
          display: flex !important;
          width: 100% !important;
        }
        [data-testid="stSidebar"] div.sidebar-primary-btn .stButton > button:hover {
          filter: brightness(1.1);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.45) !important;
          transform: translateY(-1px);
        }
        [data-testid="stSidebar"] div.sidebar-primary-btn .stButton > button * {
          color: #FFFFFF !important;
        }

        /* FORCE OVERRIDE: Ensure any inline or higher-specificity styles use the theme blue
           This targets buttons inside the sidebar including those with inline `style` attrs. */
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] .stButton > button[style],
        .sidebar-primary-btn .stButton > button[style] {
          background-image: none !important;
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
          background-color: #374151 !important;
          color: #FFFFFF !important;
          border: none !important;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45) !important;
        }

        /* Also override any globally inline-styled buttons to use theme gradient */
        .stButton > button[style] {
          background-image: none !important;
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
          background-color: #374151 !important;
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
          background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%) !important;
          color: #FFFFFF !important;
          border-radius: 12px !important;
          height: 48px !important;
          font-size: 16px !important;
          font-weight: 600 !important;
          border: none !important;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.45);
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
          box-shadow: 0 6px 15px rgba(0, 0, 0, 0.45);
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

        /* Popover buttons — Theme Gradient Pills, Centered, Narrow */
        [data-testid="stSidebar"] [data-testid="stPopoverBody"] .stButton > button {
          width: 50px !important;   /* Narrower buttons as set by user */
          height: 36px !important;
          padding: 0 !important;
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
          color: #FFFFFF !important;
          border-radius: 20px !important; /* Pill shape */
          border: none !important;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.42) !important;
          font-size: 13px !important;
          font-weight: 500 !important;
>>>>>>> 21ee670 (emergency button removed)
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
<<<<<<< HEAD
        
=======
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
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
          color: #FFFFFF !important;
          margin-left: auto !important;
          border: none !important;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.38) !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="user"] * {
          color: #FFFFFF !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="assistant"] > div{
          background: #FFFFFF !important;
          color: #111827 !important;
          margin-right: auto !important;
          border: 1px solid #EAF6FB !important; /* Extremely subtle blue border */
          box-shadow: 0 2px 12px rgba(0, 0, 0, 0.28) !important;
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
          border-color: #374151 !important;
        }

        /* Focus state - Show purple border when active */
        .stChatInput:focus-within,
        div[data-testid="stChatInputContainer"]:focus-within,
        div[data-testid="stChatInputContainer"]:focus-within > div,
        div[data-testid="stChatInputContainer"]:focus-within > div > div {
          border-color: #374151 !important;
          box-shadow: 0 0 0 1px #374151 !important;
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
          background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
          border: none !important;
          color: #FFFFFF !important;
          font-weight: 700 !important;
          padding: 8px 16px !important;
          border-radius: 8px !important;
          transition: all 0.2s ease !important;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.42) !important;
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
  background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
  padding: 8px 18px !important;
  border-radius: 8px !important;
  border: none !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.45) !important;
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

>>>>>>> 21ee670 (emergency button removed)
        </style>
        """,
        unsafe_allow_html=True
    )