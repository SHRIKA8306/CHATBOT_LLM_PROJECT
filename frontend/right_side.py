import streamlit as st

def show_right_sidebar():
    st.markdown('<div class="right-sidebar-container">', unsafe_allow_html=True)

    st.markdown("### Women's Safety Resources")

    # Emergency Helplines
    with st.expander("Emergency Helplines"):
        st.markdown("""
        - Police: 100  
        - Women Helpline (181)  
        - Child Helpline: 1098  
        - Anti-Trafficking: 1091  
        """)

    # Laws
    with st.expander("Laws and Rights for Women"):
        st.markdown("""
        - IPC 375: Rape laws  
        - IPC 354: Assault on women  
        - Domestic Violence Act 2005  
        - Protection of Women from Sexual Harassment Act 2013  
        - Right to live with dignity  
        - Right to equality  
        - Right against domestic violence  
        - Right to file a complaint against harassment  
        """)

    st.markdown("</div>", unsafe_allow_html=True)

