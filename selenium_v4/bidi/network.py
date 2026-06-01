# -*- coding: utf-8 -*-
"""
WebDriver BiDi Network Features examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/bidi/network/

Network handlers allow intercepting and manipulating HTTP traffic in real time
via the WebDriver BiDi protocol. This is the standards-based replacement for
CDP network interception.

Requires BiDi to be enabled: options.enable_bidi = True

Topics covered:
    - Authentication Handlers — handle HTTP Basic Auth prompts automatically
    - Request Handlers        — intercept and inspect/modify outgoing requests
    - Response Handlers       — intercept and inspect incoming responses
    - Remove Handler          — deregister a specific handler by id
    - Clear Handlers          — remove all registered network handlers
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASIC_AUTH_URL = 'https://the-internet.herokuapp.com/basic_auth'
SELENIUM_URL = 'https://www.selenium.dev/'


def _build_bidi_driver() -> webdriver.Chrome:
    """Build a Chrome driver with WebDriver BiDi enabled."""
    options = webdriver.ChromeOptions()
    options.enable_bidi = True
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ---------------------------------------------------------------------------
# 1. Authentication Handlers
# ---------------------------------------------------------------------------

def add_authentication_handler():
    """
    driver.network.add_authentication_handler(username, password) automatically
    provides credentials whenever the server responds with a 401 challenge.
    This handles HTTP Basic Authentication without user interaction.
    """
    driver = _build_bidi_driver()

    driver.network.add_authentication_handler('admin', 'admin')
    driver.get(BASIC_AUTH_URL)

    print(f'Auth handler active — page title: {driver.title}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Request Handlers
# ---------------------------------------------------------------------------

def add_request_handler():
    """
    driver.network.add_request_handler(callback) intercepts outgoing network
    requests before they are sent to the server.

    The callback receives a RequestData object. Call request.continue_() to
    allow the request, or request.fail() to abort it.

    Use cases:
        - Logging all outgoing requests
        - Blocking specific URLs
        - Modifying request headers before dispatch
    """
    driver = _build_bidi_driver()

    intercepted = []

    def log_request(request):
        intercepted.append(request.url)
        request.continue_()

    driver.network.add_request_handler(log_request)
    driver.get(SELENIUM_URL)

    print(f'Requests intercepted: {len(intercepted)}')
    for url in intercepted[:3]:
        print(f'  {url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Response Handlers
# ---------------------------------------------------------------------------

def add_response_handler():
    """
    driver.network.add_response_handler(callback) intercepts incoming server
    responses before they are processed by the browser.

    The callback receives a ResponseData object with status, headers, and body.
    Use cases:
        - Verifying response status codes
        - Logging API responses during test execution
        - Asserting response headers
    """
    driver = _build_bidi_driver()

    responses = []

    def log_response(response):
        responses.append({
            'url': response.request.url,
            'status': response.response.status,
        })

    driver.network.add_response_handler(log_response)
    driver.get(SELENIUM_URL)

    print(f'Responses captured: {len(responses)}')
    for r in responses[:3]:
        print(f'  {r["status"]} — {r["url"]}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Remove Handler
# ---------------------------------------------------------------------------

def remove_network_handler():
    """
    add_*_handler() methods return a handler id.
    Pass that id to the matching remove_*_handler(id) to stop interception.
    """
    driver = _build_bidi_driver()

    intercepted = []

    def log_request(request):
        intercepted.append(request.url)
        request.continue_()

    handler_id = driver.network.add_request_handler(log_request)

    # Remove before any navigation
    driver.network.remove_request_handler(handler_id)

    driver.get(SELENIUM_URL)

    print(f'Requests after handler removed: {len(intercepted)}')  # 0

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Clear Handlers
# ---------------------------------------------------------------------------

def clear_network_handlers():
    """
    driver.network.clear_handlers() removes all registered request, response,
    and authentication handlers in one call. Useful for cleanup between tests.
    """
    driver = _build_bidi_driver()

    intercepted = []

    def log_request(request):
        intercepted.append(request.url)
        request.continue_()

    driver.network.add_request_handler(log_request)
    driver.network.add_authentication_handler('user', 'pass')

    driver.network.clear_handlers()
    driver.get(SELENIUM_URL)

    print(f'Requests after clear_handlers: {len(intercepted)}')  # 0

    driver.quit()


if __name__ == '__main__':
    add_authentication_handler()
    add_request_handler()
    add_response_handler()
