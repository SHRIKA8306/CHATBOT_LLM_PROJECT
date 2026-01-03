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

        html, body { background: transparent; }

        /* ===== App background (girly gradient) ===== */
        [data-testid="stAppViewContainer"]{
          background:
            radial-gradient(1000px 700px at 12% 10%, rgba(255, 79, 167, 0.25), transparent 60%),
            radial-gradient(900px 650px at 88% 20%, rgba(182, 156, 255, 0.28), transparent 55%),
            linear-gradient(135deg, #FFF6FB, #F3EEFF) !important;
          min-height: 100vh;
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
          background:
            radial-gradient(700px 500px at 20% 10%, rgba(255,79,167,0.18), transparent 60%),
            radial-gradient(700px 500px at 80% 30%, rgba(182,156,255,0.22), transparent 60%),
            linear-gradient(180deg, #FFE8F4, #F2EBFF) !important;
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
          padding: 14px 12px 12px 12px !important;
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
          border-radius: 14px !important;
          padding: 10px 12px !important;
          border: 1px solid rgba(45,27,71,0.10) !important;
          background: rgba(255,255,255,0.55) !important;
          transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease, background 140ms ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover{
          transform: translateY(-1px);
          box-shadow: 0 12px 24px rgba(45, 27, 71, 0.14) !important;
          filter: brightness(1.03);
          background: linear-gradient(90deg, rgba(255,79,167,0.20), rgba(182,156,255,0.18)) !important;
          border: 1px solid rgba(232, 74, 159, 0.18) !important;
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
          border: 1px solid rgba(255, 79, 167, 0.28) !important;
          background: linear-gradient(90deg, rgba(255,79,167,0.25), rgba(182,156,255,0.20)) !important;
        }

        /* Main page buttons */
        .stButton > button{
          border-radius: 14px !important;
          border: 1px solid rgba(232, 74, 159, 0.22) !important;
          background: linear-gradient(90deg, rgba(232,74,159,0.18), rgba(182,156,255,0.18)) !important;
          transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease;
        }
        .stButton > button:hover{
          transform: translateY(-1px);
          box-shadow: 0 14px 30px rgba(45, 27, 71, 0.16);
          filter: brightness(1.05);
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
        [data-testid="stBottomBlockContainer"]{
          background: linear-gradient(135deg, var(--bottom-1), var(--bottom-2)) !important;
          border-top: 1px solid var(--bottom-border) !important;
          box-shadow: 0 -14px 34px rgba(45, 27, 71, 0.10) !important;
        } /* [web:534] */

        /* Sometimes the floating container is the one that appears dark */
        .stChatFloatingInputContainer{
          background: linear-gradient(135deg, var(--bottom-1), var(--bottom-2)) !important;
          border-top: 1px solid var(--bottom-border) !important;
        } /* [web:537] */

        /* =========================================================
           CHAT INPUT COLORS
           ========================================================= */
        div[data-testid="stChatInput"]{
          background: linear-gradient(135deg, rgba(255,255,255,0.75), rgba(217,203,255,0.45)) !important;
          border-radius: 22px !important;
          padding: 14px 16px !important;
          border: 1px solid rgba(182,156,255,0.35) !important;
          backdrop-filter: blur(10px);
        } /* [web:500] */

        div[data-testid="stChatInput"] textarea,
        div[data-testid="stChatInput"] input{
          background: rgba(255,255,255,0.92) !important;
          color: var(--ws-text) !important;
          border: 1px solid rgba(232,74,159,0.22) !important;
          border-radius: 16px !important;
          padding: 14px 14px !important;
        } /* [web:501] */

        div[data-testid="stChatInput"] textarea::placeholder,
        div[data-testid="stChatInput"] input::placeholder{
          color: rgba(45,27,71,0.45) !important;
        } /* [web:501] */

        div[data-testid="stChatInput"] button{
          background: linear-gradient(90deg, #B69CFF, #FF4FA7) !important;
          color: white !important;
          border-radius: 22px !important;
          border: none !important;
          box-shadow: 0 10px 22px rgba(45, 27, 71, 0.16) !important;
          transition: transform 140ms ease, filter 140ms ease, box-shadow 140ms ease;
        } /* [web:500] */

        div[data-testid="stChatInput"] button:hover{
          transform: translateY(-1px);
          filter: brightness(1.06);
        } /* [web:500] */
        </style>
        """,
        unsafe_allow_html=True
    )
