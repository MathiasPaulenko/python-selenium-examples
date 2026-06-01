# -*- coding: utf-8 -*-
"""
Browser Capabilities/Options
all browsers share These capabilities.

In Selenium 4, use browser options classes (for example, ChromeOptions) and
set_capability() for W3C capabilities.

For remote sessions, passing an option instance is required because it also
declares the target browser.

These options are described in the w3c specification for Capabilities.

browserName - This capability is used to set the browserName for a given session. If the specified browser is not
installed at the remote end, the session creation will fail.

browserVersion - This capability is optional, this is used to set the available browser version at the remote end.
For Example, if you ask for Chrome version 75 on a system that only has 80 installed, the session creation will fail.

pageLoadStrategy - Three types of page load strategies are available:
    - Normal - Used by default, waits for all resources to download
    - eager - DOM access is ready, but other resources like images may still be loading
    - none - Does not block WebDriver at all

platformName - This identifies the operating system at the remote-end, fetching the platformName returns the OS name.

acceptInsecureCerts - This capability checks whether an expired (or) invalid TLS Certificate is used while
navigating during a session. If the capability is set to false, an insecure certificate error will be returned as
navigation encounters any domain certificate problems. If set to true, an invalid certificate will be trusted by the
browser.

timeouts - A WebDriver session is imposed with a certain session timeout interval, during which the user can control
the behavior of executing scripts or retrieving information from the browser.
Each session timeout is configured with a combination of different timeouts:
    - Script Timeout - Specifies when to interrupt an executing script in a current browsing context.
    The default timeout of 30,000 is imposed when a new session is created by WebDriver.
    - Page Load Timeout - Specifies the time interval in which a web page needs to be loaded in a current browsing
    context. The default timeout of 300 thousand is imposed when a new session is created by WebDriver. If page load limits a
    given/default time frame, the script will be stopped by TimeoutException.
    - Implicit Wait Timeout - This specifies the time to wait for the implicit element location strategy when locating
    elements. The default timeout 0 is imposed when a new session is created by WebDriver.

unhandledPromptBehavior - Specifies the state of the current session’s user prompt handler.
Defaults to dismiss and notify state.
    - User Prompt Handler - This defines what action must take when a user prompt encounters at the remote-end.
    This is defined by unhandledPromptBehavior capability and has the following states:
        - dismiss
        - accept
        - dismiss and notify
        - accept and notify
        - ignore

setWindowRect - Indicates whether the remote end supports all the resizing and repositioning commands.

strictFileInteractability - This new capability indicates if strict interactability checks should be applied to input
type=file elements. As strict interactability checks are off by default, there is a change in behavior when using
Element Send Keys with hidden file upload controls.

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Configuring driver capabilities.
def general_capabilities_att():
    """
    Configure common capabilities through Options attributes plus set_capability.
    """
    options = Options()
    options.page_load_strategy = 'normal'
    options.accept_insecure_certs = True
    options.set_capability('browserVersion', 'latest')
    options.set_capability('platformName', 'windows')
    options.set_capability('timeouts', {
        'implicit': 4500,
        'script': 300,
        'pageLoad': 30000,
    })
    options.set_capability('unhandledPromptBehavior', 'ignore')
    options.set_capability('strictFileInteractability', False)
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # do something
    driver.quit()


# Configuring driver capabilities.
def general_capabilities_dict():
    """
    Configure common capabilities from a dictionary and map them into Options.
    """
    capabilities = {
        'browserVersion': 'latest',
        'platformName': 'windows',
        'pageLoadStrategy': 'normal',
        'acceptInsecureCerts': True,
        'timeouts': {
            'implicit': 4500,
            'script': 300,
            'pageLoad': 30000,
        },
        'strictFileInteractability': False,
        'unhandledPromptBehavior': 'ignore',
    }
    options = Options()
    for key, value in capabilities.items():
        options.set_capability(key, value)

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # do something
    driver.quit()


def firefox_capabilities_att():
    """
    Configure common capabilities for Firefox via Options attributes plus set_capability.
    """
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'normal'
    options.accept_insecure_certs = True
    options.set_capability('browserVersion', 'latest')
    options.set_capability('platformName', 'windows')
    options.set_capability('timeouts', {
        'implicit': 4500,
        'script': 300,
        'pageLoad': 30000,
    })
    options.set_capability('unhandledPromptBehavior', 'ignore')
    options.set_capability('strictFileInteractability', False)

    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    # do something
    driver.quit()


def edge_capabilities_att():
    """
    Configure common capabilities for Edge via Options attributes plus set_capability.
    """
    options = webdriver.EdgeOptions()
    options.page_load_strategy = 'normal'
    options.accept_insecure_certs = True
    options.set_capability('browserVersion', 'latest')
    options.set_capability('platformName', 'windows')
    options.set_capability('timeouts', {
        'implicit': 4500,
        'script': 300,
        'pageLoad': 30000,
    })
    options.set_capability('unhandledPromptBehavior', 'ignore')
    options.set_capability('strictFileInteractability', False)

    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    # do something
    driver.quit()


if __name__ == '__main__':
    general_capabilities_att()

