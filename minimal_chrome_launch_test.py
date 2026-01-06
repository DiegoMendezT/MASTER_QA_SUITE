import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def log(msg):
    print(msg)
    with open('minimal_chrome_launch_log.txt', 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

log('--- MINIMAL CHROME LAUNCH TEST START ---')
try:
    chromedriver_autoinstaller.install()
    opts = Options()
    # Force non-headless for debug
    opts.add_argument('--window-size=800,600')
    log('Attempting to launch Chrome driver (non-headless)...')
    driver = webdriver.Chrome(options=opts)
    log('Chrome driver launched successfully.')
    driver.get('https://www.google.com')
    log('Navigated to Google.')
    driver.quit()
    log('Chrome driver closed successfully.')
except Exception as e:
    log(f'Failed to launch or use Chrome driver: {e}')
