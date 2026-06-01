# -*- coding: utf-8 -*-
"""
Browser information interactions examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/interactions/

Topics covered:
    - Get page title
    - Get current URL
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SELENIUM_URL = 'https://www.selenium.dev/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Get title
# ---------------------------------------------------------------------------

def get_title():
    """
    Read the current page title from the browser.
    Equivalent to the <title> tag in the HTML head.
    """
    driver = _build_driver()
    driver.get(SELENIUM_URL)

    title = driver.title
    print(f'Page title: {title}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Get current URL
# ---------------------------------------------------------------------------

def get_current_url():
    """
    Read the current URL from the browser's address bar.
    Useful to verify redirects or page transitions.
    """
    driver = _build_driver()
    driver.get(SELENIUM_URL)

    url = driver.current_url
    print(f'Current URL: {url}')

    driver.quit()


def get_title_and_url():
    """
    Read both title and current URL in a single session.
    """
    driver = _build_driver()
    driver.get(SELENIUM_URL)

    title = driver.title
    url = driver.current_url
    print(f'Title: {title}')
    print(f'URL: {url}')

    driver.quit()


if __name__ == '__main__':
    get_title_and_url()
