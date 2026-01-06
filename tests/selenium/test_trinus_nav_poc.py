import pytest

# @pytest.mark.trinus
# def test_trinus_nav_poc():
#     pass  # Disabled: Only test_trinus_site_tour should run for Trinus label
import os
import pytest
import time
import datetime
import json
from pathlib import Path

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE = Path(__file__).resolve().parents[2]


def make_run_dir():
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    run_dir = BASE / 'artifacts' / 'trinus' / ts
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir, ts

def test_trinus_open_only(tmp_path):
    # Disabled: Only test_trinus_site_tour should run for Trinus label
    pass
    """
    Simple test: open trinus.com, click Join Trinus CTA, take screenshots, write result.json.
    Attempts to locate all filter elements using multiple locator strategies and tries all click types.
    """
    url = os.environ.get('TRINUS_URL', 'https://trinus.com')

    run_dir, ts = make_run_dir()

    # install chromedriver
    chromedriver_autoinstaller.install()

    opts = Options()
    # allow visible run via TRINUS_VISIBLE
    if not os.environ.get('TRINUS_VISIBLE'):
        # prefer newer headless flag when available
        try:
            opts.add_argument('--headless=new')
        except Exception:
            opts.add_argument('--headless')

    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-web-security')
    opts.add_argument('--allow-running-insecure-content')
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--ignore-ssl-errors')
    opts.add_argument('--ignore-certificate-errors-spki-list')
    opts.add_argument('--ignore-ssl-errors-ignore-untrusted')
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument('--window-size=1366,900')

    driver = webdriver.Chrome(options=opts)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    visited = []
    try:
        # navigate directly to careers page
        # local_html = BASE / 'artifacts' / 'trinus_career.html'
        # url = f'file:///{local_html}'
        url = 'https://trinus.com/career'
        driver.get(url)
        time.sleep(2)  # wait for page load and JS
        print(f"Navigated to: {driver.current_url}")
        # save initial screenshot
        init_shot = run_dir / 'careers.png'
        driver.save_screenshot(str(init_shot))
        visited.append({'step': 0, 'url': driver.current_url, 'screenshot': str(init_shot)})


        # scroll down 350 pixels to reveal filters module
        driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1)
        print("Scrolled 350 pixels")

        # Wait for any select element to be visible (JS-rendered filters)
        try:
            print("Waiting for any <select> element to become visible...")
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, "select")))
            print("A <select> element is now visible.")
        except Exception as e:
            print(f"No <select> element became visible after waiting: {e}")

        # Try to find all filter elements using multiple locator strategies, print their presence/attributes
        print("Locating filter elements using multiple strategies...")
        filter_ids = ["sortorder", "workmodel", "industry", "country", "state", "city", "zip", "radius"]
        for fid in filter_ids:
            try:
                el = driver.find_element(By.ID, fid)
                print(f"Found by ID: {fid} | tag: {el.tag_name} | enabled: {el.is_enabled()} | displayed: {el.is_displayed()}")
            except Exception as e:
                print(f"Not found by ID: {fid} | {e}")
        # Try by name
        filter_names = ["sortorder", "workmodel", "industry", "country", "state", "city", "zip", "radius"]
        for fname in filter_names:
            try:
                el = driver.find_element(By.NAME, fname)
                print(f"Found by NAME: {fname} | tag: {el.tag_name} | enabled: {el.is_enabled()} | displayed: {el.is_displayed()}")
            except Exception as e:
                print(f"Not found by NAME: {fname} | {e}")
        # Try by class
        filter_classes = ["filterBlock", "isATS", "form-control"]
        for fclass in filter_classes:
            try:
                els = driver.find_elements(By.CLASS_NAME, fclass)
                print(f"Found {len(els)} elements by CLASS: {fclass}")
            except Exception as e:
                print(f"Not found by CLASS: {fclass} | {e}")
        # Try by CSS selector
        selectors = [".filterBlock.isATS select", "select.form-control", "#sortorder", "#workmodel", "#industry"]
        for sel in selectors:
            try:
                els = driver.find_elements(By.CSS_SELECTOR, sel)
                print(f"Found {len(els)} elements by CSS: {sel}")
            except Exception as e:
                print(f"Not found by CSS: {sel} | {e}")
        # Try by XPath
        xpaths = ["//select", "//div[contains(@class,'filterBlock')]//select", "//select[@id='sortorder']"]
        for xp in xpaths:
            try:
                els = driver.find_elements(By.XPATH, xp)
                print(f"Found {len(els)} elements by XPATH: {xp}")
            except Exception as e:
                print(f"Not found by XPATH: {xp} | {e}")
        print("Element location attempts complete. No clicks performed.")

        # Try all click types on found filter elements
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        print("\nTrying all click types on filter elements...")
        # Collect all select elements found by previous strategies
        all_selects = set()
        for sel in selectors:
            try:
                for el in driver.find_elements(By.CSS_SELECTOR, sel):
                    all_selects.add(el)
            except Exception:
                pass
        for xp in xpaths:
            try:
                for el in driver.find_elements(By.XPATH, xp):
                    all_selects.add(el)
            except Exception:
                pass
        all_selects = list(all_selects)
        print(f"Total unique select elements found: {len(all_selects)}")
        for idx, el in enumerate(all_selects):
            print(f"\nElement {idx+1}: tag={el.tag_name}, id={el.get_attribute('id')}, name={el.get_attribute('name')}, class={el.get_attribute('class')}")
            # 1. Standard Selenium click
            try:
                el.click()
                print("  - element.click() succeeded")
            except Exception as e:
                print(f"  - element.click() failed: {e}")
            # 2. JavaScript click
            try:
                driver.execute_script("arguments[0].click();", el)
                print("  - JS click succeeded")
            except Exception as e:
                print(f"  - JS click failed: {e}")
            # 3. ActionChains click
            try:
                ActionChains(driver).move_to_element(el).click().perform()
                print("  - ActionChains click succeeded")
            except Exception as e:
                print(f"  - ActionChains click failed: {e}")
            # 4. Send ENTER key
            try:
                el.send_keys(Keys.ENTER)
                print("  - send_keys(Keys.ENTER) succeeded")
            except Exception as e:
                print(f"  - send_keys(Keys.ENTER) failed: {e}")
        print("\nAll click attempts complete.")

        # save screenshot after filter manipulation
        filters_shot = run_dir / 'filters.png'
        driver.save_screenshot(str(filters_shot))
        visited.append({'step': 2, 'url': driver.current_url, 'screenshot': str(filters_shot)})

        # write result.json
        out = {'timestamp': ts, 'start_url': url, 'visited': visited}
        (run_dir / 'result.json').write_text(json.dumps(out, indent=2), encoding='utf-8')

        # simple assertion: ensure we loaded the page and navigated to career
        assert 'trinus' in driver.current_url.lower(), 'Did not load Trinus page'
        assert 'career' in driver.current_url.lower(), 'Did not navigate to career page'
        assert len(visited) == 2, 'Did not complete all steps'

    finally:
        try:
            driver.quit()
        except Exception:
            pass