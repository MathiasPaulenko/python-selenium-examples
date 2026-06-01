# -*- coding: utf-8 -*-
"""
WebDriver BiDi Logging Features examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/bidi/logging/

BiDi logging features are accessed via driver.script and allow real-time
interception of console messages and JavaScript exceptions as they occur,
without polling.

Requires BiDi to be enabled: options.enable_bidi = True

Topics covered:
    - Console Message Handlers — add and remove
    - JavaScript Exception Handlers — add and remove
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

LOG_PAGE = 'https://www.selenium.dev/selenium/web/bidi/logEntryAdded.html'


def _build_bidi_driver() -> webdriver.Chrome:
    """Build a Chrome driver with WebDriver BiDi enabled."""
    options = webdriver.ChromeOptions()
    options.enable_bidi = True
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ---------------------------------------------------------------------------
# 1. Console Message Handlers
# ---------------------------------------------------------------------------

def add_console_message_handler():
    """
    driver.script.add_console_message_handler(callback) registers a function
    that is called each time console.log (or similar) is invoked in the page.

    The callback receives a ConsoleLogEntry object with:
        - text       : the logged message string
        - type       : log level ('log', 'warn', 'error', etc.)
        - args       : list of arguments passed to console
        - timestamp  : when the message was emitted
    """
    driver = _build_bidi_driver()
    driver.get(LOG_PAGE)

    log_entries = []
    driver.script.add_console_message_handler(log_entries.append)

    driver.find_element(By.ID, 'consoleLog').click()

    WebDriverWait(driver, 5).until(lambda _: log_entries)
    print(f'Console message captured: {log_entries[0].text}')  # Hello, world!

    driver.quit()


def remove_console_message_handler():
    """
    add_console_message_handler() returns an id that can be passed to
    remove_console_message_handler(id) to stop listening.
    After removal, new console messages are no longer captured.
    """
    driver = _build_bidi_driver()
    driver.get(LOG_PAGE)

    log_entries = []
    handler_id = driver.script.add_console_message_handler(log_entries.append)

    # Remove the handler before the event fires
    driver.script.remove_console_message_handler(handler_id)

    driver.find_element(By.ID, 'consoleLog').click()

    print(f'Log entries after handler removed: {len(log_entries)}')  # 0

    driver.quit()


# ---------------------------------------------------------------------------
# 2. JavaScript Exception Handlers
# ---------------------------------------------------------------------------

def add_javascript_error_handler():
    """
    driver.script.add_javascript_error_handler(callback) registers a function
    that is called whenever an uncaught JavaScript exception occurs on the page.

    The callback receives a JavascriptException object with:
        - text        : the exception message
        - type        : always 'javascript'
        - timestamp   : when the exception was thrown
        - stack_trace : stack trace information
    """
    driver = _build_bidi_driver()
    driver.get(LOG_PAGE)

    log_entries = []
    driver.script.add_javascript_error_handler(log_entries.append)

    driver.find_element(By.ID, 'jsException').click()

    WebDriverWait(driver, 5).until(lambda _: log_entries)
    print(f'JS exception captured: {log_entries[0].text}')  # Error: Not working

    driver.quit()


def remove_javascript_error_handler():
    """
    add_javascript_error_handler() returns an id that can be passed to
    remove_javascript_error_handler(id) to stop listening for JS exceptions.
    """
    driver = _build_bidi_driver()
    driver.get(LOG_PAGE)

    log_entries = []
    handler_id = driver.script.add_javascript_error_handler(log_entries.append)

    driver.script.remove_javascript_error_handler(handler_id)

    driver.find_element(By.ID, 'jsException').click()

    print(f'JS exception entries after handler removed: {len(log_entries)}')  # 0

    driver.quit()


if __name__ == '__main__':
    add_console_message_handler()
    remove_console_message_handler()
    add_javascript_error_handler()
    remove_javascript_error_handler()
