import streamlit as st
import subprocess
import os

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

    if st.button("Run All Tests"):
        cmd = f"pytest -n {workers} --login-mode='{login_mode}'"
        
        # Set environment variable for browser selection
        env = os.environ.copy()
        env["BROWSER"] = browser
        
        st.write(f"Running command: `{cmd}` with BROWSER={browser}")
        
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

if __name__ == "__main__":
    run_tests_ui()
