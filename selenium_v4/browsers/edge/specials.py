# -*- coding: utf-8 -*-
"""
Edge browser-specific Selenium 4 examples.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/edge/

Topics covered:
    - Starting Edge (basic, headless, keep open)
    - Edge-specific arguments
    - Internet Explorer Compatibility Mode
    - WebView2
    - Network conditions (CDP)
    - Download behaviour
    - Permissions
    - CDP commands
"""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

EXAMPLE_URL = 'https://www.example.com/'


def _build_driver(options: webdriver.EdgeOptions | None = None) -> webdriver.Edge:
    """Helper: build a local Edge driver."""
    service = Service(executable_path=EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=options or webdriver.EdgeOptions())


# ---------------------------------------------------------------------------
# 1. Starting Edge
# ---------------------------------------------------------------------------

def start_basic():
    """Start Edge with default settings."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_headless():
    """Start Edge in headless mode (no visible UI)."""
    options = webdriver.EdgeOptions()
    options.add_argument('--headless=new')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_with_arguments():
    """Start Edge with common arguments."""
    options = webdriver.EdgeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--inprivate')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_keep_browser_open():
    """Keep Edge open after the script finishes using the detach option."""
    options = webdriver.EdgeOptions()
    options.add_experimental_option('detach', True)
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    # Do NOT call driver.quit() — browser stays open intentionally.


# ---------------------------------------------------------------------------
# 2. Custom binary
# ---------------------------------------------------------------------------

def start_custom_binary():
    """
    Point to a custom Edge binary (e.g. Edge Beta or Canary).
    Set EDGE_BINARY environment variable to the binary path.
    """
    options = webdriver.EdgeOptions()
    binary = os.getenv('EDGE_BINARY')
    if binary:
        options.binary_location = binary
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Internet Explorer Compatibility Mode
# ---------------------------------------------------------------------------

def ie_compatibility_mode():
    """
    Open a specific URL in Internet Explorer compatibility mode within Edge.
    Requires Microsoft Edge with IE mode configured in the OS/Group Policy.
    """
    options = webdriver.EdgeOptions()
    options.add_argument('--ie-mode-test')
    ie_options = webdriver.IeOptions()
    ie_options.attach_to_edge_chrome = True
    ie_options.edge_executable_path = os.getenv(
        'EDGE_BINARY', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    )
    # Use webdriver.Ie with ie_options to drive IE mode inside Edge
    from selenium.webdriver.ie.service import Service as IEService
    from webdriver_manager.microsoft import IEDriverServerManager
    ie_service = IEService(executable_path=IEDriverServerManager().install())
    driver = webdriver.Ie(service=ie_service, options=ie_options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. WebView2
# ---------------------------------------------------------------------------

def start_webview2():
    """
    Automate a WebView2 embedded browser (e.g. in a Windows desktop app).
    Set WEBVIEW2_BROWSER_EXECUTABLE to the host app executable path.
    """
    options = webdriver.EdgeOptions()
    options.use_webview = True
    app_path = os.getenv('WEBVIEW2_BROWSER_EXECUTABLE')
    if app_path:
        options.binary_location = app_path
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 5. Network Conditions (CDP)
# ---------------------------------------------------------------------------

def set_network_conditions():
    """
    Simulate slow network via CDP (same API as Chrome).
    """
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'downloadThroughput': 500 * 1024 / 8,
        'uploadThroughput': 500 * 1024 / 8,
        'latency': 20,
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 6. Download behaviour
# ---------------------------------------------------------------------------

def set_download_directory(download_dir: str | None = None):
    """Configure Edge download directory via experimental prefs."""
    target = str(Path(download_dir or Path.cwd() / 'output').resolve())
    options = webdriver.EdgeOptions()
    options.add_experimental_option('prefs', {
        'download.default_directory': target,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
    })
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 7. Permissions
# ---------------------------------------------------------------------------

def set_permission():
    """
    Set browser permissions using Selenium's built-in method.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.set_permissions('geolocation', 'granted')
    driver.set_permissions('notifications', 'denied')
    driver.quit()


# ---------------------------------------------------------------------------
# 8. CDP: geolocation, performance, block URLs
# ---------------------------------------------------------------------------

def set_geolocation():
    """Override device geolocation via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
        'latitude': 40.4168,
        'longitude': -3.7038,
        'accuracy': 100,
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


def get_performance_metrics():
    """Collect performance metrics via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Performance.enable', {})
    driver.get(EXAMPLE_URL)
    metrics = driver.execute_cdp_cmd('Performance.getMetrics', {})
    for m in metrics.get('metrics', []):
        print(f'  {m["name"]}: {m["value"]}')
    driver.quit()


# ---------------------------------------------------------------------------
# 9. Print page
# ---------------------------------------------------------------------------

def print_page_to_pdf():
    """Print the page to PDF (headless required)."""
    options = webdriver.EdgeOptions()
    options.add_argument('--headless=new')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    pdf_base64 = driver.print_page()
    print(f'PDF base64 length: {len(pdf_base64)} chars')
    driver.quit()


if __name__ == '__main__':
    start_basic()
    start_headless()
    get_performance_metrics()

