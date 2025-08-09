import streamlit as st
import subprocess
import os
import json

def run_tests_ui():
    st.title("Master QA Suite Runner")
    
    st.sidebar.title("Test Execution Config")
    
    # --- Worker Selection ---
    workers = st.sidebar.slider("Parallel Workers", min_value=1, max_value=os.cpu_count() or 1, value=2)
    
    # --- Browser Selection ---
    browser = st.sidebar.selectbox("Browser", ["chrome", "firefox", "edge"], index=0)
    
    # --- Login Mode Selection ---
    login_mode = st.sidebar.radio(
        "Login Method",
        ["UI Login", "API+Cookie Login"],
        index=0
    )

    # --- Headless Mode ---
    headless = st.sidebar.checkbox("Run Headless", value=True)

    # --- Sauce Labs Toggle ---
    sauce = st.sidebar.checkbox("Run on Sauce Labs", value=False)

    # --- Marker Selection ---
    markers = st.sidebar.text_input("Markers (e.g., 'smoke and not slow')")

    # --- Test Path Selection ---
    test_path = st.sidebar.text_input("Test Path", "tests/")

    # --- Environment Variables ---
    st.sidebar.subheader("Environment Variables")
    env_vars_str = st.sidebar.text_area("Enter as KEY=VALUE pairs, one per line")

    if st.button("Run Tests"):
        cmd = f"pytest {test_path} -n {workers} --login-mode='{login_mode}'"
        if markers:
            cmd += f" -m '{markers}'"
        
        # Set environment variables
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

        st.write(f"Running command: `{cmd}`")
        
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

    # --- Docs Sync Button ---
    if st.sidebar.button("Sync Docs"):
        st.write("Running documentation sync...")
        try:
            result = subprocess.run(
                "python tools/sync_docs.py",
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            st.text(result.stdout)
            st.success("Documentation synced!")
        except subprocess.CalledProcessError as e:
            st.text(e.stdout + e.stderr)
            st.error("Documentation sync failed.")

if __name__ == "__main__":
    run_tests_ui()
