# -*- coding: utf-8 -*-
"""
Chrome Service configuration examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/chrome/

The Service class manages the lifecycle of the ChromeDriver process
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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXAMPLE_URL = 'https://www.example.com/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'

def _build_driver(service: Service, options: webdriver.ChromeOptions | None = None) -> webdriver.Chrome:
    return webdriver.Chrome(service=service, options=options or webdriver.ChromeOptions())


# ---------------------------------------------------------------------------
# 1. Driver location
# ---------------------------------------------------------------------------

def driver_selenium_manager():
    """
    Selenium Manager (built-in since Selenium 4.6) resolves and downloads
    the correct ChromeDriver automatically — no extra library needed.
    """
    driver = webdriver.Chrome()  # Selenium Manager handles everything
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_webdriver_manager():
    """
    Use the third-party webdriver-manager library to resolve ChromeDriver.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_explicit_path():
    """
    Hard-code the ChromeDriver path.
    Set CHROME_DRIVER_PATH or falls back to 'chromedriver' on PATH.
    """
    path = os.getenv('CHROME_DRIVER_PATH', 'chromedriver')
    service = Service(executable_path=path)
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Port
# ---------------------------------------------------------------------------

def service_custom_port():
    """
    Assign a specific port for the ChromeDriver HTTP server.
    Defaults to 0 (OS picks a free port automatically).
    """
    service = Service(
        executable_path=ChromeDriverManager().install(),
        port=16654,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Log output
# ---------------------------------------------------------------------------

def service_log_to_file():
    """
    Write ChromeDriver logs to a file.
    Uses log_path (Selenium 4.9.x) for Chrome Service.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path=ChromeDriverManager().install(),
        log_path=str(OUTPUT_DIR / 'chromedriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_log_to_stdout():
    """
    Redirect ChromeDriver output to the current process stdout.
    Useful for CI environments where logs are captured from stdout.
    """
    service = Service(
        executable_path=ChromeDriverManager().install(),
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
    Set ChromeDriver log verbosity with --log-level.
    Valid values: ALL, DEBUG, INFO, WARNING, SEVERE, OFF
    """
    service = Service(
        executable_path=ChromeDriverManager().install(),
        service_args=['--log-level=DEBUG'],
        log_path=str(OUTPUT_DIR / 'chromedriver.log'),
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
        executable_path=ChromeDriverManager().install(),
        service_args=['--append-log'],
        log_path=str(OUTPUT_DIR / 'chromedriver.log'),
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
        executable_path=ChromeDriverManager().install(),
        service_args=['--readable-timestamp'],
        log_path=str(OUTPUT_DIR / 'chromedriver.log'),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_disable_build_check():
    """
    Skip the ChromeDriver/Chrome version compatibility check.
    Useful when testing with a patched or non-standard Chrome build.
    """
    service = Service(
        executable_path=ChromeDriverManager().install(),
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
    Pass a custom environment to the ChromeDriver subprocess.
    Inherits the current process environment and adds/overrides variables.
    """
    custom_env = {**os.environ, 'MY_CUSTOM_VAR': 'selenium_example'}
    service = Service(
        executable_path=ChromeDriverManager().install(),
        env=custom_env,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


if __name__ == '__main__':
    driver_selenium_manager()
    service_log_to_file()
    print(f'Log written to: {OUTPUT_DIR / "chromedriver.log"}')

