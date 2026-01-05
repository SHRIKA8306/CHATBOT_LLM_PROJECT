import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        :root{
          --ws-text: #4B3F72; /* Elegant deep lavender for text */
          --ws-muted: rgba(75, 63, 114, 0.55);

          --pastel-pink: #F8E1F4;
          --pastel-lav: #E3D7F7;
          --pastel-blue: #D6EAF8;
          --white: #FFFFFF;

          --border-soft: rgba(75, 63, 114, 0.10);
          --shadow: 0 8px 24px rgba(75, 63, 114, 0.08);

          /* Bottom/chat theme */
          --bottom-1: rgba(253, 228, 234, 0.96); /* blush */
          --bottom-2: rgba(230, 218, 248, 0.96); /* lavender */
          --bottom-border: rgba(255,218,185,0.22); /* gold */
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
        }
          [data-testid="stSidebar"] *{
          background: transparent !important;
          color: var(--ws-text) !important;
          border: none !important;
          box-shadow: none !important;
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]{
          background: rgba(255,255,255,0.28) !important;
          border: 1px solid rgba(182,156,255,0.18) !important;
          border-radius: 16px !important;
          padding: 0px !important;
          padding-bottom: 0px !important;
          box-shadow: 0 10px 22px rgba(45, 27, 71, 0.08) !important;
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
          box-shadow: 0 2px 8px rgba(75, 63, 114, 0.07);
          transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease, background 140ms ease;
        }
        [data-testid="stSidebar"] .stButton > button:hover{
          background: linear-gradient(135deg, var(--pastel-pink), var(--pastel-blue)) !important;
          color: var(--ws-text) !important;
        }

        /* Chat history list items (sidebar) - show as full-width compact list like ChatGPT */
        [data-testid="stSidebar"] .chat-item{
          display:block;
          width:100%;
          padding:6px 8px; /* tighter vertical padding */
          border-radius:8px;
          background: transparent;
          color: var(--ws-text) !important;
          text-decoration: none;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          border-left: 3px solid transparent;
          margin: 4px 0; /* reduce gap between items */
          font-size: 16px; /* slightly larger for readability */
          line-height: 1.2;
        }
        [data-testid="stSidebar"] .chat-item:hover{
          background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.02));
        }
        [data-testid="stSidebar"] .chat-item.active{
          background: linear-gradient(90deg, rgba(230,218,248,0.95), rgba(214,234,248,0.95));
          border-left-color: rgba(75,63,114,0.8);
          font-weight:700;
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
           (This is the key fix)
           ========================================================= */
        /* Apply gradient border to the outer chat input box */
div[data-testid="stChatInputContainer"] {
  border: 2px solid transparent !important;
  border-image: linear-gradient(90deg, var(--pastel-pink), var(--pastel-blue)) 1 !important;
  border-radius: 22px !important;
  background: var(--white) !important;
  box-shadow: 0 2px 8px rgba(75, 63, 114, 0.07);
  padding: 8px !important;
  color: var(--ws-text) !important;
}
div[data-testid="stChatInputContainer"] input,
div[data-testid="stChatInputContainer"] textarea {
  color: var(--ws-text) !important;
  background: var(--white) !important;
  caret-color: var(--ws-text) !important;
}

/* Also fix floating wrapper if Streamlit uses it */
/* Make bottom chat bar same as top gradient header */
.stChatFloatingInputContainer,
div[data-testid="stChatInputContainer"],
div[data-testid="stBottomBlockContainer"] {
  background: linear-gradient(135deg, var(--pastel-pink) 0%, var(--pastel-lav) 60%, var(--pastel-blue) 100%) !important;
  border: none !important;
  box-shadow: none !important;
}
        
        </style>
        """,
        unsafe_allow_html=True
    )
