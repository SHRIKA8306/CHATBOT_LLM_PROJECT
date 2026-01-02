import streamlit as st

def apply_styles():

    st.markdown("""
    <style>
    /* ---------- FULL PAGE BACKGROUND FIX ---------- */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        min-height: 100vh !important;
    }

    /* Remove default padding/margins */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* ---------- HEADINGS ---------- */
    h1, h2, h3 {
        color: #5E2B97;
        font-weight: 800;
    }

    /* ---------- GLASS CARD ---------- */
    .glass-card {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 35px;
        box-shadow: 0 20px 40px rgba(94, 43, 151, 0.25);
    }

    /* ---------- INPUT FIX ---------- */
    .stTextInput input {
        border-radius: 18px !important;
        height: 48px !important;
        border: none !important;
        outline: none !important;
        padding-left: 15px !important;
    }

    /* ---------- BUTTON ---------- */
    .stButton button {
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

    .stButton button:hover {
        transform: scale(1.04);
        box-shadow: 0 15px 35px rgba(232, 74, 159, 0.65);
    }

    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
        color: white;
    }

    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] p {
        color: white;
    }

    /* ---------- CHAT INPUT FIX ---------- */
    .stChatInput textarea {
        border-radius: 20px !important;
        padding: 15px !important;
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
    }

    
    /* ---------- CHAT MESSAGES ---------- */
    .stChatMessage {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC)  !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
    }

    /* ---------- SIDEBAR BUTTONS ---------- */
    .stSidebar .stButton button {
        background: transparent !important;
        color: #5E2B97 !important;
        border: none !important;
        text-align: left !important;
        padding: 5px 0 !important;
        font-size: 14px !important;
        height: auto !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }
    .stSidebar .stButton button:hover {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        color: #5E2B97  !important;
        padding: 10px  !important;
    }

    /* ---------- BUTTON CONTAINER ---------- */
    .button-container .stButton button {
        background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
        color: white !important;
        border-radius: 30px !important;
        height: 50px !important;
        font-size: 17px !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* ---------- LOGOUT BUTTON ---------- */
    .stSidebar .logout-button .stButton button {
        background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
        color: white !important;
        border-radius: 30px !important;
        height: 50px !important;
        font-size: 17px !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* ---------- CHAT MESSAGES ---------- */
    .stChatMessage {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        border-radius: 20px !important;
    }
            
    </style>
    """, unsafe_allow_html=True)