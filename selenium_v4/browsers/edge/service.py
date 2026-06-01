# -*- coding: utf-8 -*-
"""
Edge Service configuration examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/edge/

The Service class manages the lifecycle of the EdgeDriver process
(starting, stopping, port binding, logging).

Topics covered:
    - Driver location (explicit path vs Selenium Manager vs webdriver-manager)
    - Port assignment
    - Log output (file, stdout, stderr)
    - Log level via service_args
    - Append log across runs
    - Readable timestamp in log
    - Build check disable
    - Custom environment variables
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

EXAMPLE_URL = 'https://www.example.com/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'

def _build_driver(service: Service, options: webdriver.EdgeOptions | None = None) -> webdriver.Edge:
    return webdriver.Edge(service=service, options=options or webdriver.EdgeOptions())


# ---------------------------------------------------------------------------
# 1. Driver location
# ---------------------------------------------------------------------------

def driver_selenium_manager():
    """
    Selenium Manager (built-in since Selenium 4.6) resolves and downloads
    the correct EdgeDriver automatically — no extra library needed.
    """
    driver = webdriver.Edge()  # Selenium Manager handles everything
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_webdriver_manager():
    """
    Use the third-party webdriver-manager library to resolve EdgeDriver.
    """
    service = Service(executable_path=EdgeChromiumDriverManager().install())
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_explicit_path():
    """
    Hard-code the EdgeDriver path.
    Set EDGE_DRIVER_PATH or falls back to 'msedgedriver' on PATH.
    """
    path = os.getenv('EDGE_DRIVER_PATH', 'msedgedriver')
    service = Service(executable_path=path)
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Port
# ---------------------------------------------------------------------------

def service_custom_port():
    """
    Assign a specific port for the EdgeDriver HTTP server.
    Defaults to 0 (OS picks a free port automatically).
    """
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        port=17564,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Log output
# ---------------------------------------------------------------------------

def service_log_to_file():
    """
    Write EdgeDriver logs to a file.
    Uses log_path (Selenium 4.9.x) for Edge Service.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        log_path=str(OUTPUT_DIR / 'msedgedriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_log_to_stdout():
    """
    Redirect EdgeDriver output to the current process stdout.
    Useful for CI environments where logs are captured from stdout.
    """
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        log_path=subprocess.STDOUT,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. service_args: log level, append log, readable timestamp, build check
# ---------------------------------------------------------------------------

def service_log_level():
    """
    Set EdgeDriver log verbosity with --log-level.
    Valid values: ALL, DEBUG, INFO, WARNING, SEVERE, OFF
    """
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        service_args=['--log-level=DEBUG'],
        log_path=str(OUTPUT_DIR / 'msedgedriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_append_log():
    """
    Append to the existing log file instead of overwriting it on restart.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        service_args=['--append-log'],
        log_path=str(OUTPUT_DIR / 'msedgedriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_readable_log():
    """
    Add human-readable timestamps to each log entry.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        service_args=['--readable-timestamp'],
        log_path=str(OUTPUT_DIR / 'msedgedriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_disable_build_check():
    """
    Skip the EdgeDriver/Edge version compatibility check.
    Useful when testing with a patched or non-standard Edge build.
    """
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        service_args=['--disable-build-check'],
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 5. Custom environment variables
# ---------------------------------------------------------------------------

def service_custom_env():
    """
    Pass a custom environment to the EdgeDriver subprocess.
    Inherits the current process environment and adds/overrides variables.
    """
    custom_env = {**os.environ, 'MY_CUSTOM_VAR': 'selenium_example'}
    service = Service(
        executable_path=EdgeChromiumDriverManager().install(),
        env=custom_env,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


if __name__ == '__main__':
    driver_selenium_manager()
    service_log_to_file()
    print(f'Log written to: {OUTPUT_DIR / "msedgedriver.log"}')
