"""
Accessibility (a11y) Utilities for MASTER QA SUITE

This module provides helper functions to inject and run the axe-core
accessibility testing engine in the browser.
"""
import json
import logging

from selenium.webdriver.remote.webdriver import WebDriver

AXE_CORE_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.3/axe.min.js"

def inject_axe(driver: WebDriver):
    """
    Injects the axe-core script into the current page.

    Args:
        driver: The Selenium WebDriver instance.
    """
    try:
        script_content = f"var script = document.createElement('script'); script.src = '{AXE_CORE_CDN_URL}'; document.head.appendChild(script);"
        driver.execute_script(script_content)
        # Give the script a moment to load
        driver.execute_script("return typeof window.axe !== 'undefined';")
        logging.info("axe-core script injected successfully.")
    except Exception as e:
        logging.error(f"Failed to inject axe-core script: {e}")
        raise

def run_axe(driver: WebDriver, context: str = None, options: dict = None) -> list:
    """
    Runs axe-core on the current page and returns any violations.

    Args:
        driver: The Selenium WebDriver instance.
        context: Optional. A CSS selector for the element to analyze.
                 If None, the entire document is analyzed.
        options: Optional. A dictionary of axe-core configuration options.
                 See https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#options-parameter

    Returns:
        A list of accessibility violations found by axe-core.
        Returns an empty list if no violations are found or if axe is not present.
    """
    if driver.execute_script("return typeof window.axe === 'undefined';"):
        logging.warning("axe-core not injected. Skipping accessibility scan.")
        return []

    # Serialize context and options for the script
    context_arg = json.dumps(context) if context else 'undefined'
    options_arg = json.dumps(options) if options else 'undefined'

    # This script runs axe.run and waits for the promise to resolve
    axe_script = f"""
    const context = {context_arg};
    const options = {options_arg};
    const callback = arguments[arguments.length - 1];
    
    axe.run(context, options)
        .then(results => callback(results))
        .catch(err => callback({{ 'error': err.toString() }}));
    """
    
    try:
        results = driver.execute_async_script(axe_script)
        if 'error' in results:
            logging.error(f"An error occurred while running axe: {results['error']}")
            return []
        
        violations = results.get('violations', [])
        if violations:
            logging.warning(f"Found {len(violations)} accessibility violations.")
        else:
            logging.info("No accessibility violations found by axe-core.")
            
        return violations
    except Exception as e:
        logging.error(f"Failed to execute axe-core script: {e}")
        return []
