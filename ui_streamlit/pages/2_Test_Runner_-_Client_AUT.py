import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Test Runner – Client AUT",
    page_icon="🧑‍💻",
    layout="wide"
)

st.header("🧑‍💻Test Runner – Client AUT")

with st.sidebar:
    st.header("Test Selection")
    run_button = st.button("▶️ Run Client Tests", use_container_width=True, type="primary")
    selected_tests = st.multiselect("Select tests by marker:", options=["smoke", "regression", "api", "ui"], default=["smoke"])
    st.header("Configuration")
    integration_modes = ['simulated', 'live']
    selected_mode = st.selectbox("Select integration mode:", options=integration_modes, index=0)
    parallel_modes = ['Off', 'Auto', 'Custom']
    parallel_mode = st.selectbox("Parallel execution:", options=parallel_modes, index=0)
    if parallel_mode == 'Custom':
        worker_count = st.number_input("Number of workers:", min_value=2, max_value=16, value=4)

tabs = st.tabs(["Run Client Tests", "See Test Metrics"])

with tabs[0]:
    st.write("## Run Client Tests")
    st.info("Select test markers from the sidebar and click 'Run Client Tests' to begin.")
    # Add logic for running client tests here

with tabs[1]:
    st.write("## See Test Metrics")
    st.info("This page will show widgets and graphs reflecting the last Client's Test run metrics.")
    # Add widgets/graphs for metrics here
