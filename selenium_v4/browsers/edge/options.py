# -*- coding: utf-8 -*-
"""
Complete Selenium 4 examples for EdgeOptions.

Reference:
https://www.selenium.dev/documentation/webdriver/drivers/options/

This module focuses on:
    - W3C common capabilities
    - Edge-specific options (ms:edgeOptions)
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


def common_w3c_options() -> webdriver.EdgeOptions:
    """Common W3C capabilities supported by Selenium options classes."""
    options = webdriver.EdgeOptions()
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


def edge_arguments_and_headless() -> webdriver.EdgeOptions:
    """Edge command-line arguments and headless mode examples."""
    options = webdriver.EdgeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--inprivate')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--lang=en-US')
    options.add_argument('--headless=new')
    return options


def edge_binary_and_debugger() -> webdriver.EdgeOptions:
    """Custom binary/debugger attachment options."""
    options = webdriver.EdgeOptions()

    edge_binary = os.getenv('EDGE_BINARY')
    if edge_binary:
        options.binary_location = edge_binary

    debugger = os.getenv('EDGE_DEBUGGER_ADDRESS')
    if debugger:
        options.debugger_address = debugger
    return options


def edge_experimental_options(download_dir: str | None = None) -> webdriver.EdgeOptions:
    """add_experimental_option examples (prefs, excludeSwitches, mobileEmulation)."""
    options = webdriver.EdgeOptions()

    target_dir = Path(download_dir or Path.cwd() / 'output').resolve()
    prefs = {
        'download.default_directory': str(target_dir),
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
    }
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('mobileEmulation', {'deviceName': 'Pixel 5'})
    return options


def edge_extensions_examples() -> webdriver.EdgeOptions:
    """Extension examples using add_extension and add_encoded_extension."""
    options = webdriver.EdgeOptions()

    extension_path = os.getenv('EDGE_EXTENSION_CRX')
    if extension_path and Path(extension_path).exists():
        options.add_extension(extension_path)

    encoded_extension = os.getenv('EDGE_EXTENSION_BASE64')
    if encoded_extension:
        options.add_encoded_extension(encoded_extension)
    return options


def edge_proxy_example() -> webdriver.EdgeOptions:
    """Proxy capability via selenium Proxy object."""
    options = webdriver.EdgeOptions()

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'
    proxy.no_proxy = 'localhost,127.0.0.1'
    options.proxy = proxy
    options.ignore_local_proxy_environment_variables()
    return options


def edge_webview2_example() -> webdriver.EdgeOptions:
    """Run Edge using WebView2 mode."""
    options = webdriver.EdgeOptions()
    options.use_webview = True
    return options


def edge_mobile_android_example() -> webdriver.EdgeOptions:
    """Enable Edge/Chromium automation on Android device/emulator."""
    options = webdriver.EdgeOptions()
    options.enable_mobile(
        android_package='com.microsoft.emmx',
        android_activity='com.microsoft.ruby.Main',
        device_serial=os.getenv('ANDROID_SERIAL'),
    )
    return options


def edge_custom_capabilities() -> webdriver.EdgeOptions:
    """Custom vendor capabilities with set_capability."""
    options = webdriver.EdgeOptions()
    options.set_capability('webSocketUrl', True)
    options.set_capability('se:recordVideo', False)
    options.set_capability('se:timeZone', 'UTC')
    return options


def all_examples() -> dict[str, webdriver.EdgeOptions]:
    """Collect all option builders in one place."""
    return {
        'common_w3c_options': common_w3c_options(),
        'edge_arguments_and_headless': edge_arguments_and_headless(),
        'edge_binary_and_debugger': edge_binary_and_debugger(),
        'edge_experimental_options': edge_experimental_options(),
        'edge_extensions_examples': edge_extensions_examples(),
        'edge_proxy_example': edge_proxy_example(),
        'edge_webview2_example': edge_webview2_example(),
        'edge_mobile_android_example': edge_mobile_android_example(),
        'edge_custom_capabilities': edge_custom_capabilities(),
    }


def print_capabilities_examples() -> None:
    """Print every example as JSON capabilities payload."""
    payload = {name: options.to_capabilities() for name, options in all_examples().items()}
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    print_capabilities_examples()

