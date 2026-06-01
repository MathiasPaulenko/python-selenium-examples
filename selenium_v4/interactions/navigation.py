# -*- coding: utf-8 -*-
"""
Browser navigation examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/interactions/navigation/

Topics covered:
    - Navigate to URL (driver.get and driver.navigate().to equivalent)
    - Back
    - Forward
    - Refresh
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SELENIUM_URL = 'https://www.selenium.dev/'
INDEX_URL = 'https://www.selenium.dev/selenium/web/index.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Navigate to URL
# ---------------------------------------------------------------------------

def navigate_to():
    """
    Navigate to a URL using driver.get().
    This is the standard way to load a page in Selenium.
    """
    driver = _build_driver()

    driver.get(SELENIUM_URL)
    print(f'Navigated to: {driver.current_url}')

    driver.quit()


def navigate_to_multiple():
    """
    Navigate to multiple URLs sequentially in the same session.
    Each call to get() waits for the page to finish loading.
    """
    driver = _build_driver()

    driver.get(SELENIUM_URL)
    print(f'First URL: {driver.current_url}')

    driver.get(INDEX_URL)
    print(f'Second URL: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Back
# ---------------------------------------------------------------------------

def navigate_back():
    """
    Press the browser's back button to go to the previous page in history.
    Equivalent to clicking the back arrow in the browser UI.
    """
    driver = _build_driver()

    driver.get(SELENIUM_URL)
    driver.get(INDEX_URL)
    print(f'Before back: {driver.current_url}')

    driver.back()
    print(f'After back: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Forward
# ---------------------------------------------------------------------------

def navigate_forward():
    """
    Press the browser's forward button to go to the next page in history.
    Only works if the driver has previously navigated back.
    """
    driver = _build_driver()

    driver.get(SELENIUM_URL)
    driver.get(INDEX_URL)
    driver.back()
    print(f'After back: {driver.current_url}')

    driver.forward()
    print(f'After forward: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Refresh
# ---------------------------------------------------------------------------

def navigate_refresh():
    """
    Reload the current page, equivalent to pressing F5 or Ctrl+R.
    Useful to test page state after reload or to clear dynamic content.
    """
    driver = _build_driver()

    driver.get(INDEX_URL)
    print(f'Before refresh: {driver.title}')

    driver.refresh()
    print(f'After refresh: {driver.title}')

    driver.quit()


def full_navigation_flow():
    """
    Demonstrate a complete navigation flow: get → back → forward → refresh.
    """
    driver = _build_driver()

    driver.get(SELENIUM_URL)
    driver.get(INDEX_URL)

    driver.back()
    assert 'Selenium' in driver.title

    driver.forward()
    assert 'Index' in driver.title

    driver.refresh()
    assert 'Index' in driver.title

    print('Full navigation flow completed successfully')
    driver.quit()


if __name__ == '__main__':
    full_navigation_flow()
