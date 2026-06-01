# -*- coding: utf-8 -*-
"""
Firefox Service configuration examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/firefox/

The Service class manages the lifecycle of the GeckoDriver process
(starting, stopping, port binding, logging).

Topics covered:
    - Driver location (Selenium Manager, webdriver-manager, explicit path)
    - Port assignment
    - Log output (file, stdout)
    - Log level via service_args  (--log trace|debug|config|info|warn|error|fatal)
    - Truncated log entries disable (--log-no-truncate)
    - Custom environment variables
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

EXAMPLE_URL = 'https://www.example.com/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'
GECKODRIVER_LOG = GECKODRIVER_LOG


def _build_driver(service: Service, options: webdriver.FirefoxOptions | None = None) -> webdriver.Firefox:
    return webdriver.Firefox(service=service, options=options or webdriver.FirefoxOptions())


# ---------------------------------------------------------------------------
# 1. Driver location
# ---------------------------------------------------------------------------

def driver_selenium_manager():
    """
    Selenium Manager (built-in since Selenium 4.6) resolves and downloads
    the correct GeckoDriver automatically — no extra library needed.
    """
    driver = webdriver.Firefox()  # Selenium Manager handles everything
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_webdriver_manager():
    """
    Use the third-party webdriver-manager library to resolve GeckoDriver.
    """
    service = Service(executable_path=GeckoDriverManager().install())
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def driver_explicit_path():
    """
    Hard-code the GeckoDriver path.
    Set GECKO_DRIVER_PATH or falls back to 'geckodriver' on PATH.
    """
    path = os.getenv('GECKO_DRIVER_PATH', 'geckodriver')
    service = Service(executable_path=path)
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Port
# ---------------------------------------------------------------------------

def service_custom_port():
    """
    Assign a specific port for the GeckoDriver HTTP server.
    Defaults to 0 (OS picks a free port automatically).
    """
    service = Service(
        executable_path=GeckoDriverManager().install(),
        port=4444,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Log output
# ---------------------------------------------------------------------------

def service_log_to_file():
    """
    Write GeckoDriver logs to a file via the log_output parameter.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    log_file = OUTPUT_DIR / GECKODRIVER_LOG
    service = Service(
        executable_path=GeckoDriverManager().install(),
        log_output=str(log_file),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()
    print(f'GeckoDriver log written to: {log_file}')


def service_log_to_stdout():
    """
    Redirect GeckoDriver output to the current process stdout.
    Useful in CI environments where logs are captured from stdout.
    """
    service = Service(
        executable_path=GeckoDriverManager().install(),
        log_output=subprocess.STDOUT,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 4. service_args: log level, no-truncate
# ---------------------------------------------------------------------------

def service_log_level():
    """
    Set GeckoDriver log verbosity with the --log flag.
    Valid values: trace, debug, config, info, warn, error, fatal
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path=GeckoDriverManager().install(),
        service_args=['--log', 'debug'],
        log_output=str(OUTPUT_DIR / GECKODRIVER_LOG),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


def service_log_no_truncate():
    """
    Disable truncation of long log lines (geckodriver truncates by default).
    Pass --log-no-truncate via service_args.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = Service(
        executable_path=GeckoDriverManager().install(),
        service_args=['--log-no-truncate'],
        log_output=str(OUTPUT_DIR / GECKODRIVER_LOG),
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


# ---------------------------------------------------------------------------
# 5. Custom environment variables
# ---------------------------------------------------------------------------

def service_custom_env():
    """
    Pass a custom environment to the GeckoDriver subprocess.
    Inherits the current process environment and adds/overrides variables.
    """
    custom_env = {**os.environ, 'MY_CUSTOM_VAR': 'selenium_example'}
    service = Service(
        executable_path=GeckoDriverManager().install(),
        env=custom_env,
    )
    driver = _build_driver(service)
    driver.get(EXAMPLE_URL)
    driver.quit()


if __name__ == '__main__':
    driver_selenium_manager()
    service_log_to_file()
    print(f'Log written to: {OUTPUT_DIR / "geckodriver.log"}')

