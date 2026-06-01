# -*- coding: utf-8 -*-
"""
Complete Selenium 4 examples for FirefoxOptions.

Reference:
https://www.selenium.dev/documentation/webdriver/drivers/options/

This module focuses on:
    - W3C common capabilities
    - Firefox-specific options (moz:firefoxOptions)
    - Local and remote-ready option building

The examples build options objects and print capabilities, so the file is
executable without requiring Selenium Grid.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def common_w3c_options() -> webdriver.FirefoxOptions:
    """Common W3C capabilities supported by Selenium options classes."""
    options = webdriver.FirefoxOptions()
    options.accept_insecure_certs = True
    options.page_load_strategy = 'eager'
    options.strict_file_interactability = False
    options.unhandled_prompt_behavior = 'dismiss and notify'
    options.set_window_rect = True
    options.timeouts = {
        'implicit': 1500,
        'pageLoad': 30000,
        'script': 30000,
    }
    options.platform_name = 'windows'
    options.browser_version = 'stable'
    return options


def firefox_arguments_and_headless() -> webdriver.FirefoxOptions:
    """Firefox command-line arguments and headless mode examples."""
    options = webdriver.FirefoxOptions()
    options.add_argument('-private')
    options.add_argument('-devtools')
    options.add_argument('-headless')
    options.add_argument('--width=1366')
    options.add_argument('--height=768')
    return options


def firefox_binary_and_log() -> webdriver.FirefoxOptions:
    """Custom Firefox binary and geckodriver log level options."""
    options = webdriver.FirefoxOptions()

    firefox_binary = os.getenv('FIREFOX_BINARY')
    if firefox_binary:
        options.binary_location = firefox_binary

    options.log.level = 'trace'
    return options


def firefox_preferences(download_dir: str | None = None) -> webdriver.FirefoxOptions:
    """set_preference examples for profile behavior and download handling."""
    options = webdriver.FirefoxOptions()

    target_dir = Path(download_dir or Path.cwd() / 'output').resolve()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.dir', str(target_dir))
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/pdf')
    options.set_preference('browser.download.useDownloadDir', True)
    options.set_preference('pdfjs.disabled', True)
    options.set_preference('browser.startup.homepage', 'https://www.example.com/')
    options.set_preference('intl.accept_languages', 'en-US')
    return options


def firefox_profile_example() -> webdriver.FirefoxOptions:
    """Attach an existing Firefox profile if FIREFOX_PROFILE_DIR is set."""
    options = webdriver.FirefoxOptions()

    profile_dir = os.getenv('FIREFOX_PROFILE_DIR')
    if profile_dir and Path(profile_dir).exists():
        options.profile = FirefoxProfile(profile_dir)
    return options


def firefox_proxy_example() -> webdriver.FirefoxOptions:
    """Proxy capability via selenium Proxy object."""
    options = webdriver.FirefoxOptions()

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'
    proxy.no_proxy = 'localhost,127.0.0.1'
    options.proxy = proxy
    options.ignore_local_proxy_environment_variables()
    return options


def firefox_mobile_android_example() -> webdriver.FirefoxOptions:
    """Enable Firefox automation on Android device/emulator."""
    options = webdriver.FirefoxOptions()
    options.enable_mobile(
        android_package='org.mozilla.firefox',
        android_activity='org.mozilla.gecko.BrowserApp',
        device_serial=os.getenv('ANDROID_SERIAL'),
    )
    return options


def firefox_custom_capabilities() -> webdriver.FirefoxOptions:
    """Custom vendor capabilities with set_capability."""
    options = webdriver.FirefoxOptions()
    options.set_capability('webSocketUrl', True)
    options.set_capability('se:recordVideo', False)
    options.set_capability('se:timeZone', 'UTC')
    return options


def all_examples() -> dict[str, webdriver.FirefoxOptions]:
    """Collect all option builders in one place."""
    return {
        'common_w3c_options': common_w3c_options(),
        'firefox_arguments_and_headless': firefox_arguments_and_headless(),
        'firefox_binary_and_log': firefox_binary_and_log(),
        'firefox_preferences': firefox_preferences(),
        'firefox_profile_example': firefox_profile_example(),
        'firefox_proxy_example': firefox_proxy_example(),
        'firefox_mobile_android_example': firefox_mobile_android_example(),
        'firefox_custom_capabilities': firefox_custom_capabilities(),
    }


def print_capabilities_examples() -> None:
    """Print every example as JSON capabilities payload."""
    payload = {name: options.to_capabilities() for name, options in all_examples().items()}
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    print_capabilities_examples()

