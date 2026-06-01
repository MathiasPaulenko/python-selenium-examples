# -*- coding: utf-8 -*-
"""
Implicit Waits examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/waits/

An implicit wait is a global setting that applies to every element location
call for the entire session. When set, the driver will wait up to the given
duration before returning a NoSuchElementException.

Key characteristics:
    - Set once, applies globally to all find_element/find_elements calls.
    - Default value is 0 (fail immediately if element not found).
    - As soon as the element is found the driver continues — no fixed delay.
    - Can be set via driver method or via timeouts capability in browser options.

WARNING:
    Do NOT mix implicit and explicit waits in the same session.
    Doing so can cause unpredictable and compounding wait times.
    For example, implicit=10s + explicit=15s could timeout at 20s.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

DYNAMIC_PAGE = 'https://www.selenium.dev/selenium/web/dynamic.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Set implicit wait via driver method
# ---------------------------------------------------------------------------

def implicit_wait_via_driver():
    """
    Set implicit wait using driver.implicitly_wait().
    The driver will poll for up to 2 seconds before raising NoSuchElementException.
    """
    driver = _build_driver()
    driver.implicitly_wait(2)  # seconds
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'adder').click()
    # Without implicit wait this would fail immediately; with it the driver
    # retries until the element appears or the timeout is reached.
    added = driver.find_element(By.ID, 'box0')
    print(f'Element class: {added.get_attribute("class")}')

    driver.quit()


def implicit_wait_via_options():
    """
    Set implicit wait via the timeouts capability in ChromeOptions.
    Equivalent to driver.implicitly_wait() but declared at session creation.
    """
    options = webdriver.ChromeOptions()
    options.timeouts = {'implicit': 2000}  # milliseconds in capabilities

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'adder').click()
    added = driver.find_element(By.ID, 'box0')
    print(f'Element class: {added.get_attribute("class")}')

    driver.quit()


def implicit_wait_zero_default():
    """
    Demonstrate the default behavior (implicit wait = 0):
    driver raises NoSuchElementException immediately if element is not present.
    """
    driver = _build_driver()
    # No implicit wait set — default is 0
    driver.get(DYNAMIC_PAGE)
    driver.find_element(By.ID, 'adder').click()

    try:
        # The new element may not be in the DOM yet — this can fail immediately.
        driver.find_element(By.ID, 'box0')
        print('Element found (may have loaded fast enough)')
    except Exception as exc:
        print(f'Expected failure with no wait: {type(exc).__name__}')
    finally:
        driver.quit()


def implicit_wait_reset():
    """
    Reset implicit wait back to 0 mid-session.
    Useful to disable it for specific lookups without rebuilding the driver.
    """
    driver = _build_driver()
    driver.implicitly_wait(5)  # global 5-second wait
    driver.get(DYNAMIC_PAGE)

    # ... do work with the 5s implicit wait ...

    driver.implicitly_wait(0)  # reset to default (no wait)
    # Subsequent find_element calls will fail immediately if element not present.

    driver.quit()


if __name__ == '__main__':
    implicit_wait_via_driver()
