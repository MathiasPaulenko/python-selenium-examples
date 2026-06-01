# -*- coding: utf-8 -*-
"""
Firefox special features examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/firefox/

Topics covered:
    - Starting Firefox (basic, headless, private, keep open)
    - Custom binary location
    - Firefox Profile (preferences, custom profile directory)
    - Install / uninstall add-ons at runtime (signed xpi, temporary/unsigned)
    - Full page screenshot
    - Contexts (chrome vs content)
    - Permissions (Selenium set_permissions)
    - Print page to PDF
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

EXAMPLE_URL = 'https://www.example.com/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'


def _build_driver(options: webdriver.FirefoxOptions | None = None) -> webdriver.Firefox:
    """Helper: build a local Firefox driver via webdriver-manager."""
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
    """
    Start Firefox in headless mode (no visible UI).
    Uses the -headless argument supported since Firefox 55.
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_private():
    """Open Firefox in Private Browsing mode."""
    options = webdriver.FirefoxOptions()
    options.add_argument('-private')
    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


def start_keep_browser_open():
    """
    Keep Firefox open after the script finishes.
    Firefox does not have a 'detach' option like Chrome; simply omit quit().
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    # Intentionally NOT calling driver.quit()


# ---------------------------------------------------------------------------
# 2. Custom binary location
# ---------------------------------------------------------------------------

def start_custom_binary():
    """
    Point to a specific Firefox binary (e.g. Firefox Nightly or ESR).
    Set the FIREFOX_BINARY environment variable to the binary path.
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

def start_with_existing_profile():
    """
    Start Firefox with an existing profile directory.
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
    Customise Firefox behaviour via about:config preferences.
    set_preference merges values into the generated profile.
    """
    options = webdriver.FirefoxOptions()
    download_dir = str((OUTPUT_DIR).resolve())

    # Downloads
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.dir', download_dir)
    options.set_preference('browser.download.useDownloadDir', True)
    options.set_preference(
        'browser.helperApps.neverAsk.saveToDisk',
        'text/csv,application/pdf,application/zip',
    )
    options.set_preference('pdfjs.disabled', True)

    # Privacy / UX
    options.set_preference('dom.push.enabled', False)       # disable notification prompts
    options.set_preference('geo.enabled', False)            # disable geolocation prompts
    options.set_preference('intl.accept_languages', 'en-US')

    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Add-ons at runtime
# ---------------------------------------------------------------------------

def install_addon():
    """
    Install a signed Firefox extension (.xpi) at runtime and then uninstall it.
    Set FIREFOX_ADDON_XPI to the path of the .xpi file.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    addon_path = os.getenv('FIREFOX_ADDON_XPI')
    if addon_path and Path(addon_path).exists():
        addon_id = driver.install_addon(addon_path)
        print(f'Installed addon ID: {addon_id}')
        driver.uninstall_addon(addon_id)
        print('Addon uninstalled.')

    driver.quit()


def install_unsigned_addon():
    """
    Install an unsigned (temporary) extension from a directory.
    Requires a directory containing a valid manifest.json.
    Set FIREFOX_ADDON_DIR to the unpacked extension directory.
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
    Capture the entire page (including below-the-fold content).
    Firefox supports get_full_page_screenshot_as_file natively — no CDP needed.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / 'firefox_full_page.png'
    driver.get_full_page_screenshot_as_file(str(output))
    print(f'Full page screenshot saved: {output}')

    driver.quit()


# ---------------------------------------------------------------------------
# 6. Contexts (chrome vs content)
# ---------------------------------------------------------------------------

def use_chrome_context():
    """
    Switch to Firefox 'chrome' context to interact with browser UI elements
    (menus, toolbars) rather than web content.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    with driver.context(driver.CONTEXT_CHROME):
        # Scripts run here operate in Firefox's chrome (browser UI) context
        location = driver.execute_script('return window.location.href;')
        print(f'Chrome context location: {location}')

    # Automatically returns to content context after the with-block
    title = driver.execute_script('return document.title;')
    print(f'Content context title: {title}')
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
# 7. Permissions
# ---------------------------------------------------------------------------

def set_permissions():
    """
    Grant or deny standard browser permissions using Selenium's set_permissions API.
    Supported states: 'granted', 'denied', 'prompt'
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.set_permissions('geolocation', 'granted')
    driver.set_permissions('notifications', 'denied')
    print('Permissions updated.')

    driver.quit()


# ---------------------------------------------------------------------------
# 8. Print page to PDF
# ---------------------------------------------------------------------------

def print_page_to_pdf():
    """
    Print the current page as a PDF file.
    Firefox supports print_page() in both headed and headless modes.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    pdf_base64 = driver.print_page()
    print(f'PDF base64 length: {len(pdf_base64)} chars')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / 'firefox_page.pdf'
    pdf_path.write_bytes(base64.b64decode(pdf_base64))
    print(f'PDF saved to: {pdf_path}')

    driver.quit()


if __name__ == '__main__':
    start_basic()
    start_headless()
    full_page_screenshot()
    print_page_to_pdf()

