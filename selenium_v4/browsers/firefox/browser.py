# -*- coding: utf-8 -*-
"""
Firefox browser-specific Selenium 4 examples.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/firefox/

Topics covered:
    - Starting Firefox (basic, headless, keep open)
    - Firefox-specific arguments
    - Custom binary location
    - Firefox Profile (custom preferences, extensions)
    - Install/uninstall add-ons at runtime
    - Full page screenshot
    - Contexts (chrome vs content)
    - Log level
"""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

EXAMPLE_URL = 'https://www.example.com/'


def _build_driver(options: webdriver.FirefoxOptions | None = None) -> webdriver.Firefox:
    """Helper: build a local Firefox driver."""
    service = Service(executable_path=GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options or webdriver.FirefoxOptions())


# ---------------------------------------------------------------------------
# 1. Starting Firefox
# ---------------------------------------------------------------------------

def start_basic():
    """Start Firefox with default settings."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_headless():
    """Start Firefox in headless mode (no visible UI)."""
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_with_arguments():
    """Start Firefox with common arguments."""
    options = webdriver.FirefoxOptions()
    options.add_argument('-private')     # Private browsing
    options.add_argument('-devtools')    # Open DevTools automatically
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_keep_browser_open():
    """
    Keep Firefox open after the script finishes using a detached profile approach.
    Note: Firefox does not support the 'detach' experimental option like Chrome.
    The recommended way is to not call driver.quit().
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    # Do NOT call driver.quit() — browser stays open intentionally.


# ---------------------------------------------------------------------------
# 2. Custom binary location
# ---------------------------------------------------------------------------

def start_custom_binary():
    """
    Point to a specific Firefox binary (e.g. Firefox Nightly or ESR).
    Set FIREFOX_BINARY environment variable to the binary path.
    """
    options = webdriver.FirefoxOptions()
    binary = os.getenv('FIREFOX_BINARY')
    if binary:
        options.binary_location = binary
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Firefox Profile
# ---------------------------------------------------------------------------

def start_with_profile():
    """
    Start Firefox with a custom profile directory.
    Set FIREFOX_PROFILE_DIR to an existing profile path.
    """
    options = webdriver.FirefoxOptions()
    profile_dir = os.getenv('FIREFOX_PROFILE_DIR')
    if profile_dir and Path(profile_dir).exists():
        options.profile = FirefoxProfile(profile_dir)
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_with_profile_preferences():
    """
    Set Firefox preferences via profile to customize browser behaviour.
    Preferences are the same as what you would find in about:config.
    """
    options = webdriver.FirefoxOptions()
    # Accept cookies
    options.set_preference('network.cookie.cookieBehavior', 0)
    # Set download directory
    download_dir = str(Path.cwd() / 'output')
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.dir', download_dir)
    options.set_preference('browser.download.useDownloadDir', True)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk',
                           'text/csv,application/pdf,application/zip')
    options.set_preference('pdfjs.disabled', True)
    # Disable browser notifications prompt
    options.set_preference('dom.push.enabled', False)
    # Disable geolocation prompt
    options.set_preference('geo.enabled', False)
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Add-ons (extensions) at runtime
# ---------------------------------------------------------------------------

def install_addon():
    """
    Install a Firefox extension (.xpi) at runtime.
    Set FIREFOX_ADDON_XPI to the path of the .xpi file.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    addon_path = os.getenv('FIREFOX_ADDON_XPI')
    if addon_path and Path(addon_path).exists():
        addon_id = driver.install_addon(addon_path)
        print(f'Installed addon ID: {addon_id}')
        driver.uninstall_addon(addon_id)
    driver.quit()


def install_unsigned_addon():
    """
    Install an unsigned (temporary) Firefox extension.
    Requires a directory with the unpacked extension manifest.
    Set FIREFOX_ADDON_DIR to the extension directory.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    addon_dir = os.getenv('FIREFOX_ADDON_DIR')
    if addon_dir and Path(addon_dir).exists():
        addon_id = driver.install_addon(addon_dir, temporary=True)
        print(f'Installed temporary addon ID: {addon_id}')
    driver.quit()


# ---------------------------------------------------------------------------
# 5. Full page screenshot
# ---------------------------------------------------------------------------

def full_page_screenshot():
    """
    Take a screenshot of the full page (including content below the fold).
    Firefox supports this natively via get_full_page_screenshot_as_file.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    output = Path.cwd() / 'output' / 'firefox_full_page.png'
    output.parent.mkdir(parents=True, exist_ok=True)
    driver.get_full_page_screenshot_as_file(str(output))
    print(f'Full page screenshot saved: {output}')
    driver.quit()


# ---------------------------------------------------------------------------
# 6. Contexts (chrome vs content)
# ---------------------------------------------------------------------------

def use_chrome_context():
    """
    Switch to Firefox 'chrome' context to interact with browser UI elements
    (menus, toolbars) rather than web content. Useful for testing browser UI.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    with driver.context(driver.CONTEXT_CHROME):
        # Scripts/interactions here run in Firefox's chrome context (browser UI)
        result = driver.execute_script('return window.location.href;')
        print(f'Chrome context location: {result}')
    # Back to normal content context
    result = driver.execute_script('return document.title;')
    print(f'Content title: {result}')
    driver.quit()


def use_content_context():
    """
    Explicitly switch to Firefox 'content' context (the default web page context).
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    with driver.context(driver.CONTEXT_CONTENT):
        title = driver.execute_script('return document.title;')
        print(f'Content context title: {title}')
    driver.quit()


# ---------------------------------------------------------------------------
# 7. Log level
# ---------------------------------------------------------------------------

def set_log_level():
    """Configure geckodriver log verbosity."""
    options = webdriver.FirefoxOptions()
    options.log.level = 'trace'   # trace, debug, config, info, warn, error, fatal
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


if __name__ == '__main__':
    start_basic()
    start_headless()
    full_page_screenshot()

