import streamlit as st

def apply_styles():
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
          padding-top: 0rem !important;
          padding-bottom: 1.2rem !important;
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
          padding-top: 0 !important;
          padding-bottom: 0 !important;
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