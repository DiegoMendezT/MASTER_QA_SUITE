import os
import subprocess
import sys
import streamlit as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.task_prioritizer import Task, prioritize, _load_tasks


def run_tests_ui():
    st.set_page_config(layout="wide")
    st.title("MASTER QA SUITE :: Task Prioritizer")

    # --- Main Columns ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Test Execution")

        # --- Engine Selection ---
        engine = st.selectbox("Test Engine", ["Selenium", "Playwright"], index=0)
        
        # --- Worker Selection ---
        workers = st.slider("Parallel Workers", min_value=1, max_value=os.cpu_count() or 1, value=2)
        
        # --- Browser & Engine-Specific Options ---
        if engine == "Selenium":
            browser = st.selectbox("Browser", ["chrome", "firefox", "edge"], index=0)
            login_mode = st.radio(
                "Login Method",
                ["UI Login", "API+Cookie Login"],
                index=0,
                horizontal=True
            )
            headless = st.checkbox("Run Headless", value=True)
            sauce = st.checkbox("Run on Sauce Labs", value=False)
        
        elif engine == "Playwright":
            browser = st.selectbox("Browser", ["chromium", "firefox", "webkit"], index=0)
            headless = st.checkbox("Run Headless", value=True)
            # Set Selenium-specific options to defaults that won't interfere
            login_mode = "N/A"
            sauce = False

        # --- Marker Selection ---
        markers = st.text_input("Markers (e.g., 'smoke and not slow')")

        # --- Test Path Selection ---
        test_path = st.text_input("Test Path", "tests/")

        # --- Environment Variables ---
        with st.expander("Environment Variables"):
            env_vars_str = st.text_area("Enter as KEY=VALUE pairs, one per line")

        if st.button("Run Tests", use_container_width=True):
            env = os.environ.copy()

            # Base command
            cmd = f"pytest {test_path} -n {workers}"

            # Engine-specific command building
            if engine == "Selenium":
                cmd += f" --login-mode='{login_mode}'"
                env["BROWSER"] = browser
                if headless:
                    env["QA_HEADLESS"] = "1"
                if sauce:
                    env["SAUCE_USERNAME"] = os.getenv("SAUCE_USERNAME", "")
                    env["SAUCE_ACCESS_KEY"] = os.getenv("SAUCE_ACCESS_KEY", "")
            
            elif engine == "Playwright":
                cmd += f" --browser {browser}"
                # The --headless flag for pytest-playwright is a store_true action,
                # so it doesn't take an argument. We just add it if the box is checked.
                if headless:
                    cmd += " --headless"

            if markers:
                cmd += f" -m '{markers}'"
            
            for line in env_vars_str.splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()

            st.code(f"Running command: {cmd}", language="bash")
            
            # Live log output
            log_placeholder = st.empty()
            log_output = ""
            
            try:
                process = subprocess.Popen(
                    cmd, 
                    shell=True, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env,
                    bufsize=1,
                    universal_newlines=True
                )
                
                for line in process.stdout:
                    log_output += line
                    log_placeholder.text_area("Live Test Output", log_output, height=400)
                
                process.wait()
                
                if process.returncode == 0:
                    st.success("Tests completed successfully!")
                else:
                    st.error(f"Tests failed with exit code {process.returncode}.")

            except Exception as e:
                st.error(f"An error occurred while running tests: {e}")

    with col2:
        st.header("Task Prioritizer")


        # --- Strategy Selection ---
        strategies = ["wsjf", "rice", "linear"]
        strategy = st.selectbox("Scoring Strategy", strategies, index=0)

        if st.button(f"Prioritize with '{strategy.upper()}'", use_container_width=True):
            try:
                tasks = _load_tasks()
                recommended_tasks = prioritize(tasks, strategy=strategy, top=5, explain=True)

                st.success(f"Top 5 Recommendations using '{strategy}' strategy:")

                if not recommended_tasks:
                    st.info("No tasks to prioritize or all tasks are blocked.")

                for i, task in enumerate(recommended_tasks, 1):
                    score = task._explain.get("total", 0.0)
                    with st.expander(f"{i}. {task.name} (Score: {score:.2f})"):
                        st.markdown(f"**ID:** `{task.id}` | **Status:** `{task.status}`")
                        st.json(task._explain)
                        if getattr(task, "depends_on", None):
                            st.markdown(f"**Dependencies:** `{', '.join(task.depends_on)}`")

            except FileNotFoundError:
                st.error("Error: A required configuration file (`roadmap_phase2.yml` or `backlog.yml`) was not found.")
            except ValueError as ve:
                st.error(f"Configuration Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

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
