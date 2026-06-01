# -*- coding: utf-8 -*-
"""
Chrome special features examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/chrome/

Topics covered:
    - Starting Chrome (basic, headless, keep open, incognito)
    - Network conditions (slow network, offline) via CDP
    - Download behaviour (custom directory, headless downloads)
    - Permissions (CDP Browser.grantPermissions + Selenium set_permissions)
    - Console logs (browser log capture)
    - Cast / screen mirroring (list sinks, start/stop tab mirroring)
    - DevTools Protocol (CDP): performance metrics, block URLs, geolocation
    - Print page to PDF
"""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXAMPLE_URL = 'https://www.example.com/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'


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


def start_headless():
    """Start Chrome in headless mode (no visible UI). Recommended since Chrome 112."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_with_arguments():
    """Start Chrome with common arguments useful for CI/Docker environments."""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')             # Required in CI/Docker
    options.add_argument('--disable-dev-shm-usage')  # Required in Docker
    options.add_argument('--disable-gpu')             # Windows headless fix
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_incognito():
    """Open Chrome in Incognito mode."""
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_keep_browser_open():
    """
    Keep the browser open after the script exits (useful for debugging).
    The 'detach' experimental option tells ChromeDriver not to kill Chrome on quit.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    # Intentionally NOT calling driver.quit()


# ---------------------------------------------------------------------------
# 2. Network conditions (CDP)
# ---------------------------------------------------------------------------

def simulate_slow_network():
    """
    Throttle network speed to simulate slow 3G conditions.
    Uses CDP Network.emulateNetworkConditions.
    """
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'downloadThroughput': 500 * 1024 / 8,  # 500 kb/s
        'uploadThroughput': 500 * 1024 / 8,
        'latency': 400,                          # ms round-trip
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


def simulate_offline():
    """
    Put the browser into fully offline mode via CDP.
    Any navigation will fail with a network error (expected behaviour).
    """
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': True,
        'downloadThroughput': 0,
        'uploadThroughput': 0,
        'latency': 0,
    })
    # Navigation will raise WebDriverException — handle it in real tests.
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Download behaviour
# ---------------------------------------------------------------------------

def set_download_directory(download_dir: str | None = None):
    """
    Configure Chrome to save downloads to a specific folder without prompting.
    Works for both headed and headless modes.
    """
    target = str(Path(download_dir or OUTPUT_DIR).resolve())
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


def allow_downloads_in_headless():
    """
    Enable file downloads in headless Chrome via CDP Page.setDownloadBehavior.
    Required because headless Chrome disables downloads by default.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    target = str(OUTPUT_DIR.resolve())
    driver = _build_driver(options)
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {
        'behavior': 'allow',
        'downloadPath': target,
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Permissions
# ---------------------------------------------------------------------------

def grant_permissions_via_cdp():
    """
    Grant browser permissions for a specific origin using CDP.
    Available permissions: geolocation, notifications, camera, microphone, etc.
    """
    driver = _build_driver()
    driver.execute_cdp_cmd('Browser.grantPermissions', {
        'origin': EXAMPLE_URL,
        'permissions': ['geolocation', 'notifications'],
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


def reset_permissions_via_cdp():
    """Reset all granted permissions for the session via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Browser.resetPermissions', {})
    driver.get(EXAMPLE_URL)
    driver.quit()


def set_permissions_via_selenium():
    """
    Grant/deny permissions using Selenium's built-in set_permissions API.
    Simpler alternative to CDP for standard permissions.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.set_permissions('geolocation', 'granted')
    driver.set_permissions('notifications', 'denied')
    driver.quit()


# ---------------------------------------------------------------------------
# 5. Console logs
# ---------------------------------------------------------------------------

def get_browser_console_logs():
    """
    Capture browser console logs (console.log, errors, warnings).
    Requires goog:loggingPrefs capability set at session creation.
    """
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    logs = driver.get_log('browser')
    for entry in logs:
        print(f"  [{entry['level']}] {entry['message']}")
    driver.quit()


def list_log_types():
    """Print all available log types for the current Chrome session."""
    driver = _build_driver()
    print(f'Available log types: {driver.log_types}')
    driver.quit()


# ---------------------------------------------------------------------------
# 6. Cast (screen mirroring)
# ---------------------------------------------------------------------------

def list_cast_sinks():
    """
    List all available Cast sinks (Chromecast/smart TV devices).
    Requires the Google Cast extension to be present.
    """
    driver = _build_driver()
    sinks = driver.get_sinks()
    for sink in sinks:
        print(f'  Cast sink: {sink}')
    driver.quit()


def start_tab_mirroring():
    """Start mirroring the current tab to the first available Cast sink."""
    driver = _build_driver()
    sinks = driver.get_sinks()
    if sinks:
        driver.start_tab_mirroring(sinks[0]['name'])
    driver.quit()


def stop_casting():
    """Stop the active Cast session and print any issue message."""
    driver = _build_driver()
    issue = driver.get_issue_message()
    if issue:
        print(f'Cast issue: {issue}')
    sinks = driver.get_sinks()
    if sinks:
        driver.stop_casting(sinks[0]['name'])
    driver.quit()


# ---------------------------------------------------------------------------
# 7. CDP: geolocation, performance metrics, block URLs
# ---------------------------------------------------------------------------

def override_geolocation():
    """Override device geolocation (latitude/longitude) via CDP."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
        'latitude': 40.4168,
        'longitude': -3.7038,
        'accuracy': 100,
    })
    driver.get(EXAMPLE_URL)
    js_coords = driver.execute_script(
        'return new Promise(r => navigator.geolocation.getCurrentPosition('
        'p => r({lat: p.coords.latitude, lng: p.coords.longitude})));'
    )
    print(f'Overridden geolocation: {js_coords}')
    driver.quit()


def get_performance_metrics():
    """Collect V8/browser performance metrics via CDP Performance domain."""
    driver = _build_driver()
    driver.execute_cdp_cmd('Performance.enable', {})
    driver.get(EXAMPLE_URL)
    metrics = driver.execute_cdp_cmd('Performance.getMetrics', {})
    for m in metrics.get('metrics', []):
        print(f"  {m['name']}: {m['value']}")
    driver.quit()


def block_resource_urls():
    """
    Block specific URL patterns (images, stylesheets) from loading via CDP.
    Useful for performance testing or isolating behaviour.
    """
    driver = _build_driver()
    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        'urls': ['*.png', '*.jpg', '*.css', '*.woff2'],
    })
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 8. Print page to PDF
# ---------------------------------------------------------------------------

def print_page_to_pdf():
    """
    Print the current page as PDF (base64 encoded).
    Headless mode is required for print_page() to work.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    pdf_base64 = driver.print_page()
    print(f'PDF base64 length: {len(pdf_base64)} chars')

    # Optionally save to file
    import base64
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / 'page.pdf'
    pdf_path.write_bytes(base64.b64decode(pdf_base64))
    print(f'PDF saved to: {pdf_path}')

    driver.quit()


if __name__ == '__main__':
    start_basic()
    start_headless()
    list_log_types()
    print_page_to_pdf()

