"""
Streamlit Test Runner for MASTER QA SUITE

This application provides a simple UI for selecting and running pytest tests,
viewing live output, and accessing reports and artifacts.
"""

import glob
import os
import subprocess
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# --- Configuration ---
TEST_DIR = "tests"
REPORTS_DIR = "reports"
ARTIFACTS_DIR = "artifacts"
HTML_REPORT = os.path.join(REPORTS_DIR, "report.html")

# --- Helper Functions ---
def find_pytest_markers():
    """
    Parses pytest.ini to find all registered markers.
    This is a simple parser; a more robust one might use configparser.
    """
    markers = ["all"] # 'all' is a default option
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
    """
    Runs a pytest command in a subprocess and yields its output in real-time.
    Returns the final return code and any stderr output.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
        encoding='utf-8',
        bufsize=1
    )
    
    # Yield stdout lines as they come
    for line in iter(process.stdout.readline, ''):
        yield line
    
    process.stdout.close()
    
    # Wait for the process to finish and get the return code and stderr
    return_code = process.wait()
    stderr_output = process.stderr.read()
    
    yield return_code
    yield stderr_output

# --- Streamlit UI ---
st.set_page_config(page_title="MASTER QA SUITE Runner", layout="wide")

st.title("🚀 MASTER QA SUITE - Test Runner")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Sidebar for Test Selection ---

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
    # Integration mode selector
    integration_modes = ['simulated', 'live']
    st.session_state.selected_integration_mode = st.selectbox(
        "Select integration mode:",
        options=integration_modes,
        index=0, # Default to 'simulated'
        help="Choose 'simulated' to use mock API data, or 'live' to hit actual API endpoints."
    )

    # Execution type selector (Serial, Parallel, Custom)
    execution_types = ['Serial Run', 'Parallel Run', 'Custom']
    st.session_state.execution_type = st.selectbox(
        "Execution Type:",
        options=execution_types,
        index=0, # Default to 'Serial Run'
        help="'Parallel Run' uses one worker per CPU core. 'Custom' lets you specify the number."
    )
    if st.session_state.execution_type == 'Custom':
        st.session_state.worker_count = st.number_input("Number of workers:", min_value=2, max_value=16, value=4)


# --- Main Content Area ---
if run_button:
    st.header("Test Execution")
    
    # Build the pytest command
    marker_expression = " or ".join(selected_markers) if selected_markers else ""
    if not marker_expression:
        st.warning("No markers selected. Please select at least one marker to run tests.")
        st.stop()

    # Base command
    command_parts = [
        f"C:/Users/USUARIO/Projects/MASTER_QA_SUITE/.venv/Scripts/python.exe",
        "-m", "pytest", "-v",
        f"--html={HTML_REPORT}", "--self-contained-html",
        f"--integration-mode={st.session_state.get('selected_integration_mode', 'simulated')}"
    ]

    # Handle execution type (JIRA-003 fix: Serial Run disables all parallelism)
    execution_type = st.session_state.get('execution_type', 'Serial Run')
    if execution_type == 'Parallel Run':
        command_parts.extend(["-n", "auto"])
    elif execution_type == 'Custom':
        worker_count = st.session_state.get('worker_count', 2)
        command_parts.extend(["-n", str(worker_count)])
    elif execution_type == 'Serial Run':
        # Explicitly ensure no -n is present and add --maxfail=1 for clarity
        command_parts = [p for p in command_parts if p != "-n"]
        command_parts.append("--maxfail=1")
    # If 'Off', do NOT add '-n' (serial execution)

    run_all = 'all' in selected_markers
    # Remove 'all' from marker list if present
    filtered_markers = [m for m in selected_markers if m != 'all']
    marker_expression = " or ".join(filtered_markers) if filtered_markers else ""

    # Handle marker expression, excluding 'serial' if running in parallel
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
    st.caption(f"Execution type: {execution_type} (JIRA-003: Serial Run disables all parallelism)")

    log_placeholder = st.empty()
    log_output = ""

    with st.spinner("Tests are running..."):
        return_code = None
        stderr_output = ""
        
        try:
            # The generator now yields stdout lines, then the return code, then stderr
            runner = run_pytest(command)
            
            # Process stdout
            for line in runner:
                if isinstance(line, str):
                    log_output += line
                    log_placeholder.code(log_output, language="log")
                else:
                    # First non-string is the return code
                    return_code = line
                    break
            
            # The last item yielded is stderr
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
    
    # Link to HTML report (fixed: use Streamlit-native widgets)

    if os.path.exists(HTML_REPORT):
        st.markdown("---")
        st.subheader("Test Report")
        col1, col2 = st.columns([1, 3])
        with col1:
            with open(HTML_REPORT, "rb") as f:
                html_bytes = f.read()
            st.download_button(
                label="⬇️ Download HTML Report",
                data=html_bytes,
                file_name="report.html",
                mime="text/html",
                use_container_width=True,
                key="download_html_report"
            )
        with col2:
            with open(HTML_REPORT, "r", encoding="utf-8") as f:
                html_content = f.read()
            st.markdown("<div style='background:#222;border-radius:8px;padding:0.5em 1em 1em 1em;margin-top:0.5em;'>", unsafe_allow_html=True)
            st.markdown("<b>Preview (scrollable):</b>", unsafe_allow_html=True)
            components.html(html_content, height=500, scrolling=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.caption("If the inline preview does not render, open the downloaded file in your browser.")

    # Placeholder for Export to Jira (future feature)
    st.button("Export Selected Bugs to Jira (Coming Soon)", disabled=True)

    # List screenshots
    screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
    if os.path.exists(screenshots_dir):
        screenshots = glob.glob(os.path.join(screenshots_dir, "*.png"))
        if screenshots:
            st.subheader("Test Evidence & Bug Traceability")
            st.caption(f"Evidence files are stored in: `{screenshots_dir}`")
            for screenshot in sorted(screenshots, reverse=True):
                base = os.path.basename(screenshot)
                # Parse filename: testname_YYYYMMDD_HHMMSS_failed.png
                parts = base.rsplit('_', 3)
                if len(parts) == 4:
                    test_name, date, time, _ = parts
                    timestamp = f"{date} {time[:2]}:{time[2:4]}:{time[4:]}"
                else:
                    test_name = base.replace('_failed.png', '')
                    timestamp = "Unknown"
                
                # Assuming Jira ticket ID is part of the filename, e.g., TEST-123_...
                jira_ticket_id = test_name.split('-')[0] if '-' in test_name else None
                jira_link = f"https://your-jira-instance/browse/{jira_ticket_id}" if jira_ticket_id else None

                # Display screenshot with test name, timestamp, and Jira link
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

        # --- Display Network URL for remote/mobile access (JIRA-010) ---
    import socket
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        port = 8505  # Default Streamlit port, update if dynamic
        network_url = f"http://{local_ip}:{port}"
    except Exception:
        network_url = "[Could not determine network URL]"
    st.markdown(
        f"<span style='color:#43a047; font-size:18px; font-weight:700;'>Network URL: <span style='background:#e3f2fd; padding:2px 8px; border-radius:6px;'>{network_url}</span></span>",
        unsafe_allow_html=True,
    )
    st.caption("Use this URL on your mobile or remote device (same network required). Tutorial will guide you.")

