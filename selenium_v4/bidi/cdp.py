# -*- coding: utf-8 -*-
"""
Chrome DevTools Protocol (CDP) examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/bidi/cdp/

CDP support is temporary — WebDriver BiDi is the long-term replacement.
Chrome and Edge expose execute_cdp_cmd() which sends raw CDP commands.
This does NOT support bidirectional streaming; for that, use WebDriver BiDi.

When to use:
    - You need a feature not yet available in WebDriver BiDi
    - You are testing only on Chrome or Edge (Chromium-based browsers)

Topics covered:
    - Enabling BiDi (for BiDi-based features)
    - Set cookie via CDP (Network.setCookie)
    - Get page metrics via CDP (Performance.getMetrics)
    - Override geolocation via CDP (Emulation.setGeolocationOverride)
    - Set extra HTTP headers via CDP (Network.setExtraHTTPHeaders)
    - Block URLs via CDP (Network.setBlockedURLs)
    - Emulate network conditions via CDP (Network.emulateNetworkConditions)
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SELENIUM_URL = 'https://www.selenium.dev/'
EXAMPLE_URL = 'https://www.example.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


def _build_bidi_driver() -> webdriver.Chrome:
    """Build a driver with WebDriver BiDi enabled via the webSocketUrl capability."""
    options = webdriver.ChromeOptions()
    options.enable_bidi = True
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ---------------------------------------------------------------------------
# 1. Enabling BiDi
# ---------------------------------------------------------------------------

def enable_bidi():
    """
    Set options.enable_bidi = True to activate the WebDriver BiDi protocol.
    This enables the WebSocket connection required for bidirectional features
    such as logging handlers, network interception, and DOM mutation tracking.
    """
    options = webdriver.ChromeOptions()
    options.enable_bidi = True

    driver = _build_bidi_driver()
    driver.get(SELENIUM_URL)
    print(f'BiDi session active, title: {driver.title}')
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Set cookie via CDP
# ---------------------------------------------------------------------------

def set_cookie_via_cdp():
    """
    Use execute_cdp_cmd() with 'Network.setCookie' to set a cookie directly
    through the CDP protocol. This bypasses the domain restriction of
    driver.add_cookie() which requires visiting the domain first.
    """
    driver = _build_driver()

    cookie = {
        'name': 'cheese',
        'value': 'gouda',
        'domain': 'www.selenium.dev',
        'secure': True,
    }
    driver.execute_cdp_cmd('Network.setCookie', cookie)

    driver.get(SELENIUM_URL)
    cheese = driver.get_cookie('cheese')
    print(f'CDP cookie value: {cheese["value"]}')  # gouda

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Get performance metrics via CDP
# ---------------------------------------------------------------------------

def get_performance_metrics():
    """
    Enable the Performance domain and retrieve browser performance metrics
    such as JS heap size, DOM node count, and layout count.
    """
    driver = _build_driver()

    driver.execute_cdp_cmd('Performance.enable', {})
    driver.get(SELENIUM_URL)

    metrics = driver.execute_cdp_cmd('Performance.getMetrics', {})
    metrics_dict = {m['name']: m['value'] for m in metrics['metrics']}

    print(f'JS Heap Used Size: {metrics_dict.get("JSHeapUsedSize", "N/A")}')
    print(f'DOM Nodes: {metrics_dict.get("Nodes", "N/A")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Override geolocation via CDP
# ---------------------------------------------------------------------------

def override_geolocation():
    """
    Use Emulation.setGeolocationOverride to spoof the browser's GPS location.
    Useful for testing location-dependent features without physical movement.
    """
    driver = _build_driver()

    driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
        'latitude': 40.7128,
        'longitude': -74.0060,
        'accuracy': 100,
    })

    driver.get(EXAMPLE_URL)
    print('Geolocation overridden to New York (40.71°N, 74.00°W)')

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Set extra HTTP headers via CDP
# ---------------------------------------------------------------------------

def set_extra_http_headers():
    """
    Network.setExtraHTTPHeaders injects additional headers into every request
    made during the session. Useful for passing auth tokens or custom metadata.
    """
    driver = _build_driver()

    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        'headers': {
            'X-Custom-Header': 'selenium-bidi-test',
            'Accept-Language': 'en-US',
        }
    })

    driver.get(SELENIUM_URL)
    print('Extra HTTP headers applied to all requests')

    driver.quit()


# ---------------------------------------------------------------------------
# 6. Block URLs via CDP
# ---------------------------------------------------------------------------

def block_urls():
    """
    Network.setBlockedURLs prevents the browser from loading resources that
    match the given URL patterns. Useful to simulate missing assets or ads.
    """
    driver = _build_driver()

    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.setBlockedURLs', {
        'urls': ['*.png', '*.jpg', '*.gif'],
    })

    driver.get(SELENIUM_URL)
    print('Image URLs blocked — page loaded without images')

    driver.quit()


# ---------------------------------------------------------------------------
# 7. Emulate network conditions via CDP
# ---------------------------------------------------------------------------

def emulate_slow_network():
    """
    Network.emulateNetworkConditions simulates network throttling.
    Allows testing how the application behaves under slow or unstable networks.

    Preset: Slow 3G (~400 kbps download, ~400 kbps upload, 400ms latency)
    """
    driver = _build_driver()

    driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'latency': 400,           # ms
        'downloadThroughput': 50000,   # bytes/s (~400 kbps)
        'uploadThroughput': 50000,
        'connectionType': 'cellular3g',
    })

    driver.get(SELENIUM_URL)
    print('Page loaded under simulated Slow 3G conditions')

    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'latency': 0,
        'downloadThroughput': -1,
        'uploadThroughput': -1,
    })
    print('Network conditions reset to normal')

    driver.quit()


if __name__ == '__main__':
    set_cookie_via_cdp()
    get_performance_metrics()
    override_geolocation()
    block_urls()
