

import glob
import os
import subprocess
import sys
import shutil
from datetime import datetime
import streamlit as st

# --- Set Streamlit Page Config FIRST ---
st.set_page_config(
    page_title="Test Runner – Online Demos",
    page_icon="🚀",
    layout="wide"
)

st.markdown(
    """
    <style>
        .demo-label {
            font-size: 50px !important;
            font-weight: 900 !important;
            letter-spacing: 0.08em !important;
            margin: 0.2rem 0 0.5rem 0 !important;
            line-height: 1.05 !important;
            color: #f0f2f6 !important;
        }
        .demo-story {
            font-size: 1.08rem !important;
            line-height: 1.8 !important;
            color: #e6edf7 !important;
            max-width: 1200px !important;
        }
        div[data-testid="stMarkdownContainer"] h3 {
            font-size: 2.1rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMarkdownContainer"] p {
            line-height: 1.75 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Configuration ---
TEST_DIR = "tests"
REPORTS_DIR = "reports"
ARTIFACTS_DIR = "artifacts"
HTML_REPORT = os.path.join(REPORTS_DIR, "report.html")
RUN_ID_KEY = "active_run_id"
DEMO_MVP_MARKERS = ["superbaterias", "ui", "api"]
LEGACY_BATERIAS_MARKERS = {"bateriascostaricacr", "superbaterias"}

# --- Helper Functions ---
def make_run_id():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%S%fZ")


def filter_current_evidence(file_paths, run_start_time=None, selected_markers=None):
    """Keep only artifacts from the active run and the selected marker set."""
    selected_markers = [m.lower() for m in (selected_markers or [])]
    if not file_paths:
        return []

    filtered = []
    for file_path in file_paths:
        if not file_path or not os.path.exists(file_path):
            continue

        if run_start_time is not None:
            try:
                if os.path.getmtime(file_path) < run_start_time:
                    continue
            except OSError:
                continue

        name = os.path.basename(file_path).lower()
        if not selected_markers:
            filtered.append(file_path)
            continue

        matches = False
        if "all" in selected_markers:
            matches = True
        selected_baterias_markers = {"superbaterias", "bateriascostaricacr"}.intersection(selected_markers)
        if selected_baterias_markers:
            is_ui_baterias_artifact = name.startswith("ui_") and "baterias" in name.lower()
            is_real_baterias_artifact = (
                "superbaterias_" in name
                or name.lower().startswith("superbaterias_")
                or "bateriascostaricacr_" in name
                or name.lower().startswith("bateriascostaricacr_")
                or ("baterias" in name and "ui_test" not in name)
                or ("superbaterias" in name and "ui_test" not in name)
            )
            matches = matches or is_real_baterias_artifact
            if is_ui_baterias_artifact:
                matches = False
        if "trinus" in selected_markers:
            matches = matches or "trinus" in name
        if "ui" in selected_markers:
            is_ui_artifact = name.startswith("ui_") or "ui_test" in name
            matches = matches or is_ui_artifact
        if "api" in selected_markers:
            matches = matches or "api" in name

        if matches:
            filtered.append(file_path)

    return sorted(set(filtered), key=lambda p: os.path.getmtime(p))


def collect_run_screenshots(base_dir, run_start_time=None, selected_markers=None):
    """Recursively collect screenshot evidence, keeping only files from the active run and selected markers."""
    if not base_dir or not os.path.isdir(base_dir):
        return []

    image_exts = (".png", ".jpg", ".jpeg", ".webp")
    collected = []
    for root, _, files in os.walk(base_dir):
        for filename in files:
            candidate = os.path.join(root, filename)
            if not filename.lower().endswith(image_exts):
                continue
            collected.append(candidate)

    return filter_current_evidence(collected, run_start_time=run_start_time, selected_markers=selected_markers)


def should_show_baterias_summary(selected_markers=None):
    selected_markers = [m.lower() for m in (selected_markers or [])]
    if not selected_markers:
        return False
    return bool(set(selected_markers).intersection(LEGACY_BATERIAS_MARKERS))


def default_demo_markers(available_markers=None):
    available = [m.lower() for m in (available_markers or [])]
    selected = []
    for marker in DEMO_MVP_MARKERS:
        if marker in available:
            selected.append(marker)
    if selected:
        return selected
    fallback = [m for m in available if m != "all"]
    return fallback[:1]


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


def clear_evidence_folders():
    for path in [ARTIFACTS_DIR, os.path.join(ARTIFACTS_DIR, "screenshots"), os.path.join(ARTIFACTS_DIR, "trinus")]:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
        except Exception:
            pass
    for pattern in [os.path.join(ARTIFACTS_DIR, "*.png"), os.path.join(ARTIFACTS_DIR, "*.jpg"), os.path.join(ARTIFACTS_DIR, "*.jpeg")]:
        for stale_file in glob.glob(pattern):
            try:
                os.remove(stale_file)
            except Exception:
                pass
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(ARTIFACTS_DIR, "screenshots"), exist_ok=True)
    os.makedirs(os.path.join(ARTIFACTS_DIR, "trinus"), exist_ok=True)

    run_id = st.session_state.get(RUN_ID_KEY)
    if run_id:
        run_dir = os.path.join(ARTIFACTS_DIR, "screenshots", run_id)
        os.makedirs(run_dir, exist_ok=True)


def collect_test_files_for_markers(selected_markers):
    if not selected_markers:
        return []
    selected_lower = {m.lower() for m in selected_markers}
    files = set()
    if "all" in selected_lower:
        return ["tests"]
    if "ui" in selected_lower:
        files.update(sorted(glob.glob(os.path.join("tests", "ui", "test_*.py"))))
    if "api" in selected_lower:
        files.update(sorted(glob.glob(os.path.join("tests", "api", "test_*.py"))))
    if "superbaterias" in selected_lower or "bateriascostaricacr" in selected_lower or "trinus" in selected_lower:
        files.add(os.path.join("tests", "ui", "test_homepage_screenshot_cases.py"))
    return sorted(files)


def run_pytest(command):
    import time
    import platform
    clear_evidence_folders()
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
    default_marker = default_demo_markers(available_markers)
    selected_markers = st.multiselect(
        "Select tests by marker:",
        options=available_markers,
        default=default_marker
    )
    demo_case = None
    if "superbaterias" in selected_markers:
        demo_case = "superbaterias"
    elif "bateriascostaricacr" in selected_markers:
        demo_case = "bateriascostaricacr"
    elif "trinus" in selected_markers:
        demo_case = "trinus"
    else:
        demo_case = "superbaterias"

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
        st.session_state[RUN_ID_KEY] = make_run_id()
        st.session_state['selected_markers'] = selected_markers
        if not test_running:
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

            test_files = collect_test_files_for_markers(selected_markers)
            if not test_files:
                st.warning("No test files matched the selected markers.")
                st.stop()

            command_parts = [
                python_exec,
                "-m", "pytest", "-v",
                *test_files,
                f"--html={HTML_REPORT}", "--self-contained-html",
                f"--integration-mode={integration_mode_cli}"
            ]
            if headless_mode:
                command_parts.append("--headless")
            if demo_case:
                command_parts.extend(["--demo-case", demo_case])
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
            if final_marker_expr:
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
    active_run_id = st.session_state.get(RUN_ID_KEY, "n/a")
    st.caption(f"Active run ID: {active_run_id}")
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
            html_content = f.read()
        st.download_button("Download HTML Report", html_content, file_name="test_report.html")
        st.markdown(f'<a href="file:///{os.path.abspath(HTML_REPORT)}" target="_blank">View HTML Report</a>', unsafe_allow_html=True)
    screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
    import json, re
    def friendly_name(filename):
        base = os.path.splitext(os.path.basename(filename))[0]
        return re.sub(r'[_]+', ' ', base).title()

    def show_homepage_screenshot_evidence(recent_screens):
        if not recent_screens:
            return

        ordered_images = sorted(set(recent_screens), key=lambda p: os.path.getmtime(p))
        def is_real_baterias_image(path):
            name = os.path.basename(path).lower()
            return (
                "superbaterias_" in name
                or "bateriascostaricacr_" in name
                or ("superbaterias" in name and "ui_test" not in name and "trinus" not in name)
                or ("baterias" in name and "ui_test" not in name and "trinus" not in name)
            )

        def is_ui_image(path):
            name = os.path.basename(path).lower()
            return name.startswith("ui_") or "ui_test" in name

        baterias_images = [img for img in ordered_images if is_real_baterias_image(img)]
        ui_images = [img for img in ordered_images if is_ui_image(img)]
        other_images = [img for img in ordered_images if img not in baterias_images and img not in ui_images]

        st.caption(f"Mostrando {len(ordered_images)} capturas creadas en esta ejecución.")

        if baterias_images:
            st.markdown('<div class="demo-label">BATERIAS</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="demo-story">
                <h3>Qué es</h3>
                Este caso valida la experiencia real de un cliente en una tienda que vende baterías y energía. El crawler no es solo un script técnico: es una comprobación ligera pero poderosa de la salud del sitio. Revisa si la home carga, si las landing pages principales responden, si las imágenes aparecen, si los enlaces funcionan y si la navegación se siente estable y esperada.
                <br><br>
                <h3>Qué podría ser</h3>
                Esto puede convertirse en una verificación automatizada y programada cada mañana. El sistema puede visitar las páginas clave, validar los links, comprobar secciones críticas y enviar un resumen breve por correo al equipo, o incluso dispararse desde un job programado en Jenkins o en cualquier pipeline de automatización. Así deja de ser solo una prueba manual y se vuelve una señal diaria de operación del negocio.
                <br><br>
                <h3>Valor adicional</h3>
                Además, este caso es muy útil para negocio y para operación. Sirve para detectar fallas antes de que las sienta el cliente, protege la confianza en la marca, mejora la experiencia de compra y convierte QA en una capa de monitoreo y riesgo. Es un ejemplo claro de cómo una validación técnica puede aportar valor comercial y operativo real.
                </div>
                """,
                unsafe_allow_html=True,
            )
            for img in baterias_images:
                filename = os.path.basename(img)
                caption_base = filename.replace("superbaterias_", "").replace("bateriascostaricacr_", "").replace("_", " ").replace(".png", "")
                caption = caption_base.title()
                if caption_base == "home":
                    caption = "Home"
                st.image(img, caption=f"{caption} | {filename} | {datetime.fromtimestamp(os.path.getmtime(img)).strftime('%Y-%m-%d %H:%M:%S')}")

        if ui_images:
            st.markdown('<div class="demo-label">UI</div>', unsafe_allow_html=True)
            for img in ui_images:
                filename = os.path.basename(img)
                st.image(img, caption=f"UI Evidence | {filename} | {datetime.fromtimestamp(os.path.getmtime(img)).strftime('%Y-%m-%d %H:%M:%S')}")
        elif "ui" in selected_markers:
            st.markdown('<div class="demo-label">UI</div>', unsafe_allow_html=True)
            st.info("No screenshots were generated for the selected UI tests in this run.")

        if other_images:
            st.subheader("📸 Additional Evidence")
            for img in other_images:
                filename = os.path.basename(img)
                label = "Trinus" if "trinus" in filename.lower() else friendly_name(filename)
                st.image(img, caption=f"{label} | {filename} | {datetime.fromtimestamp(os.path.getmtime(img)).strftime('%Y-%m-%d %H:%M:%S')}")

        st.caption(f"Evidence folder: {os.path.abspath(screenshots_dir)}")

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
        screenshots_dir = os.path.join(ARTIFACTS_DIR, "screenshots")
        run_start = st.session_state.get('run_start_time', None)
        all_screen_files = collect_run_screenshots(
            screenshots_dir,
            run_start_time=run_start,
            selected_markers=selected_markers,
        )
        recent_screens = all_screen_files
        st.caption(f"Evidence scope: active run {active_run_id} | selected markers: {', '.join(selected_markers) if selected_markers else 'none'}")
        if recent_screens:
            show_homepage_screenshot_evidence(recent_screens)

        if "api" in selected_markers:
            st.markdown('<div class="demo-label">API</div>', unsafe_allow_html=True)
            api_summary = []
            for line in log_output.splitlines():
                lowered = line.lower()
                if "api" in lowered or "health check" in lowered or "retrieved" in lowered or "created post" in lowered or "updated post" in lowered or "deleted post" in lowered or "error handling" in lowered:
                    api_summary.append(line.strip())
            if api_summary:
                for line in api_summary[-12:]:
                    st.write(line)
            else:
                st.info("No API-specific evidence was emitted in the log output for this run.")

        if "trinus" in selected_markers:
            trinus_dir = os.path.join(ARTIFACTS_DIR, "trinus")
            if os.path.exists(trinus_dir):
                run_dirs = [d for d in glob.glob(os.path.join(trinus_dir, "*")) if os.path.isdir(d)]
                if run_dirs and any(os.path.exists(os.path.join(d, "result.json")) for d in run_dirs):
                    latest_run = max(run_dirs, key=os.path.basename)
                    result_json = os.path.join(latest_run, "result.json")
                    summary_txt = os.path.join(latest_run, "result_summary.txt")
                    if os.path.exists(result_json):
                        with open(result_json, encoding="utf-8") as f:
                            result = json.load(f)
                        dt_str = datetime.strptime(result['timestamp'], "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M:%S")
                        st.subheader(f"\U0001F4F7 Trinus Site Tour – {dt_str}")
                        if os.path.exists(summary_txt):
                            with open(summary_txt, encoding="utf-8") as sf:
                                st.markdown(sf.read())
                        else:
                            st.info(ai_summary_trinus(result))
                        for step in result.get("visited", []):
                            screenshot = step.get("screenshot")
                            if screenshot and os.path.exists(screenshot):
                                if not run_start or os.path.getmtime(screenshot) >= run_start:
                                    page = step.get('name', '')
                                    st.image(screenshot, caption=f"Trinus Site Tour | {page} | {dt_str}")
    if not log_output and not test_running:
        st.info("Select test markers from the sidebar and click 'Run Tests' to begin.")
