# -*- coding: utf-8 -*-
"""
Working with Cookies examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/interactions/cookies/

Cookies are small pieces of data stored by the browser, used for sessions,
tracking, and preferences. WebDriver provides a full API to manage them.

Topics covered:
    - Add cookie
    - Get named cookie
    - Get all cookies
    - Delete named cookie
    - Delete all cookies
    - Same-site cookie attribute (Strict, Lax, None)
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXAMPLE_URL = 'https://www.example.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Add cookie
# ---------------------------------------------------------------------------

def add_cookie():
    """
    Add a cookie to the current browsing context.
    The browser must be on the same domain as the cookie before adding it.
    Minimum required field: 'name'. Commonly also set 'value'.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({'name': 'selenium', 'value': 'webdriver'})
    print('Cookie added')

    driver.quit()


def add_cookie_with_options():
    """
    Add a cookie with additional options:
        - domain   : domain the cookie is valid for
        - path     : URL path the cookie applies to
        - secure   : only sent over HTTPS
        - httpOnly : not accessible via JavaScript
        - expiry   : Unix timestamp for expiration
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({
        'name': 'selenium',
        'value': 'webdriver',
        'path': '/',
        'secure': True,
    })
    print('Cookie with options added')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Get named cookie
# ---------------------------------------------------------------------------

def get_named_cookie():
    """
    Retrieve a specific cookie by name from the current browsing context.
    Returns a dictionary with all cookie fields, or None if not found.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({'name': 'selenium', 'value': 'webdriver'})
    cookie = driver.get_cookie('selenium')
    print(f'Cookie: {cookie}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Get all cookies
# ---------------------------------------------------------------------------

def get_all_cookies():
    """
    Retrieve all cookies for the current browsing context.
    Returns a list of dictionaries, one per cookie.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({'name': 'cookie1', 'value': 'value1'})
    driver.add_cookie({'name': 'cookie2', 'value': 'value2'})

    cookies = driver.get_cookies()
    print(f'Total cookies: {len(cookies)}')
    for cookie in cookies:
        print(f'  {cookie["name"]} = {cookie["value"]}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Delete named cookie
# ---------------------------------------------------------------------------

def delete_named_cookie():
    """
    Delete a specific cookie by name from the current browsing context.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({'name': 'selenium', 'value': 'webdriver'})
    print(f'Before delete: {driver.get_cookie("selenium")}')

    driver.delete_cookie('selenium')
    print(f'After delete: {driver.get_cookie("selenium")}')  # None

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Delete all cookies
# ---------------------------------------------------------------------------

def delete_all_cookies():
    """
    Delete all cookies in the current browsing context.
    Useful for resetting session state between test runs.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({'name': 'cookie1', 'value': 'value1'})
    driver.add_cookie({'name': 'cookie2', 'value': 'value2'})
    print(f'Before delete all: {len(driver.get_cookies())} cookies')

    driver.delete_all_cookies()
    print(f'After delete all: {len(driver.get_cookies())} cookies')

    driver.quit()


# ---------------------------------------------------------------------------
# 6. Same-site cookie attribute
# ---------------------------------------------------------------------------

def add_cookie_same_site_strict():
    """
    Add a cookie with SameSite=Strict.
    The cookie is only sent with requests originating from the same site.
    Provides the strongest protection against CSRF attacks.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({
        'name': 'strict_cookie',
        'value': 'strict_value',
        'sameSite': 'Strict',
    })
    cookie = driver.get_cookie('strict_cookie')
    print(f'SameSite Strict cookie: {cookie}')

    driver.quit()


def add_cookie_same_site_lax():
    """
    Add a cookie with SameSite=Lax.
    The cookie is sent with same-site requests and top-level cross-site navigations.
    Default value in modern browsers when SameSite is not explicitly set.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.add_cookie({
        'name': 'lax_cookie',
        'value': 'lax_value',
        'sameSite': 'Lax',
    })
    cookie = driver.get_cookie('lax_cookie')
    print(f'SameSite Lax cookie: {cookie}')

    driver.quit()


if __name__ == '__main__':
    add_cookie()
    get_all_cookies()
    delete_all_cookies()
    add_cookie_same_site_strict()
