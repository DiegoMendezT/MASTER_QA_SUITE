
import glob
import os
import subprocess
from datetime import datetime
import streamlit as st

# --- Set Streamlit Page Config FIRST ---
st.set_page_config(
    page_title="🚀 Test Runner – Online Demos",
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
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
        encoding='utf-8',
        bufsize=1
    )
    for line in iter(process.stdout.readline, ''):
        yield line
    process.stdout.close()
    return_code = process.wait()
    stderr_output = process.stderr.read()
    yield return_code
    yield stderr_output

# --- Sidebar for Test Selection ---
st.set_page_config(
    page_title="🚀 Test Runner – Online Demos",
    page_icon="🚀",
    layout="wide"
)

st.header("🚀 Test Runner – Online Demos")
with st.sidebar:
    st.header("Test Selection")
    available_markers = find_pytest_markers()
    selected_markers = st.multiselect(
        "Select tests by marker:",
        options=available_markers,
        default=["ui", "api"]
    )
    run_button = st.button("▶️ Run Tests", use_container_width=True, type="primary")
    st.header("Configuration")
    integration_modes = ['simulated', 'live']
    st.session_state.selected_integration_mode = st.selectbox(
        "Select integration mode:",
        options=integration_modes,
        index=0,
        help="Choose 'simulated' to use mock API data, or 'live' to hit actual API endpoints."
    )
    parallel_modes = ['Off', 'Auto', 'Custom']
    st.session_state.parallel_mode = st.selectbox(
        "Parallel execution:",
        options=parallel_modes,
        index=0,
        help="'Auto' uses one worker per CPU core. 'Custom' lets you specify the number."
    )
    if st.session_state.parallel_mode == 'Custom':
        st.session_state.worker_count = st.number_input("Number of workers:", min_value=2, max_value=16, value=4)

if run_button:
    st.header("Test Execution")
    marker_expression = " or ".join(selected_markers) if selected_markers else ""
    if not marker_expression:
        st.warning("No markers selected. Please select at least one marker to run tests.")
        st.stop()
    command_parts = [
        f"C:/Users/USUARIO/Projects/MASTER_QA_SUITE/.venv/Scripts/python.exe",
        "-m", "pytest", "-v",
        f"--html={HTML_REPORT}", "--self-contained-html",
        f"--integration-mode={st.session_state.get('selected_integration_mode', 'simulated')}"
    ]
    parallel_mode = st.session_state.get('parallel_mode', 'Off')
    if parallel_mode == 'Auto':
        command_parts.extend(["-n", "auto"])
    elif parallel_mode == 'Custom':
        worker_count = st.session_state.get('worker_count', 2)
        command_parts.extend(["-n", str(worker_count)])
    if parallel_mode != 'Off' and 'serial' not in selected_markers:
        final_marker_expr = f"({marker_expression}) and not serial"
    else:
        final_marker_expr = marker_expression
    command_parts.extend(["-m", f'"{final_marker_expr}"'])
    command = " ".join(command_parts)
    st.info(f"**Running command:** `{command}`")
    log_placeholder = st.empty()
    log_output = ""
    with st.spinner("Tests are running..."):
        return_code = None
        stderr_output = ""
        try:
            runner = run_pytest(command)
            for line in runner:
                if isinstance(line, str):
                    log_output += line
                    log_placeholder.code(log_output, language="log")
                else:
                    return_code = line
                    break
            stderr_output = next(runner, "")
        except Exception as e:
            st.error(f"An error occurred while running pytest: {e}")
            log_placeholder.code(log_output, language="log")
    st.header("📊 Results & Artifacts")
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
            st.subheader("📷 Screenshots on Failure")
            for screenshot in screenshots:
                st.image(screenshot, caption=os.path.basename(screenshot))
else:
    st.info("Select test markers from the sidebar and click 'Run Tests' to begin.")
