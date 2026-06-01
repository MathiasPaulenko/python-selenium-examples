# -*- coding: utf-8 -*-
"""
Selenium WebDriver HTTP client examples for Python.

Reference:
https://www.selenium.dev/documentation/webdriver/drivers/http_client/

This file explains how to customize the HTTP transport used by RemoteWebDriver.
The examples are written for Selenium 4.x and remain executable even when there
is no Selenium Grid available.

Notes:
    - In Selenium 4.9.x, RemoteConnection is the primary customization API.
    - Newer Selenium releases also expose ClientConfig. This file includes a
      compatibility helper that only runs that example when available.
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.remote_connection import RemoteConnection

GRID_URL = os.getenv('SELENIUM_GRID_URL', 'http://127.0.0.1:4444/wd/hub')
EXAMPLE_URL = 'https://www.example.com/'


def basic_remote_with_keep_alive() -> None:
    """Example of configuring HTTP keep-alive from webdriver.Remote."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=GRID_URL,
        options=options,
        keep_alive=True,
    )
    driver.get(EXAMPLE_URL)
    print(driver.title)
    driver.quit()


def custom_remote_connection() -> RemoteConnection:
    """Create and configure RemoteConnection directly."""
    connection = RemoteConnection(
        remote_server_addr=GRID_URL,
        keep_alive=True,
        ignore_proxy=False,
    )

    # Global timeout (seconds) used by Selenium HTTP calls.
    connection.set_timeout(30)

    # Optional CA bundle path for HTTPS endpoints.
    ca_bundle = os.getenv('SELENIUM_CA_BUNDLE')
    if ca_bundle:
        connection.set_certificate_bundle_path(ca_bundle)

    return connection


def custom_headers_preview() -> dict:
    """Build the HTTP headers Selenium would send to the remote server."""
    parsed = urlparse(GRID_URL)
    headers = RemoteConnection.get_remote_connection_headers(parsed, keep_alive=True)

    # Add custom headers if your Selenium Grid/reverse-proxy needs them.
    custom_user_agent = os.getenv('SELENIUM_HTTP_USER_AGENT')
    if custom_user_agent:
        headers['User-Agent'] = custom_user_agent

    return headers


def remote_with_custom_http_client() -> None:
    """Use a custom RemoteConnection as command executor."""
    options = webdriver.ChromeOptions()
    connection = custom_remote_connection()
    driver = webdriver.Remote(command_executor=connection, options=options)
    driver.execute(Command.GET, {'url': EXAMPLE_URL})
    print(driver.title)
    driver.quit()


def client_config_example_if_available() -> str:
    """Show whether selenium.webdriver.remote.client_config is available."""
    try:
        from selenium.webdriver.remote.client_config import ClientConfig  # pylint: disable=import-outside-toplevel

        config = ClientConfig(remote_server_addr=GRID_URL)
        return f'ClientConfig available: {config.__class__.__name__}'
    except Exception:
        return 'ClientConfig module is not available in this Selenium version.'


def print_documentation_examples() -> None:
    """Print a dry-run summary without requiring a running Selenium Grid."""
    connection = custom_remote_connection()
    headers = custom_headers_preview()

    print('HTTP client dry-run')
    print(f'- GRID_URL: {GRID_URL}')
    print(f'- keep_alive: {connection.keep_alive}')
    print(f'- timeout: {connection.get_timeout()}')
    print(f'- certificate bundle: {connection.get_certificate_bundle_path()}')
    print(f'- headers preview: {headers}')
    print(f'- {client_config_example_if_available()}')


def run_live_remote_examples() -> None:
    """Run real remote sessions (requires a reachable Selenium Grid)."""
    basic_remote_with_keep_alive()
    remote_with_custom_http_client()


if __name__ == '__main__':
    # Default mode: documentation dry-run.
    # Set RUN_LIVE_REMOTE_EXAMPLES=1 to execute real remote sessions.
    if os.getenv('RUN_LIVE_REMOTE_EXAMPLES') == '1':
        run_live_remote_examples()
    else:
        print_documentation_examples()



