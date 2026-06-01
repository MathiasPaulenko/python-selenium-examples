# -*- coding: utf-8 -*-
"""
Complete Selenium 4 examples for ChromeOptions.

Reference:
https://www.selenium.dev/documentation/webdriver/drivers/options/

This module focuses on:
	- W3C common capabilities
	- Chrome-specific options (goog:chromeOptions)
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


def common_w3c_options() -> webdriver.ChromeOptions:
	"""Common W3C capabilities supported by Selenium options classes."""
	options = webdriver.ChromeOptions()

	# W3C capabilities
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

	# Useful mostly for remote sessions
	options.platform_name = 'windows'
	options.browser_version = 'stable'
	return options


def chrome_arguments_and_headless() -> webdriver.ChromeOptions:
	"""Chrome command-line arguments and headless mode examples."""
	options = webdriver.ChromeOptions()

	options.add_argument('--start-maximized')
	options.add_argument('--incognito')
	options.add_argument('--disable-notifications')
	options.add_argument('--disable-popup-blocking')
	options.add_argument('--lang=en-US')

	# Headless mode in current Chromium versions.
	options.add_argument('--headless=new')
	return options


def chrome_binary_and_debugger() -> webdriver.ChromeOptions:
	"""Custom binary/debugger attachment options."""
	options = webdriver.ChromeOptions()

	# If you use a custom Chrome/Chromium binary.
	chrome_binary = os.getenv('CHROME_BINARY')
	if chrome_binary:
		options.binary_location = chrome_binary

	# Attach to existing browser started with --remote-debugging-port=9222
	debugger = os.getenv('CHROME_DEBUGGER_ADDRESS')
	if debugger:
		options.debugger_address = debugger
	return options


def chrome_experimental_options(download_dir: str | None = None) -> webdriver.ChromeOptions:
	"""add_experimental_option examples (prefs, excludeSwitches, mobileEmulation)."""
	options = webdriver.ChromeOptions()

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

	# Device emulation by known device name.
	options.add_experimental_option('mobileEmulation', {'deviceName': 'Pixel 5'})
	return options


def chrome_extensions_examples() -> webdriver.ChromeOptions:
	"""Extension examples using add_extension and add_encoded_extension."""
	options = webdriver.ChromeOptions()

	# Real extension file path (.crx) if available.
	extension_path = os.getenv('CHROME_EXTENSION_CRX')
	if extension_path and Path(extension_path).exists():
		options.add_extension(extension_path)

	# Base64 encoded extension content.
	encoded_extension = os.getenv('CHROME_EXTENSION_BASE64')
	if encoded_extension:
		options.add_encoded_extension(encoded_extension)
	return options


def chrome_proxy_example() -> webdriver.ChromeOptions:
	"""Proxy capability via selenium Proxy object."""
	options = webdriver.ChromeOptions()

	proxy = Proxy()
	proxy.proxy_type = ProxyType.MANUAL
	proxy.http_proxy = 'http://proxy:80'
	proxy.ssl_proxy = 'http://proxy:80'
	proxy.no_proxy = 'localhost,127.0.0.1'
	options.proxy = proxy

	# Ignore proxy-related environment variables from local machine.
	options.ignore_local_proxy_environment_variables()
	return options


def chrome_mobile_android_example() -> webdriver.ChromeOptions:
	"""Enable Chrome on Android device/emulator."""
	options = webdriver.ChromeOptions()
	options.enable_mobile(
		android_package='com.android.chrome',
		android_activity='com.google.android.apps.chrome.Main',
		device_serial=os.getenv('ANDROID_SERIAL'),
	)
	return options


def chrome_custom_capabilities() -> webdriver.ChromeOptions:
	"""Custom vendor capabilities with set_capability."""
	options = webdriver.ChromeOptions()
	options.set_capability('webSocketUrl', True)  # Useful with BiDi sessions.
	options.set_capability('se:recordVideo', False)  # Example Grid vendor cap.
	options.set_capability('se:timeZone', 'UTC')
	return options


def all_examples() -> dict[str, webdriver.ChromeOptions]:
	"""Collect all option builders in one place."""
	return {
		'common_w3c_options': common_w3c_options(),
		'chrome_arguments_and_headless': chrome_arguments_and_headless(),
		'chrome_binary_and_debugger': chrome_binary_and_debugger(),
		'chrome_experimental_options': chrome_experimental_options(),
		'chrome_extensions_examples': chrome_extensions_examples(),
		'chrome_proxy_example': chrome_proxy_example(),
		'chrome_mobile_android_example': chrome_mobile_android_example(),
		'chrome_custom_capabilities': chrome_custom_capabilities(),
	}


def print_capabilities_examples() -> None:
	"""Print every example as JSON capabilities payload."""
	payload = {
		name: options.to_capabilities()
		for name, options in all_examples().items()
	}
	print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
	print_capabilities_examples()

