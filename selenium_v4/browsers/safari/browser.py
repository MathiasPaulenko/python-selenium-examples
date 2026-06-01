# -*- coding: utf-8 -*-
"""
Safari browser-specific Selenium 4 examples.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/safari/

IMPORTANT:
    Safari is only available on macOS.
    SafariDriver is built into macOS — no extra download needed.
    Enable Remote Automation in Safari:
        Safari > Develop > Allow Remote Automation

Topics covered:
    - Starting Safari
    - Safari-specific options
    - Enable logging
    - Permissions (geography, notifications)
    - Safari Technology Preview
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service

EXAMPLE_URL = 'https://www.example.com/'


def _build_driver(options: SafariOptions | None = None) -> webdriver.Safari:
    """Helper: build a local Safari driver."""
    service = Service()  # safaridriver is in /usr/bin/safaridriver by default
    return webdriver.Safari(service=service, options=options or SafariOptions())


# ---------------------------------------------------------------------------
# 1. Starting Safari
# ---------------------------------------------------------------------------

def start_basic():
    """
    Start Safari with default settings.
    Requires Safari > Develop > Allow Remote Automation to be enabled.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_with_logging():
    """
    Enable SafariDriver logging for debugging.
    Logs are written to ~/Library/Logs/com.apple.WebDriver/.
    """
    options = SafariOptions()
    options.enable_automatic_inspection = True     # Opens Web Inspector automatically
    options.enable_automatic_profiling = True      # Opens Timelines panel automatically
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Safari Technology Preview
# ---------------------------------------------------------------------------

def start_safari_technology_preview():
    """
    Use Safari Technology Preview instead of the stable Safari release.
    Safari TP must be installed from:
    https://developer.apple.com/safari/technology-preview/
    """
    service = Service(executable_path='/Applications/Safari Technology Preview.app'
                      '/Contents/MacOS/safaridriver')
    options = SafariOptions()
    driver = webdriver.Safari(service=service, options=options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Permissions
# ---------------------------------------------------------------------------

def grant_geolocation_permission():
    """
    Grant geolocation permission for the current session.
    Safari uses set_permissions to control access.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.set_permissions('geolocation', 'prompt')  # 'prompt', 'granted', 'denied'
    driver.quit()


def deny_notifications_permission():
    """Deny notification permission for the current session."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.set_permissions('notifications', 'denied')
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Diagnostics and capabilities
# ---------------------------------------------------------------------------

def print_current_capabilities():
    """Print Safari session capabilities for debugging."""
    driver = _build_driver()
    print(driver.capabilities)
    driver.quit()


if __name__ == '__main__':
    # Safari automation only works on macOS.
    start_basic()
    print_current_capabilities()

