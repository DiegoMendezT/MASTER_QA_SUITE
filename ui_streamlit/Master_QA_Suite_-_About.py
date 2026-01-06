

import streamlit as st
from datetime import datetime
import pathlib

st.set_page_config(
    page_title="Master QA Suite",
    page_icon="🧪",
    layout="wide"
)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load README.md content
readme_path = pathlib.Path(__file__).parent.parent / "README.md"
with open(readme_path, encoding="utf-8") as f:
    readme_content = f.read()

st.markdown(readme_content, unsafe_allow_html=False)

st.sidebar.success("Select a page above.")
