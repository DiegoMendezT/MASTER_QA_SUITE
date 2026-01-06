import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    chromedriver_autoinstaller.install()

    opts = Options()
    # Run visible browser for MVP (no headless arg)
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1400,1000')

    driver = webdriver.Chrome(options=opts)
    out_dir = os.path.join('artifacts', 'trinus_debug')
    os.makedirs(out_dir, exist_ok=True)
    try:
        print('Opening http://localhost:8501')
        driver.get('http://localhost:8501')

        # Wait for main app shell to render (Streamlit mounts into #root)
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        # Give Streamlit extra time for client-side rendering
        time.sleep(3)

    # Save screenshot for inspection (root)
        screenshot_path = os.path.join(out_dir, 'screenshot.png')
        driver.save_screenshot(screenshot_path)
        print('Saved screenshot to', screenshot_path)

        # Save page source after JS render
        dom_path = os.path.join(out_dir, 'page_source.html')
        with open(dom_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('Saved page source to', dom_path)

        # Try to find Trinus Demo elements (may be loaded inside shadow DOMs or iframes)
        try:
            elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Trinus Demo')]")
        except Exception:
            elems = []
        print('Found Trinus Demo:', bool(elems))

        try:
            btns = driver.find_elements(By.XPATH, "//button[contains(., 'Run demo (smoke)')]")
        except Exception:
            btns = []

        if btns:
            print('Clicking Run demo (smoke) button')
            btns[0].click()
        else:
            print('Run demo button not found; page presence is success')

        # If Trinus Demo wasn't found on the root, try navigating to the online demos page from the sidebar
        if not elems:
            try:
                link = driver.find_element(By.XPATH, "//a[.//span[contains(text(), 'Test Runner - Online Demos')]]")
                print('Clicking sidebar link to Test Runner - Online Demos')
                link.click()
                time.sleep(2)
                # Save another screenshot after navigation
                screenshot2 = os.path.join(out_dir, 'screenshot_online_demos.png')
                driver.save_screenshot(screenshot2)
                print('Saved screenshot to', screenshot2)

                # Update page source
                dom2 = os.path.join(out_dir, 'page_source_online_demos.html')
                with open(dom2, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print('Saved page source to', dom2)

                # Re-attempt to find Trinus Demo and button
                elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Trinus Demo')]")
                print('Found Trinus Demo after nav:', bool(elems))
                # On the Online Demos page the primary action is ▶️ Run Tests and there is a
                # 'Headless Mode (no browser windows)' checkbox. Toggle headless off then run.
                try:
                    headless_label = driver.find_element(By.XPATH, "//label[.//p[contains(text(), 'Headless Mode')]]")
                    # Click the label to toggle the checkbox (if present)
                    print('Toggling Headless Mode via label')
                    headless_label.click()
                    time.sleep(0.5)
                except Exception:
                    print('Headless label not found or toggle failed')

                try:
                    run_btn = driver.find_element(By.XPATH, "//button[.//p[contains(text(), 'Run Tests')]]")
                    print('Clicking Run Tests')
                    run_btn.click()
                except Exception:
                    print('Run Tests button not found')
            except Exception as e:
                print('Could not navigate to online demos page:', e)

        time.sleep(5)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
