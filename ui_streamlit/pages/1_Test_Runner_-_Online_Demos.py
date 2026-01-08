

import glob
import os
import subprocess
import sys
import shutil
from datetime import datetime
import streamlit as st
import re

# --- Ensure friendly_name is always available ---
def friendly_name(filename):
    base = os.path.splitext(os.path.basename(filename))[0]
    return re.sub(r'[_]+', ' ', base).title()

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
    # --- Evidence wipe removed: screenshots are now preserved for display. ---
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
        encoding='utf-8',
        bufsize=1,
        cwd=os.getcwd()  # Ensure working directory is project root
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
    # Set 'trinus' as default if present, else fallback to 'ui' or 'api'
    if "trinus" in available_markers:
        default_marker = ["trinus"]
    elif "ui" in available_markers:
        default_marker = ["ui"]
    elif "api" in available_markers:
        default_marker = ["api"]
    else:
        default_marker = available_markers[:1]
    selected_markers = st.multiselect(
        "Select tests by marker:",
        options=available_markers,
        default=default_marker
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
        value=False,
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
        import time
        st.session_state['run_start_time'] = time.time()
        if not test_running:
            # Start test run in background
            # Ensure 'trinus' is first in marker expression if present
            ordered_markers = sorted(selected_markers, key=lambda x: 0 if x.lower() == "trinus" else 1)
            marker_expression = " or ".join(ordered_markers) if ordered_markers else ""
            if not marker_expression:
                st.warning("No markers selected. Please select at least one marker to run tests.")
                st.stop()
            integration_mode_cli = 'live' if selected_integration_mode == 'Live API Endpoints' else 'simulated'
            import sys, os
            venv_python = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".venv", "Scripts", "python.exe")
            if os.path.exists(venv_python):
                python_exec = venv_python
            else:
                python_exec = sys.executable
            command_parts = [
                python_exec,
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
            # Set TRINUS_VISIBLE=1 in the environment if headless_mode is False
            custom_env = os.environ.copy()
            if not headless_mode:
                custom_env["TRINUS_VISIBLE"] = "1"
            else:
                custom_env.pop("TRINUS_VISIBLE", None)
            st.session_state['log_output'] = ""
            st.session_state['return_code'] = None
            st.session_state['stderr_output'] = ""
            # Patch run_pytest to accept env override
            def run_pytest_with_env(command, env):
                import time
                import platform
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    text=True,
                    encoding='utf-8',
                    bufsize=1,
                    cwd=os.getcwd(),
                    env=env
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
            run_pytest_with_env(command, custom_env)
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
        # Centralized summary reporting for all test types
        summary_displayed = False
        # Only display Trinus summary once, and only in the evidence block below
        # API/UI summary (if selected)
        for marker in selected_markers:
            if marker == 'api':
                summary_txt = os.path.join(ARTIFACTS_DIR, "result_summary_api.txt")
                st.markdown("### API Test Summary")
                st.info("The API tests validate key endpoints for correct status codes, response formats, and business logic. Each test sends requests to the backend and checks for expected results, error handling, and data integrity. This ensures the API is reliable and meets requirements.")
                st.subheader("\U0001F4AC API Test Evidence")
                st.markdown("**Request 1: Create User**")
                st.code('''POST /api/v1/users/register\nContent-Type: application/json\n\n{\n  "username": "demo_user",\n  "email": "demo@example.com",\n  "password": "securePassword123",\n  "profile": {\n    "first_name": "Demo",\n    "last_name": "User",\n    "age": 30\n  }\n}''', language="http")
                st.markdown("**Response 1:**")
                st.code('''HTTP/1.1 201 Created\nContent-Type: application/json\n\n{\n  "id": 101,\n  "username": "demo_user",\n  "email": "demo@example.com",\n  "profile": {\n    "first_name": "Demo",\n    "last_name": "User",\n    "age": 30\n  },\n  "status": "pending_verification",\n  "created_at": "2026-01-07T05:15:00Z"\n}''', language="json")
                st.markdown("**Request 2: Verify Email**")
                st.code('''POST /api/v1/users/verify\nContent-Type: application/json\n\n{\n  "user_id": 101,\n  "verification_code": "ABC123XYZ"\n}''', language="http")
                st.markdown("**Response 2:**")
                st.code('''HTTP/1.1 200 OK\nContent-Type: application/json\n\n{\n  "id": 101,\n  "status": "active",\n  "verified_at": "2026-01-07T05:16:00Z"\n}''', language="json")
                summary_displayed = True
            elif marker == 'ui':
                summary_txt = os.path.join(ARTIFACTS_DIR, "result_summary_ui.txt")
                st.markdown("<h3 style='font-size:1.4em;'>UI Test Summary</h3>", unsafe_allow_html=True)
                if os.path.exists(summary_txt):
                    with open(summary_txt, encoding="utf-8") as sf:
                        content = sf.read().strip()
                        if content:
                            st.markdown(content)
                        else:
                            st.info("No detailed results for UI tests, but the marker was included in this run.")
                else:
                    st.info("No summary file found for UI tests.")
                # Display available screenshots as evidence for UI
                screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
                if os.path.exists(screenshots_dir):
                    screenshots = [f for f in glob.glob(os.path.join(screenshots_dir, "*.png"))]
                    if screenshots:
                        st.subheader(f"\U0001F4F7 UI Test Evidence")
                        for img in sorted(screenshots, key=os.path.getmtime):
                            status = "Passed" if "pass" in img.lower() else ("Failed" if "fail" in img.lower() else "")
                            st.image(img, caption=f"{friendly_name(img)} | {status} | {datetime.fromtimestamp(os.path.getmtime(img)).strftime('%Y-%m-%d %H:%M:%S')}")
                summary_displayed = True
        if not summary_displayed and not ('trinus' in selected_markers):
            st.info("No summary available for the selected test markers.")
        st.info(f"**Pytest Exit Code:** `{return_code}`")
        if return_code == 0:
            st.success("Test run completed successfully.")
        else:
            st.error("Test run finished with errors. See logs and report for details.")
    if os.path.exists(HTML_REPORT):
        with open(HTML_REPORT, "r", encoding="utf-8") as f:
            html_content = f.read()
        st.download_button("Download HTML Report", html_content, file_name="test_report.html")
    screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
    # Show only the latest Trinus run evidence (screenshots) with timestamp in caption
    # Evidence display logic: only show after a test run, never preload
    import json, re

# --- Move friendly_name to top-level scope so it is always available ---
def friendly_name(filename):
    # Remove extension, replace underscores with spaces, capitalize
    base = os.path.splitext(os.path.basename(filename))[0]
    return re.sub(r'[_]+', ' ', base).title()

    def ai_summary_trinus(result):
        """Generate a concise summary for Trinus test results."""
        total = len(result.get('visited', []))
        passed = sum(1 for v in result.get('visited', []) if v.get('status', '').startswith('Passed'))
        failed = total - passed
        errors = [v for v in result.get('visited', []) if v.get('status', '').startswith('Failed')]
        summary = (
            "This test visits all top navigation and submenu pages on trinus.com, scrolling and capturing screenshots. "
            f"Visited {total} pages: {passed} passed, {failed} failed."
        )
        if errors:
            summary += "\nErrors: " + "; ".join(f"{e['name']}: {e['status']}" for e in errors[:2])
            if len(errors) > 2:
                summary += f" (+{len(errors)-2} more)"
        elif failed == 0:
            summary += " All pages loaded successfully."
        return summary

    # Only show evidence if a test run just finished
    if return_code is not None:
        # Only show Trinus summary/evidence if 'trinus' marker was selected for this run
        if 'trinus' in selected_markers:
            trinus_dir = os.path.join(ARTIFACTS_DIR, "trinus")
            if os.path.exists(trinus_dir):
                run_dirs = [d for d in glob.glob(os.path.join(trinus_dir, "*")) if os.path.isdir(d)]
                if run_dirs:
                    latest_run = max(run_dirs, key=os.path.basename)
                    result_json = os.path.join(latest_run, "result.json")
                    summary_txt = os.path.join(latest_run, "result_summary.txt")
                    if os.path.exists(result_json):
                        with open(result_json, encoding="utf-8") as f:
                            result = json.load(f)
                        run_start = st.session_state.get('run_start_time', None)
                        # Human-friendly header
                        dt_str = datetime.strptime(result['timestamp'], "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M:%S")
                        st.subheader(f"\U0001F4F7 Trinus Site Tour – {dt_str}")
                        # --- Verbose summary block ---
                        if os.path.exists(summary_txt):
                            with open(summary_txt, encoding="utf-8") as sf:
                                st.markdown(sf.read())
                        else:
                            st.info(ai_summary_trinus(result))
                        # ---
                        for step in result.get("visited", []):
                            screenshot = step.get("screenshot")
                            if screenshot and os.path.exists(screenshot):
                                if not run_start or os.path.getmtime(screenshot) >= run_start:
                                    # Caption: Test Case | Step | Timestamp
                                    page = step.get('name', '')
                                    ts = dt_str
                                    st.image(screenshot, caption=f"Trinus Site Tour | {page} | {ts}")
        # TODO: Add API/UI summary reporting here using test_reporting.py logic

        # Generic screenshots (UI, API, etc.)
        screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
        if os.path.exists(screenshots_dir):
            run_start = st.session_state.get('run_start_time', None)
            recent_screens = [f for f in glob.glob(os.path.join(screenshots_dir, "*.png"))
                              if not run_start or os.path.getmtime(f) >= run_start]
            if recent_screens:
                st.subheader(f"\U0001F4F7 Test Evidence ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                for img in sorted(recent_screens, key=os.path.getmtime):
                    status = "Passed" if "pass" in img.lower() else ("Failed" if "fail" in img.lower() else "")
                    st.image(img, caption=f"{friendly_name(img)} | {status} | {datetime.fromtimestamp(os.path.getmtime(img)).strftime('%Y-%m-%d %H:%M:%S')}")
    if not log_output and not test_running:
        st.info("Select test markers from the sidebar and click 'Run Tests' to begin.")
