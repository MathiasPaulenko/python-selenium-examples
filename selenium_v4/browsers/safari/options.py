# -*- coding: utf-8 -*-
"""
Complete Selenium 4 examples for SafariOptions.

Reference:
https://www.selenium.dev/documentation/webdriver/browsers/safari/
https://www.selenium.dev/documentation/webdriver/drivers/options/

IMPORTANT:
    Safari is only available on macOS.
    SafariDriver is built into macOS — no extra download needed.
    Enable Remote Automation in Safari:
        Safari > Develop > Allow Remote Automation

This module focuses on:
    - W3C common capabilities
    - Safari-specific options
    - Safari Technology Preview
    - Local and remote-ready option building

The examples build options objects and print capabilities, so the file is
executable without requiring Safari (capabilities are printed as JSON).
"""

from __future__ import annotations

import json

from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.safari.options import Options as SafariOptions


# ---------------------------------------------------------------------------
# W3C common capabilities
# ---------------------------------------------------------------------------

def common_w3c_options() -> SafariOptions:
    """Common W3C capabilities supported by SafariOptions."""
    options = SafariOptions()
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
    options.platform_name = 'mac'
    options.browser_version = 'latest'
    return options


# ---------------------------------------------------------------------------
# Safari-specific: diagnostics options
# ---------------------------------------------------------------------------

def safari_diagnostics_options() -> SafariOptions:
    """
    Enable automatic Web Inspector and Timelines profiler.
    These open automatically when the session starts.
    """
    options = SafariOptions()
    options.automatic_inspection = True    # Opens Web Inspector automatically
    options.automatic_profiling = True     # Opens Timelines panel automatically
    return options


# ---------------------------------------------------------------------------
# Safari Technology Preview
# ---------------------------------------------------------------------------

def safari_technology_preview_options() -> SafariOptions:
    """
    Configure options to target Safari Technology Preview instead of stable Safari.
    SafariOptions.use_technology_preview switches the driver to the TP binary.
    """
    options = SafariOptions()
    options.use_technology_preview = True
    return options


# ---------------------------------------------------------------------------
# Proxy
# ---------------------------------------------------------------------------

def safari_proxy_options() -> SafariOptions:
    """Proxy capability via Selenium Proxy object."""
    options = SafariOptions()
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = 'http://proxy:80'
    proxy.ssl_proxy = 'http://proxy:80'
    proxy.no_proxy = 'localhost,127.0.0.1'
    options.proxy = proxy
    options.ignore_local_proxy_environment_variables()
    return options


# ---------------------------------------------------------------------------
# Custom vendor capabilities
# ---------------------------------------------------------------------------

def safari_custom_capabilities() -> SafariOptions:
    """Custom vendor capabilities via set_capability."""
    options = SafariOptions()
    options.set_capability('webSocketUrl', True)   # BiDi sessions
    options.set_capability('se:recordVideo', False)
    options.set_capability('se:timeZone', 'UTC')
    return options


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------

def all_examples() -> dict[str, SafariOptions]:
    """Collect all option builders in one place."""
    return {
        'common_w3c_options': common_w3c_options(),
        'safari_diagnostics_options': safari_diagnostics_options(),
        'safari_technology_preview_options': safari_technology_preview_options(),
        'safari_proxy_options': safari_proxy_options(),
        'safari_custom_capabilities': safari_custom_capabilities(),
    }


def print_capabilities_examples() -> None:
    """Print every example as a JSON capabilities payload."""
    payload = {
        name: options.to_capabilities()
        for name, options in all_examples().items()
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    print_capabilities_examples()

