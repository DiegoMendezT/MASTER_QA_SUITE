"""Run a lightweight smoke test against https://trinus.com.

Steps:
- HTTP GET the site and extract <title>
- If selenium + chromedriver available, open the page in headless Chrome and save a screenshot
- Write a result JSON under artifacts/trinus/<timestamp>/result.json
"""
from pathlib import Path
import requests
import re
import datetime
import json
import os

BASE = Path(__file__).resolve().parents[1]

def http_check(url: str = "https://trinus.com"):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "MasterQA/1.0 (smoke)"})
        title_m = re.search(r"<title>(.*?)</title>", r.text, re.I | re.S)
        title = title_m.group(1).strip() if title_m else ""
        return {"ok": True, "status_code": r.status_code, "title": title}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def selenium_screenshot(url: str, run_dir: Path):
    try:
        import chromedriver_autoinstaller
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
    except Exception as e:
        return {"ok": False, "error": f"import_error: {e}"}

    try:
        chromedriver_autoinstaller.install()
    except Exception as e:
        return {"ok": False, "error": f"chromedriver_install: {e}"}

    opts = Options()
    # Use the newer headless mode when available
    try:
        opts.add_argument('--headless=new')
    except Exception:
        opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1200,900')

    try:
        driver = webdriver.Chrome(options=opts)
    except Exception as e:
        return {"ok": False, "error": f"webdriver_launch: {e}"}

    try:
        driver.get(url)
        time.sleep(2)
        shot = run_dir / 'screenshot.png'
        driver.save_screenshot(str(shot))
        return {"ok": True, "screenshot": str(shot)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        try:
            driver.quit()
        except Exception:
            pass


def main():
    url = os.environ.get('TRINUS_URL', 'https://trinus.com')
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    run_dir = BASE / 'artifacts' / 'trinus' / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    result = {"timestamp": ts, "url": url}
    http = http_check(url)
    result['http'] = http

    # attempt selenium screenshot
    selenium = selenium_screenshot(url, run_dir)
    result['selenium'] = selenium

    out_file = run_dir / 'result.json'
    out_file.write_text(json.dumps(result, indent=2), encoding='utf-8')

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
