# -*- coding: utf-8 -*-
"""
Chrome browser-specific Selenium 4 examples.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/chrome/

Topics covered:
    - Starting Chrome (basic, headless, keep open)
    - Chrome-specific arguments
    - Network conditions (offline, throttling)
    - Download behaviour
    - Chrome Devtools Protocol (CDP) commands
    - Permissions
    - Cast (screen mirroring)
    - Log types
    - Casting
"""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXAMPLE_URL = 'https://www.example.com/'


def _build_driver(options: webdriver.ChromeOptions | None = None) -> webdriver.Chrome:
    """Helper: build a local Chrome driver."""
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options or webdriver.ChromeOptions())


# ---------------------------------------------------------------------------
# 1. Starting Chrome
# ---------------------------------------------------------------------------

def start_basic():
    """Start Chrome with default settings."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_with_arguments():
    """Start Chrome with common arguments."""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')               # Required in CI/Docker
    options.add_argument('--disable-dev-shm-usage')   # Required in Docker
    options.add_argument('--disable-gpu')              # Windows headless compatibility
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_headless():
    """Start Chrome in headless mode (no visible UI)."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # new headless is recommended in Chrome >= 112
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_keep_browser_open():
    """
    Keep the browser open after the script finishes.
    Useful for debugging. Uses the detach experimental option.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    # Do NOT call driver.quit() — browser stays open intentionally.


# ---------------------------------------------------------------------------
# 2. Chrome-specific: incognito
# ---------------------------------------------------------------------------

def start_incognito():
    """Open Chrome in incognito mode."""
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Network Conditions (CDP)
# ---------------------------------------------------------------------------

def set_network_conditions():
    """
    Set network conditions to simulate slow/offline connections via CDP.
    Requires Chrome and uses execute_cdp_cmd to control the network layer.
    """
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'downloadThroughput': 500 * 1024 / 8,   # 500 kb/s
        'uploadThroughput': 500 * 1024 / 8,
        'latency': 20,                            # ms
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


def set_offline():
    """Simulate offline network condition."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': True,
        'downloadThroughput': 0,
        'uploadThroughput': 0,
        'latency': 0,
    })
    driver.get(EXAMPLE_URL)  # Will fail to load (as expected when offline)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Download behaviour
# ---------------------------------------------------------------------------

def set_download_directory(download_dir: str | None = None):
    """
    Configure Chrome to download files to a custom directory without prompting.
    """
    target = str(Path(download_dir or Path.cwd() / 'output').resolve())
    options = webdriver.ChromeOptions()
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
# 5. Permissions (CDP)
# ---------------------------------------------------------------------------

def grant_geolocation_permission():
    """Grant geolocation permission for a specific origin via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Browser.grantPermissions', {
        'origin': EXAMPLE_URL,
        'permissions': ['geolocation'],
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


def reset_permissions():
    """Reset all browser permissions."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Browser.resetPermissions', {})
    driver.get(EXAMPLE_URL)
    driver.quit()


def set_permission_via_webdriver():
    """
    Set permissions using Selenium's built-in set_permissions method.
    Available permissions: 'geolocation', 'notifications', 'camera', 'microphone', etc.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.set_permissions('geolocation', 'granted')
    driver.set_permissions('notifications', 'denied')
    driver.quit()


# ---------------------------------------------------------------------------
# 6. DevTools Protocol (CDP) – general commands
# ---------------------------------------------------------------------------

def get_performance_metrics():
    """Collect browser performance metrics via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Performance.enable', {})
    driver.get(EXAMPLE_URL)
    metrics = driver.execute_cdp_cmd('Performance.getMetrics', {})
    for m in metrics.get('metrics', []):
        print(f"  {m['name']}: {m['value']}")
    driver.quit()


def block_urls_via_cdp():
    """Block specific URL patterns using CDP Network interception."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        'urls': ['*.png', '*.jpg', '*.css'],
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


def set_geolocation_via_cdp():
    """Override device geolocation via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
        'latitude': 40.4168,
        'longitude': -3.7038,
        'accuracy': 100,
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 7. Log types
# ---------------------------------------------------------------------------

def get_browser_logs():
    """
    Retrieve browser console logs.
    Requires loggingPrefs capability to be set at session start.
    """
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    logs = driver.get_log('browser')
    for entry in logs:
        print(f"  [{entry['level']}] {entry['message']}")
    driver.quit()


def get_available_log_types():
    """List the available log types for the current driver."""
    driver = _build_driver()
    print(f'Available log types: {driver.log_types}')
    driver.quit()


# ---------------------------------------------------------------------------
# 8. Cast (screen mirroring)
# ---------------------------------------------------------------------------

def list_cast_sinks():
    """List available Cast sinks (Chromecast devices)."""
    driver = _build_driver()
    sinks = driver.get_sinks()
    for sink in sinks:
        print(f'  Cast sink: {sink}')
    driver.quit()


def start_cast_session():
    """Start a Cast tab mirroring session to the first available sink."""
    driver = _build_driver()
    sinks = driver.get_sinks()
    if sinks:
        driver.start_tab_mirroring(sinks[0]['name'])
    driver.quit()


def stop_cast_session():
    """Stop the active Cast session."""
    driver = _build_driver()
    issue = driver.get_issue_message()
    print(f'Cast issue: {issue}')
    driver.stop_casting(driver.get_sinks()[0]['name'] if driver.get_sinks() else '')
    driver.quit()


# ---------------------------------------------------------------------------
# 9. Print page
# ---------------------------------------------------------------------------

def print_page_to_pdf():
    """Print the current page to a PDF binary (headless required)."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    pdf_base64 = driver.print_page()
    print(f'PDF base64 length: {len(pdf_base64)} chars')
    driver.quit()


if __name__ == '__main__':
    start_basic()
    start_headless()
    get_available_log_types()

