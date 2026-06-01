# -*- coding: utf-8 -*-
"""
Internet Explorer browser-specific Selenium 4 examples.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/internet_explorer/

IMPORTANT:
    Internet Explorer is only supported on Windows.
    Selenium 4 only supports IE 11. Legacy IE support was removed.
    The IEDriverServer must be downloaded separately:
    https://www.selenium.dev/downloads/

Topics covered:
    - Starting Internet Explorer
    - IE-specific options
    - File uploads (IE specific workaround)
    - Hover behaviour
    - Basic authentication
    - IE mode in Edge (see selenium_v4/browsers/edge/browser.py)
"""

from __future__ import annotations

import os

from selenium import webdriver
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.ie.service import Service

IE_DRIVER_PATH = os.getenv('IE_DRIVER_PATH', r'C:\WebDriver\IEDriverServer.exe')
EXAMPLE_URL = 'https://www.example.com/'


def _build_driver(options: IeOptions | None = None) -> webdriver.Ie:
    """Helper: build a local IE driver."""
    service = Service(executable_path=IE_DRIVER_PATH)
    return webdriver.Ie(service=service, options=options or IeOptions())


# ---------------------------------------------------------------------------
# 1. Starting IE with default settings
# ---------------------------------------------------------------------------

def start_basic():
    """
    Start Internet Explorer with default settings.
    Protected Mode must be set equally for all zones in IE security settings,
    or ignore_protected_mode_settings=True must be used.
    """
    options = IeOptions()
    options.ignore_protected_mode_settings = True
    options.ignore_zoom_level = True
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 2. IE-specific options
# ---------------------------------------------------------------------------

def configure_ie_options():
    """Demonstrate the main IeOptions available in Selenium 4."""
    options = IeOptions()

    # Allow navigation when Protected Mode settings differ across zones
    options.ignore_protected_mode_settings = True

    # Ignore zoom level differences (default zoom must be 100%)
    options.ignore_zoom_level = True

    # Use 32-bit IEDriverServer on 64-bit Windows for better compatibility
    options.require_window_focus = True

    # Persist cookies and cache between sessions
    options.ensure_clean_session = True

    # Attach to an existing IE window instead of launching a new one
    # options.attach_to_edge_chrome = False  # Only for Edge IE mode

    # Enable native events for realistic mouse/keyboard interactions
    options.native_events = True

    # Set persistent hover (keep mouse over element)
    options.enable_persistent_hover = True

    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. File uploads
# ---------------------------------------------------------------------------

def file_upload():
    """
    Upload a file in IE. IE requires using the AutoIt or native Win32 dialogs.
    The recommended Selenium approach is to set the file path directly on
    the input element when possible (works if the input is visible).
    """
    from selenium.webdriver.common.by import By

    options = IeOptions()
    options.ignore_protected_mode_settings = True
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)

    # Locate the file input and send the file path directly
    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input.send_keys(r'C:\path\to\file.txt')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Hover behaviour
# ---------------------------------------------------------------------------

def hover_element():
    """
    Hover over an element in IE. IE has stricter focus requirements.
    Use require_window_focus=True and enable_persistent_hover=True for
    reliable hover/tooltip interactions.
    """
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By

    options = IeOptions()
    options.ignore_protected_mode_settings = True
    options.require_window_focus = True
    options.enable_persistent_hover = True
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)

    element = driver.find_element(By.TAG_NAME, 'h1')
    ActionChains(driver).move_to_element(element).perform()

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Basic Authentication (send credentials in URL)
# ---------------------------------------------------------------------------

def basic_auth_via_url():
    """
    Pass HTTP Basic Auth credentials directly in the URL.
    This approach works in IE (and other browsers for simple cases).
    """
    username = 'admin'
    password = 's3cr3t'
    protected_url = f'http://{username}:{password}@httpbin.org/basic-auth/{username}/{password}'

    options = IeOptions()
    options.ignore_protected_mode_settings = True
    driver = _build_driver(options)
    driver.get(protected_url)
    driver.quit()


# ---------------------------------------------------------------------------
# 6. IE mode inside Edge (recommended modern approach)
# ---------------------------------------------------------------------------

def ie_mode_in_edge():
    """
    Selenium 4 recommended approach for IE: use Edge in IE Compatibility Mode.
    See selenium_v4/browsers/edge/browser.py → ie_compatibility_mode() for
    the full example.
    """
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverServerManager

    ie_options = webdriver.IeOptions()
    ie_options.attach_to_edge_chrome = True
    ie_options.edge_executable_path = os.getenv(
        'EDGE_BINARY', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    )

    ie_service = Service(executable_path=IEDriverServerManager().install())
    driver = webdriver.Ie(service=ie_service, options=ie_options)
    driver.get(EXAMPLE_URL)
    driver.quit()


if __name__ == '__main__':
    # IE requires the IEDriverServer installed and IE 11 on Windows.
    # Set IE_DRIVER_PATH env var to the IEDriverServer.exe path.
    start_basic()

