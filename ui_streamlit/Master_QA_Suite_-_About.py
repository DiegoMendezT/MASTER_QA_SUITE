
import streamlit as st
from datetime import datetime
import os
import glob

st.write('**[DEBUG] Current working directory:**', os.getcwd())
st.write('**[DEBUG] Script location:**', os.path.abspath(__file__))
pages_dir = os.path.join(os.path.dirname(__file__), 'pages')
page_files = glob.glob(os.path.join(pages_dir, '*.py'))
st.write('**[DEBUG] .py files in pages folder:**', [os.path.basename(f) for f in page_files])

st.set_page_config(
    page_title="Master QA Suite",
    page_icon="🧪",
    layout="wide"
)

st.title("Master QA Suite")
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
