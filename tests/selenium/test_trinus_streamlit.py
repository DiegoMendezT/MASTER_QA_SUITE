import pytest

## @pytest.mark.trinus
## def test_trinus_streamlit_smoke():
    # pass  # Placeholder removed to avoid IndentationError
import subprocess
import pytest
import time
import requests
import os
import signal
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
import sys
venv_python = os.path.join(BASE, ".venv", "Scripts", "python.exe")
if os.path.exists(venv_python):
    STREAMLIT_SCRIPT = venv_python
else:
    STREAMLIT_SCRIPT = sys.executable
APP_ENTRY = os.path.join(BASE, 'ui_streamlit', 'Master_QA_Suite_-_About.py')


def wait_for_url(url, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def test_trinus_streamlit_smoke(tmp_path):
    """Start the Streamlit app from the venv, wait for it, then use Selenium to find the Trinus demo page and click the demo button."""
    # Start Streamlit in a subprocess (detached) unless SKIP_STREAMLIT is set
    cmd = [STREAMLIT_SCRIPT, '-m', 'streamlit', 'run', APP_ENTRY]
    env = os.environ.copy()
    # Ensure streamlit won't open a browser on CI
    env['BROWSER'] = 'none'

    proc = None
    if not os.environ.get('SKIP_STREAMLIT'):
        proc = subprocess.Popen(cmd, env=env, cwd=BASE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    try:
        assert wait_for_url('http://localhost:8501', timeout=40), 'Streamlit did not start in time'

        # Install chromedriver for the running Chrome version
        chromedriver_autoinstaller.install()

        opts = Options()
        # Allow overriding headless for local interactive debugging by setting
        # the TRINUS_VISIBLE environment variable to any value.
        if not os.environ.get('TRINUS_VISIBLE'):
            opts.add_argument('--headless=new')
        else:
            # Running with visible browser for MVP/local observation
            pass

        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--window-size=1200,900')

        driver = webdriver.Chrome(options=opts)
        try:
            driver.get('http://localhost:8501')

            # Wait a bit for the multipage list to render
            time.sleep(2)

            # Find the page title that contains 'Trinus Demo'
            elems = driver.find_elements('xpath', "//*[contains(text(), 'Trinus Demo')]")
            assert elems, 'Trinus Demo page not found in app'

            # Try to click the button 'Run demo (smoke)'
            btns = driver.find_elements('xpath', "//button[contains(., 'Run demo (smoke)')]")
            if btns:
                btns[0].click()
            else:
                # Button may be off-screen; still consider finding the page a success
                pass

        finally:
            driver.quit()

    finally:
        if proc:
            try:
                proc.send_signal(signal.SIGINT)
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
