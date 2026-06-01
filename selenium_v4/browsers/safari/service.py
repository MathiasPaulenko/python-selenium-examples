# -*- coding: utf-8 -*-
"""
Safari Service configuration examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/safari/

IMPORTANT:
    Safari is only available on macOS.
    SafariDriver is built into macOS — no extra download needed.
    Enable Remote Automation in Safari:
        Safari > Develop > Allow Remote Automation
    Or run: safaridriver --enable

The Service class manages the lifecycle of the SafariDriver process
(starting, stopping, port binding, logging).

Topics covered:
    - Driver location (built-in safaridriver vs Safari Technology Preview)
    - Port assignment
    - Log output (built-in logging to ~/Library/Logs/com.apple.WebDriver/)
    - Service arguments (diagnostics, logging)
    - Safari Technology Preview service
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service

EXAMPLE_URL = 'https://www.example.com/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'

def _build_driver(service: Service, options: SafariOptions | None = None) -> webdriver.Safari:
    return webdriver.Safari(service=service, options=options or SafariOptions())


# ---------------------------------------------------------------------------
# 1. Driver location
# ---------------------------------------------------------------------------

def driver_builtin_safaridriver():
    """
    Use the built-in SafariDriver that comes with macOS.
    SafariDriver is located at /usr/bin/safaridriver by default.
    """
    service = Service()  # Uses default safaridriver path
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_explicit_path():
    """
    Specify a custom path to SafariDriver.
    Useful for testing or non-standard installations.
    """
    path = os.getenv('SAFARIDRIVER_PATH', '/usr/bin/safaridriver')
    service = Service(executable_path=path)
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Port assignment
# ---------------------------------------------------------------------------

def service_custom_port():
    """
    Assign a specific port for the SafariDriver HTTP server.
    Defaults to 0 (OS picks a free port automatically).
    """
    service = Service(
        port=27042,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Safari Technology Preview
# ---------------------------------------------------------------------------

def service_safari_technology_preview():
    """
    Use Safari Technology Preview instead of stable Safari.
    Safari TP must be installed from:
    https://developer.apple.com/safari/technology-preview/
    """
    service = Service(
        executable_path='/Applications/Safari Technology Preview.app'
                      '/Contents/MacOS/safaridriver'
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Service arguments and logging
# ---------------------------------------------------------------------------

def service_enable_diagnostics():
    """
    Enable SafariDriver diagnostics for debugging.
    This enables additional logging output.
    """
    service = Service(
        service_args=['--diagnostics'],
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_log_output():
    """
    Redirect SafariDriver output to stdout for CI environments.
    Note: Safari also writes logs to ~/Library/Logs/com.apple.WebDriver/
    """
    service = Service(
        log_output=subprocess.STDOUT,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_log_to_file():
    """
    Write SafariDriver logs to a specific file.
    This is in addition to the default macOS logs location.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        log_output=str(OUTPUT_DIR / 'safaridriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 5. Custom environment variables
# ---------------------------------------------------------------------------

def service_custom_env():
    """
    Pass custom environment variables to the SafariDriver subprocess.
    Inherits current environment and adds/overrides variables.
    """
    custom_env = {**os.environ, 'SAFARI_DEBUG': '1'}
    service = Service(
        env=custom_env,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 6. Combined examples
# ---------------------------------------------------------------------------

def service_safari_tp_with_logging():
    """
    Combine Safari Technology Preview with custom logging.
    Useful for debugging issues specific to Safari TP.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path='/Applications/Safari Technology Preview.app'
                      '/Contents/MacOS/safaridriver',
        port=27043,
        service_args=['--diagnostics'],
        log_output=str(OUTPUT_DIR / 'safari-tp.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


if __name__ == '__main__':
    # Safari automation only works on macOS
    driver_builtin_safaridriver()
    service_log_to_file()
    print(f'SafariDriver log written to: {OUTPUT_DIR / "safaridriver.log"}')
    print('Note: Safari also logs to ~/Library/Logs/com.apple.WebDriver/')
