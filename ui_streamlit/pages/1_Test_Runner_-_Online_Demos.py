
import glob
import os
import subprocess
from datetime import datetime
import streamlit as st

# --- Set Streamlit Page Config FIRST ---
st.set_page_config(
    page_title="Test Runner – Online Demos",
    page_icon="🚀",
    layout="wide"
)

# --- Configuration ---
TEST_DIR = "tests"
REPORTS_DIR = "reports"
ARTIFACTS_DIR = "artifacts"
HTML_REPORT = os.path.join(REPORTS_DIR, "report.html")

# --- Helper Functions ---
def find_pytest_markers():
    markers = ["all"]
    try:
        with open("pytest.ini", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(("[", "#", ";")) and ":" in line:
                    marker = line.split(":")[0].strip()
                    markers.append(marker)
    except FileNotFoundError:
        st.error("pytest.ini not found. Cannot determine test markers.")
    return sorted(list(set(markers)))

def run_pytest(command):
    import time
    import platform
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
        encoding='utf-8',
        bufsize=1
    )
    st.session_state['test_process'] = process
    st.session_state['log_output'] = ""
    st.session_state['return_code'] = None
    st.session_state['stderr_output'] = ""
    st.session_state['stop_requested'] = False

    log_placeholder = st.empty()
    log_output = ""
    while True:
        if st.session_state.get('stop_requested', False):
            try:
                if platform.system() == "Windows":
                    os.system(f"taskkill /F /T /PID {process.pid}")
                else:
                    process.terminate()
            except Exception:
                pass
            break
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None:
                break
            time.sleep(0.1)
            continue
        log_output += line
        st.session_state['log_output'] = log_output
        log_placeholder.code(log_output, language="log")
        time.sleep(0.05)
    process.stdout.close()
    return_code = process.wait()
    stderr_output = process.stderr.read()
    st.session_state['test_process'] = None
    st.session_state['return_code'] = return_code
    st.session_state['stderr_output'] = stderr_output
    st.session_state['stop_requested'] = False
    return process


st.header("🚀 Test Runner – Online Demos")

with st.sidebar:
    st.header("Test Selection")
    available_markers = find_pytest_markers()
    selected_markers = st.multiselect(
        "Select tests by marker:",
        options=available_markers,
        default=["ui", "api"]
    )
    st.header("Configuration")
    execution_modes = [
        'Serial Run (1 worker)',
        'Parallel Custom Run',
        'Parallel Run (8 workers)'
    ]
    execution_mode = st.selectbox(
        "Execution Mode:",
        options=execution_modes,
        index=0,
        help="Choose how tests are executed. 'Parallel Custom Run' lets you specify the number of workers."
    )
    worker_count = 4
    if execution_mode == 'Parallel Custom Run':
        worker_count = st.number_input("Number of workers:", min_value=2, max_value=16, value=4)
    integration_modes = ['Live API Endpoints', 'Simulated API Endpoints']
    selected_integration_mode = st.selectbox(
        "Integration Mode:",
        options=integration_modes,
        index=0,
        help="Choose 'Simulated API Endpoints' to use mock API data, or 'Live API Endpoints' to hit actual API endpoints."
    )
    # Move headless checkbox directly above the Run/Stop button
    headless_mode = st.checkbox(
        "Headless Mode (no browser windows)",
        value=True,
        help="When checked, browsers run in headless mode (no UI). Uncheck to see browser windows."
    )
    # Use a single key for the button and always sync label to process state
    if 'test_process' not in st.session_state:
        st.session_state['test_process'] = None
    # Safety: If process is set but not running, clear it
    process = st.session_state['test_process']
    if process is not None:
        try:
            # Try psutil if available
            try:
                import psutil
                if not psutil.pid_exists(process.pid):
                    st.session_state['test_process'] = None
            except ImportError:
                # Fallback: use process.poll()
                if process.poll() is not None:
                    st.session_state['test_process'] = None
        except Exception:
            st.session_state['test_process'] = None
    test_running = st.session_state['test_process'] is not None
    run_button = st.button(
        "⏹️ Stop Test Run" if test_running else "▶️ Run Tests",
        use_container_width=True,
        type="primary",
        key="run_stop_button"
    )

tabs = st.tabs(["Run Online Demo Tests", "See Test Metrics"])

with tabs[0]:
    # Handle test run start/stop
    if run_button:
        if not test_running:
            # Start test run in background
            marker_expression = " or ".join(selected_markers) if selected_markers else ""
            if not marker_expression:
                st.warning("No markers selected. Please select at least one marker to run tests.")
                st.stop()
            integration_mode_cli = 'live' if selected_integration_mode == 'Live API Endpoints' else 'simulated'
            command_parts = [
                f"C:/Users/USUARIO/Projects/MASTER_QA_SUITE/.venv/Scripts/python.exe",
                "-m", "pytest", "-v",
                f"--html={HTML_REPORT}", "--self-contained-html",
                f"--integration-mode={integration_mode_cli}"
            ]
            if headless_mode:
                command_parts.append("--headless")
            if execution_mode == 'Serial Run (1 worker)':
                command_parts.extend(["-n", "1"])
            elif execution_mode == 'Parallel Run (8 workers)':
                command_parts.extend(["-n", "8"])
            elif execution_mode == 'Parallel Custom Run':
                command_parts.extend(["-n", str(worker_count)])
            if execution_mode != 'Serial Run (1 worker)' and 'serial' not in selected_markers:
                final_marker_expr = f"({marker_expression}) and not serial"
            else:
                final_marker_expr = marker_expression
            command_parts.extend(["-m", f'"{final_marker_expr}"'])
            command = " ".join(command_parts)
            st.session_state['log_output'] = ""
            st.session_state['return_code'] = None
            st.session_state['stderr_output'] = ""
            run_pytest(command)
            st.rerun()  # Force UI to update button and log placeholders
        else:
            # Stop test run
            st.session_state['stop_requested'] = True
            st.warning("Test run stopped by user.")
            st.rerun()

    # Always show logs/results if available
    st.header("Test Execution")
    log_output = st.session_state.get('log_output', "")
    return_code = st.session_state.get('return_code', None)
    stderr_output = st.session_state.get('stderr_output', "")
    log_placeholder = st.empty()
    if log_output:
        log_placeholder.code(log_output, language="log")
    if stderr_output:
        st.subheader("Errors from Test Runner")
        st.error(stderr_output)
    if return_code is not None:
        st.info(f"**Pytest Exit Code:** `{return_code}`")
        if return_code == 0:
            st.success("Test run completed successfully.")
        else:
            st.error("Test run finished with errors. See logs and report for details.")
    if os.path.exists(HTML_REPORT):
        with open(HTML_REPORT, "r", encoding="utf-8") as f:
            st.download_button("Download HTML Report", f, file_name="test_report.html")
        st.markdown(f'<a href="file:///{os.path.abspath(HTML_REPORT)}" target="_blank">View HTML Report</a>', unsafe_allow_html=True)
    screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
    if os.path.exists(screenshots_dir):
        screenshots = glob.glob(os.path.join(screenshots_dir, "*.png"))
        if screenshots:
            st.subheader("\U0001F4F7 Screenshots on Failure")
            for screenshot in screenshots:
                st.image(screenshot, caption=os.path.basename(screenshot))
    if not log_output and not test_running:
        st.info("Select test markers from the sidebar and click 'Run Tests' to begin.")
