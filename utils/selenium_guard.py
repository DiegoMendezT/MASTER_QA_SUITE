# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: selenium_guard.py
# Purpose: Selenium-specific wait and guard utilities for robust UI automation.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 14:00 UTC
#
# Agile Voice Attribution (Full Team):
# - Product Owner, Scrum Master, Development Team, Stakeholders, Subject Matter Experts
# - QA Voice: [Diego Alejandro], Shadow QA: [Diego's Shadow]
# - Teacher as Copilot, Gatekeeper as Copilot, Release Captain
#
# All major changes must be attributed in docs/decision_log.md.

from __future__ import annotations

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        StaleElementReferenceException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .flaky_guard import retry_on

WAIT_DEFAULT = 10

def _wait(driver: WebDriver, condition, timeout: int = WAIT_DEFAULT):
    return WebDriverWait(driver, timeout).until(condition)

def wait_visible(driver: WebDriver, locator: tuple[str, str], timeout: int = WAIT_DEFAULT) -> WebElement:
    return _wait(driver, EC.visibility_of_element_located(locator), timeout)

def wait_clickable(driver: WebDriver, locator: tuple[str, str], timeout: int = WAIT_DEFAULT) -> WebElement:
    return _wait(driver, EC.element_to_be_clickable(locator), timeout)

@retry_on((StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException))
def guard_click(driver: WebDriver, locator: tuple[str, str], timeout: int = WAIT_DEFAULT) -> None:
    el = wait_clickable(driver, locator, timeout)
    try:
        el.click()
    except (ElementClickInterceptedException, ElementNotInteractableException, WebDriverException):
        # Fallback JS click when native click is blocked by overlays/modals
        driver.execute_script("arguments[0].click();", el)

@retry_on((StaleElementReferenceException, ElementNotInteractableException, TimeoutException))
def guard_type(driver: WebDriver, locator: tuple[str, str], text: str, clear: bool = True, timeout: int = WAIT_DEFAULT) -> None:
    el = wait_visible(driver, locator, timeout)
    if clear:
        try:
            el.clear()
        except WebDriverException:
            driver.execute_script("arguments[0].value='';", el)
    el.send_keys(text)

@retry_on((StaleElementReferenceException, TimeoutException))
def guard_get_text(driver: WebDriver, locator: tuple[str, str], timeout: int = WAIT_DEFAULT) -> str:
    el = wait_visible(driver, locator, timeout)
    return el.text

@retry_on((StaleElementReferenceException, TimeoutException))
def guard_find(driver: WebDriver, locator: tuple[str, str], timeout: int = WAIT_DEFAULT) -> WebElement:
    return wait_visible(driver, locator, timeout)
