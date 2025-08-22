
import streamlit as st
import subprocess
import threading
import time
import queue
import os
import sys

# --- Ensure session state keys are initialized at the top ---
if 'stop_flag' not in st.session_state:
    st.session_state['stop_flag'] = False
if 'proc' not in st.session_state:
    st.session_state['proc'] = None
if 'log' not in st.session_state:
    st.session_state['log'] = ""
if 'log_thread' not in st.session_state:
    st.session_state['log_thread'] = None
if 'log_buffer' not in st.session_state:
    st.session_state['log_buffer'] = None

def reset_runner_state():
    st.session_state['proc'] = None
    st.session_state['log_thread'] = None
    st.session_state['log_buffer'] = None
    st.session_state['stop_flag'] = False
    st.session_state['test_finished'] = True

COMMAND = [sys.executable, '-m', 'pytest', 'ui_streamlit/pages', '--maxfail=1', '--disable-warnings', '-v']

# Log streaming thread (writes to a thread-safe queue, not session_state)
def log_streamer(proc, log_buffer, timeout=60):
    start_time = time.time()
    try:
        while proc.poll() is None and not st.session_state.get('stop_flag', False):
            # Timeout check
            if time.time() - start_time > timeout:
                log_buffer.put("[Process timed out after 60 seconds]\n")
                try:
                    proc.terminate()
                except Exception:
                    pass
                break
            line = proc.stdout.readline()
            if not line:
                time.sleep(0.1)
                continue
            log_buffer.put(line)
        # Read any remaining output
        for line in proc.stdout:
            log_buffer.put(line)
    except Exception as e:
        log_buffer.put(f"[Log streamer error: {e}]\n")
    # Signal end of log
    log_buffer.put(None)


# --- UI Button Logic ---
if 'test_finished' not in st.session_state:
    st.session_state['test_finished'] = False

if st.session_state['proc'] is not None:
    # Show Stop button when running
    stop_clicked = st.button("Stop Test Run", type="primary")
    if stop_clicked:
        st.session_state['stop_flag'] = True
        try:
            import platform, os
            if platform.system() == "Windows":
                os.system(f"taskkill /F /T /PID {st.session_state['proc'].pid}")
            else:
                st.session_state['proc'].terminate()
        except Exception:
            pass
        reset_runner_state()
        st.session_state['log'] += "\n[Stopped by user]\n"
        st.rerun()
else:
    # Show Run button when not running
    run_clicked = st.button("Run Test", type="primary")
    if run_clicked:
        st.session_state['log'] = ""
        st.session_state['stop_flag'] = False
        st.session_state['test_finished'] = False
        # Set working directory to project root
        workdir = os.path.abspath(os.path.dirname(__file__) + '/../../')
        try:
            # Check if pytest is importable
            import importlib.util
            if importlib.util.find_spec('pytest') is None:
                st.session_state['log'] = "[Pytest is not installed in this environment. Please install pytest in your venv.]\n"
                st.session_state['proc'] = None
                st.session_state['log_buffer'] = None
                st.session_state['log_thread'] = None
                st.session_state['test_finished'] = True
                st.rerun()
                st.stop()
            proc = subprocess.Popen(
                COMMAND,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                cwd=workdir
            )
        except Exception as e:
            st.session_state['log'] = f"[Failed to start process: {e}]\n"
            st.session_state['proc'] = None
            st.session_state['log_buffer'] = None
            st.session_state['log_thread'] = None
            st.session_state['test_finished'] = True
            st.rerun()
            st.stop()
        st.session_state['proc'] = proc
        log_buffer = queue.Queue()
        st.session_state['log_buffer'] = log_buffer
        t = threading.Thread(target=log_streamer, args=(proc, log_buffer, 60), daemon=True)
        st.session_state['log_thread'] = t
        t.start()
        st.rerun()

# --- Main thread: collect log lines from buffer and update session_state['log'] ---
if st.session_state['log_buffer'] is not None:
    log_lines = 0
    while True:
        try:
            line = st.session_state['log_buffer'].get_nowait()
        except queue.Empty:
            break
        if line is None:
            # End of log
            if log_lines == 0:
                st.session_state['log'] += "\n[No output captured. Pytest may not have run, or no tests were found.]\n"
            st.session_state['log'] += "\n[Test finished]\n"
            reset_runner_state()
            break
        # Filter out 'The process ... not found.'
        if "The process" in line and "not found" in line:
            continue
        st.session_state['log'] += line
        log_lines += 1




st.subheader("Live Log Output")
if st.session_state['log']:
    st.code(st.session_state['log'], language="log")
else:
    st.warning("No output yet. If you see no output after running, pytest may not be running or no tests were found.")
st.caption(":information_source: If you see 'missing ScriptRunContext!' warnings, they are safe to ignore (Streamlit background thread warning).")

if st.session_state['proc'] is not None:
    st.info("Test is running...")
elif st.session_state.get('test_finished', False):
    st.success("Test finished.")
else:
    st.success("Test is not running.")
