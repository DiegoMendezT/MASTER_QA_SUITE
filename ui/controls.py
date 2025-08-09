import streamlit as st
import subprocess
import os
import sys

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.innercouncil import InnerCouncil

def run_tests_ui():
    st.set_page_config(layout="wide")
    st.title("MASTER QA SUITE :: InnerCouncil Runner")

    # --- Main Columns ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Test Execution")
        
        # --- Worker Selection ---
        workers = st.slider("Parallel Workers", min_value=1, max_value=os.cpu_count() or 1, value=2)
        
        # --- Browser Selection ---
        browser = st.selectbox("Browser", ["chrome", "firefox", "edge"], index=0)
        
        # --- Login Mode Selection ---
        login_mode = st.radio(
            "Login Method",
            ["UI Login", "API+Cookie Login"],
            index=0,
            horizontal=True
        )

        # --- Headless Mode ---
        headless = st.checkbox("Run Headless", value=True)

        # --- Sauce Labs Toggle ---
        sauce = st.checkbox("Run on Sauce Labs", value=False)

        # --- Marker Selection ---
        markers = st.text_input("Markers (e.g., 'smoke and not slow')")

        # --- Test Path Selection ---
        test_path = st.text_input("Test Path", "tests/")

        # --- Environment Variables ---
        with st.expander("Environment Variables"):
            env_vars_str = st.text_area("Enter as KEY=VALUE pairs, one per line")

        if st.button("Run Tests", use_container_width=True):
            cmd = f"pytest {test_path} -n {workers} --login-mode='{login_mode}'"
            if markers:
                cmd += f" -m '{markers}'"
            
            env = os.environ.copy()
            env["BROWSER"] = browser
            if headless:
                env["QA_HEADLESS"] = "1"
            if sauce:
                env["SAUCE_USERNAME"] = os.getenv("SAUCE_USERNAME", "")
                env["SAUCE_ACCESS_KEY"] = os.getenv("SAUCE_ACCESS_KEY", "")
            
            for line in env_vars_str.splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()

            st.code(f"Running command: {cmd}", language="bash")
            
            try:
                process = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    check=True,
                    env=env
                )
                st.text_area("Test Output", process.stdout, height=400)
                st.success("Tests completed successfully!")
            except subprocess.CalledProcessError as e:
                st.text_area("Test Output", e.stdout + e.stderr, height=400)
                st.error("Tests failed.")

    with col2:
        st.header("InnerCouncil")
        
        if st.button("Let InnerCouncil Decide", use_container_width=True):
            council = InnerCouncil()
            next_task, score = council.decide_next_task()
            if 'error' in next_task:
                st.error(next_task['error'])
            else:
                st.success(f"Next Task: **{next_task['name']}**")
                st.info(f"Score: **{score:.2f}** (ROI: {next_task['roi']}, Complexity: {next_task['complexity']}, Learning: {next_task['learning']})")

        st.header("Documentation")
        if st.button("Sync Docs", use_container_width=True):
            st.write("Running documentation sync...")
            try:
                result = subprocess.run(
                    f"{sys.executable} tools/sync_docs.py",
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True
                )
                st.text_area("Sync Output", result.stdout, height=200)
                st.success("Documentation synced!")
            except subprocess.CalledProcessError as e:
                st.text_area("Sync Output", e.stdout + e.stderr, height=200)
                st.error("Documentation sync failed.")

if __name__ == "__main__":
    run_tests_ui()
