import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        :root{
          --ws-text: #2D1B47;
          --ws-muted: rgba(45, 27, 71, 0.72);

          --pink: #E84A9F;
          --hotpink: #FF4FA7;
          --lav: #B69CFF;
          --lav2: #D9CBFF;

          --border-soft: rgba(45, 27, 71, 0.12);
          --shadow: 0 10px 26px rgba(45, 27, 71, 0.10);

          /* Bottom/chat theme */
          --bottom-1: rgba(255, 232, 244, 0.96);
          --bottom-2: rgba(242, 235, 255, 0.96);
          --bottom-border: rgba(182,156,255,0.28);
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
          background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
          min-height: 100vh !important;
        }

        .main .block-container{
          max-width: 1200px;
          padding-top: 0rem !important;
          padding-bottom: 1.2rem !important;
        }

        /* ===== Default text ===== */
        [data-testid="stAppViewContainer"] * { color: var(--ws-text); }
        [data-testid="stCaptionContainer"], .stCaptionContainer, small { color: var(--ws-muted) !important; }

        /* ===== Headings ===== */
        h1, h2{
          background: linear-gradient(90deg, var(--hotpink), var(--lav));
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent !important;
          letter-spacing: 0.2px;
        }
        h3, h4, h5, h6{ color: var(--pink) !important; }

        /* Remove sidebar toggle + its reserved space */
        div[data-testid="collapsedControl"],
        div[data-testid="stSidebarCollapseButton"]{
          display: none !important;
          height: 0 !important;
          width: 0 !important;
          margin: 0 !important;
          padding: 0 !important;
        }
        section[data-testid="stSidebar"] > div{ padding-top: 0 !important; }
        [data-testid="stSidebarContent"]{ padding-top: 0 !important; }

        /* =========================================================
           SIDEBAR (LEFT PANEL) + STICKY LOGOUT FOOTER
           ========================================================= */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"]{
          background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        }

        [data-testid="stSidebar"] *{
          background: transparent !important;
          color: var(--ws-text) !important;
          border: none !important;
          box-shadow: none !important;
        }

        [data-testid="stSidebarContent"] > div{
          background: rgba(255,255,255,0.35) !important;
          border: 1px solid rgba(232, 74, 159, 0.18) !important;
          border-radius: 18px !important;
          padding: 20px !important;
          box-shadow: 0 14px 30px rgba(45, 27, 71, 0.12) !important;
          backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]{
          background: rgba(255,255,255,0.28) !important;
          border: 1px solid rgba(182,156,255,0.18) !important;
          border-radius: 16px !important;
          padding: 10px !important;
          padding-bottom: 70px !important;
          box-shadow: 0 10px 22px rgba(45, 27, 71, 0.08) !important;
        }

        [data-testid="stSidebar"] .stButton > button{
          width: 100%;
          text-align: left !important;
          justify-content: flex-start !important;
          border-radius: 10px !important;
          padding: 10px 10px !important;
          border: none !important;
          background: transparent !important;
          color: #5E2B97 !important;
          font-size: 14px !important;
          height: auto !important;
          box-shadow: none !important;
          transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease, background 140ms ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover{
          background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
          color: #5E2B97 !important;
          padding: 10px 10px !important;
        }

        .ws-sidebar-footer{
          position: sticky;
          bottom: 0;
          padding-top: 10px;
          padding-bottom: 10px;
          margin-top: 10px;
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
          background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
          color: white !important;
          border-radius: 30px !important;
          height: 50px !important;
          font-size: 17px !important;
          box-shadow: none !important;
        }

        /* Main page buttons */
        .stButton > button{
          background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
          color: white !important;
          border-radius: 30px !important;
          height: 50px !important;
          font-size: 17px !important;
          font-weight: 700 !important;
          border: none !important;
          box-shadow: 0 10px 25px rgba(232, 74, 159, 0.45);
          transition: 0.3s ease;
          padding: 25px !important;
        }
        .stButton > button:hover{
          transform: scale(1.04);
          box-shadow: 0 15px 35px rgba(232, 74, 159, 0.65);
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
          background: rgba(255, 255, 255, 0.78) !important;
          margin-left: auto !important;
          border: 1px solid rgba(232, 74, 159, 0.18) !important;
        }
        [data-testid="stChatMessage"][data-st-chat-message="assistant"] > div{
          background: rgba(217, 203, 255, 0.45) !important;
          margin-right: auto !important;
          border: 1px solid rgba(182, 156, 255, 0.22) !important;
        }

        /* =========================================================
           REMOVE BLACK STRIP BEHIND CHAT INPUT
           (This is the key fix)
           ========================================================= */
        /* Apply gradient border to the outer chat input box */
div[data-testid="stChatInputContainer"] {
    border: 2px solid transparent !important;
    border-image: linear-gradient(90deg, #E84A9F, #B69CFF) 1 !important;
    border-radius: 22px !important;
    background: rgba(255,255,255,0.6) !important; /* light blend */
    box-shadow: var(--shadow) !important;
    padding: 6px !important;
}

/* Also fix floating wrapper if Streamlit uses it */
/* Make bottom chat bar same as top gradient header */
.stChatFloatingInputContainer,
div[data-testid="stChatInputContainer"],
div[data-testid="stBottomBlockContainer"] {
    background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
    border: none !important;
    box-shadow: none !important;
}
        
        </style>
        """,
        unsafe_allow_html=True
    )
