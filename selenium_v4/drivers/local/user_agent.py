# -*- coding: utf-8 -*-
"""
User Agent customization examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/drivers/

The User-Agent header identifies the browser, OS and engine to the server.
Customizing it is useful to:
    - Simulate a different browser or device.
    - Bypass simple bot-detection based on default ChromeDriver user-agent strings.
    - Test server-side user-agent detection logic.

There are three main approaches in Selenium 4:
    1. Set via browser argument at startup (permanent for the session).
    2. Override with JavaScript at runtime (overrides for the current page).
    3. Set via experimental option in Chrome/Edge (Chrome DevTools Protocol).
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

EXAMPLE_URL = 'https://www.example.com/'

CUSTOM_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/124.0.0.0 Safari/537.36 CustomBot/1.0'
)

MOBILE_USER_AGENT = (
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/124.0.0.0 Mobile Safari/537.36'
)


def chrome_user_agent_argument():
    """
    Set a custom User-Agent at session startup via --user-agent argument.
    This applies permanently for the whole session.
    """
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent={CUSTOM_USER_AGENT}')

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(EXAMPLE_URL)

    actual_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Chrome User-Agent (argument): {actual_ua}')

    driver.quit()


def chrome_user_agent_experimental():
    """
    Override User-Agent via Chrome experimental option (CDP network conditions).
    This also applies from session start.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {})

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        'userAgent': CUSTOM_USER_AGENT,
        'acceptLanguage': 'en-US,en;q=0.9',
        'platform': 'Win32',
    })

    driver.get(EXAMPLE_URL)
    actual_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Chrome User-Agent (CDP): {actual_ua}')

    driver.quit()


def chrome_mobile_user_agent():
    """
    Simulate a mobile device by combining mobile User-Agent and device metrics via CDP.
    """
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'mobile': True,
        'width': 393,
        'height': 851,
        'deviceScaleFactor': 3,
    })
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        'userAgent': MOBILE_USER_AGENT,
    })

    driver.get(EXAMPLE_URL)
    actual_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Chrome Mobile User-Agent: {actual_ua}')

    driver.quit()


def chrome_user_agent_runtime_js():
    """
    Override User-Agent at runtime via JavaScript Object.defineProperty.
    Note: this only affects navigator.userAgent reads after the script runs;
    the HTTP header is already sent to the server by the time the page loads.
    """
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(EXAMPLE_URL)

    driver.execute_script(
        "Object.defineProperty(navigator, 'userAgent', {get: () => arguments[0]});",
        CUSTOM_USER_AGENT,
    )

    actual_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Chrome User-Agent (JS runtime): {actual_ua}')

    driver.quit()


def firefox_user_agent_preference():
    """
    Override User-Agent in Firefox via profile preference general.useragent.override.
    """
    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', CUSTOM_USER_AGENT)

    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(EXAMPLE_URL)

    actual_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Firefox User-Agent (preference): {actual_ua}')

    driver.quit()


def edge_user_agent_argument():
    """
    Set a custom User-Agent in Edge via --user-agent argument (same as Chrome).
    """
    options = webdriver.EdgeOptions()
    options.add_argument(f'--user-agent={CUSTOM_USER_AGENT}')

    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    driver.get(EXAMPLE_URL)

    actual_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Edge User-Agent (argument): {actual_ua}')

    driver.quit()


def read_current_user_agent():
    """
    Read the default User-Agent set by the browser without any customization.
    """
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(EXAMPLE_URL)

    default_ua = driver.execute_script('return navigator.userAgent;')
    print(f'Default Chrome User-Agent: {default_ua}')

    driver.quit()


if __name__ == '__main__':
    read_current_user_agent()
    chrome_user_agent_argument()
    chrome_user_agent_experimental()

