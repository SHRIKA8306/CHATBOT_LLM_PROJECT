import streamlit as st

def apply_styles():
    st.markdown("""
    <style>

    /* ---------- GLOBAL BACKGROUND ---------- */
    .stApp {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        min-height: 100vh;
    }

    /* ---------- SIDEBAR BASE ---------- */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
    }

    /* ---------- ALL SIDEBAR ELEMENTS ---------- */
    [data-testid="stSidebar"] * {
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
        color: #2d1b47 !important;
        transition: all 0.2s ease-in-out;
    }

    /* ---------- HOVER EFFECTS FOR SIDEBAR ELEMENTS ---------- */
    [data-testid="stSidebar"] button:hover,
    [data-testid="stSidebar"] input:hover,
    [data-testid="stSidebar"] textarea:hover,
    [data-testid="stSidebar"] select:hover,
    [data-testid="stSidebar"] .stExpander:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.03);
        border-radius: 12px;
    }

    /* ---------- INPUTS / TEXTAREAS / SELECTS IN SIDEBAR ---------- */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        border-radius: 12px;
        border: none !important;
        padding: 6px 10px;
        color: #2d1b47 !important;
    }

    /* ---------- CHAT MESSAGES ---------- */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        box-shadow: none !important;
        padding: 8px 0 !important;
    }

    [data-testid="stChatMessage"] p {
        color: #2d1b47 !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* ---------- MAIN PAGE CHAT INPUT CONTAINER ---------- */
    [data-testid="stChatInput"] {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        border-radius: 15px !important;
        padding: 6px 12px !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input {
        background: linear-gradient(135deg, #FFD6E8, #C18CFC) !important;
        border-radius: 12px !important;
        color: #2d1b47 !important;
        border: none !important;
        padding: 8px 12px !important;
    }

    /* ---------- SEND BUTTON ---------- */
    [data-testid="stChatInput"] button {
        background: linear-gradient(90deg, #5E2B97, #E84A9F) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
    }

    [data-testid="stChatInput"] button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(94, 43, 151, 0.4);
    }

    </style>
    """, unsafe_allow_html=True)
