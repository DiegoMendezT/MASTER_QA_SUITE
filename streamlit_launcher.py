


import glob
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import streamlit as st

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

    for line in iter(process.stdout.readline, ''):
        yield line
    process.stdout.close()
    return_code = process.wait()
    stderr_output = process.stderr.read()
    yield return_code
    yield stderr_output

st.set_page_config(page_title="MASTER QA SUITE Runner", layout="wide")
st.title("🚀 MASTER QA SUITE - Test Runner")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with st.sidebar:
    st.header("Test Selection")
    run_button = st.button("▶️ Run Tests", use_container_width=True, type="primary")
    available_markers = find_pytest_markers()
    selected_markers = st.multiselect(
        "Select tests by marker:",
        options=available_markers,
        default=["ui", "api"]
    )
    st.header("Configuration")
    integration_modes = ['simulated', 'live']
    st.session_state.selected_integration_mode = st.selectbox(
        "Select integration mode:",
        options=integration_modes,
        index=0,
        help="Choose 'simulated' to use mock API data, or 'live' to hit actual API endpoints."
    )
    execution_types = ['Serial Run', 'Parallel Run', 'Custom']
    st.session_state.execution_type = st.selectbox(
        "Execution Type:",
        options=execution_types,
        index=0,
        help="'Parallel Run' uses one worker per CPU core. 'Custom' lets you specify the number."
    )
    if st.session_state.execution_type == 'Custom':
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
    execution_type = st.session_state.get('execution_type', 'Serial Run')
    if execution_type == 'Parallel Run':
        command_parts.extend(["-n", "auto"])
    elif execution_type == 'Custom':
        worker_count = st.session_state.get('worker_count', 2)
        command_parts.extend(["-n", str(worker_count)])
    run_all = 'all' in selected_markers
    filtered_markers = [m for m in selected_markers if m != 'all']
    marker_expression = " or ".join(filtered_markers) if filtered_markers else ""
    if run_all:
        final_marker_expr = None
    else:
        if execution_type != 'Serial Run' and 'serial' not in filtered_markers and marker_expression:
            final_marker_expr = f"({marker_expression}) and not serial"
        else:
            final_marker_expr = marker_expression
    if final_marker_expr:
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
        html_report_path = os.path.abspath(HTML_REPORT)
        st.markdown(f'<a href="file:///{html_report_path}" download target="_blank" style="font-size:1.1em;font-weight:bold;">Download HTML Report</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="file:///{html_report_path}" target="_blank">View HTML Report</a>', unsafe_allow_html=True)
    screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
    if os.path.exists(screenshots_dir):
        screenshots = glob.glob(os.path.join(screenshots_dir, "*.png"))
        if screenshots:
            st.subheader("Test Evidence & Bug Traceability")
            st.caption(f"Evidence files are stored in: `{screenshots_dir}`")
            for screenshot in sorted(screenshots, reverse=True):
                base = os.path.basename(screenshot)
                parts = base.rsplit('_', 3)
                if len(parts) == 4:
                    test_name, date, time, _ = parts
                    timestamp = f"{date} {time[:2]}:{time[2:4]}:{time[4:]}"
                else:
                    test_name = base.replace('_failed.png', '')
                    timestamp = "Unknown"
                jira_ticket_id = test_name.split('-')[0] if '-' in test_name else None
                jira_link = f"https://your-jira-instance/browse/{jira_ticket_id}" if jira_ticket_id else None
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.image(screenshot, caption=f"Test: {test_name}\nTime: {timestamp}")
                with col2:
                    if jira_link:
                        st.markdown(f"[🔗 Jira Ticket]({jira_link})", unsafe_allow_html=True)
                    else:
                        st.write("No Jira link available")
else:
    st.info("Select test markers from the sidebar and click 'Run Tests' to begin.")
st.markdown(
    """
    **Note:** For mobile/remote access, ensure your device is on the same network as the test server and use the Network URL shown above.
    """,
    unsafe_allow_html=True
)
