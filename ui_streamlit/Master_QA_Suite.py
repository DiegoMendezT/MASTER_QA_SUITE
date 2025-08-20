import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="🧪 Master QA Suite",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Master QA Suite")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown(
    """
    Welcome to the MASTER QA SUITE!
    
    **👈 Select a page from the sidebar** to get started.
    
    This suite helps you run, monitor, and analyze your automated tests with ease.
    
    ### Quick Start
    - Use the sidebar to navigate between the Test Runner and other tools.
    - Each page will show its own controls in the sidebar.
    
    ### Need help?
    - Check the documentation
    - Contact the QA team
    """
)

st.sidebar.success("Select a page above.")
