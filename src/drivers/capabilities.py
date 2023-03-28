# -*- coding: utf-8 -*-
"""
Browser Capabilities/Options
These capabilities are shared by all browsers.

In Selenium 3, capabilities were defined in a session by using Desired Capabilities classes.
As of Selenium 4, you must use the browser options classes. For remote driver sessions, a browser options instance
is required as it determines which browser will be used.

These options are described in the w3c specification for Capabilities.

browserName - This capability is used to set the browserName for a given session. If the specified browser is not
installed at the remote end, the session creation will fail.

browserVersion - This capability is optional, this is used to set the available browser version at remote end.
For Example, if ask for Chrome version 75 on a system that only has 80 installed, the session creation will fail.

pageLoadStrategy - Three types of page load strategies are available:
    - Normal - Used by default, waits for all resources to download
    - eager - DOM access is ready, but other resources like images may still be loading
    - none - Does not block WebDriver at all

platformName - This identifies the operating system at the remote-end, fetching the platformName returns the OS name.

acceptInsecureCerts - This capability checks whether an expired (or) invalid TLS Certificate is used while
navigating during a session. If the capability is set to false, an insecure certificate error will be returned as
navigation encounters any domain certificate problems. If set to true, invalid certificate will be trusted by the
browser.

timeouts - A WebDriver session is imposed with a certain session timeout interval, during which the user can control
the behaviour of executing scripts or retrieving information from the browser.
Each session timeout is configured with combination of different timeouts:
    - Script Timeout - Specifies when to interrupt an executing script in a current browsing context.
    The default timeout 30,000 is imposed when a new session is created by WebDriver.
    - Page Load Timeout - Specifies the time interval in which web page needs to be loaded in a current browsing
    context. The default timeout 300,000 is imposed when a new session is created by WebDriver. If page load limits a
    given/default time frame, the script will be stopped by TimeoutException.
    - Implicit Wait Timeout - This specifies the time to wait for the implicit element location strategy when locating
    elements. The default timeout 0 is imposed when a new session is created by WebDriver.

unhandledPromptBehavior - Specifies the state of current session’s user prompt handler.
Defaults to dismiss and notify state.
    - User Prompt Handler - This defines what action must take when a user prompt encounters at the remote-end.
    This is defined by unhandledPromptBehavior capability and has the following states:
        - dismiss
        - accept
        - dismiss and notify
        - accept and notify
        - ignore

setWindowRect - Indicates whether the remote end supports all of the resizing and repositioning commands.

strictFileInteractability - This new capability indicates if strict interactability checks should be applied to input
type=file elements. As strict interactability checks are off by default, there is a change in behaviour when using
Element Send Keys with hidden file upload controls.

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Configuring driver capabilities.
def general_capabilities_att():
    """
    Configuring general capabilities via driver attributes.
    """
    options = Options()
    options.browser = 'Chrome'
    options.browser_version = '111.0.5563.65'
    options.page_load_strategy = 'normal'
    options.platform_name = 'windows'
    options.timeouts = {
        "implicit": 4500,
        "script": 300,
        "pageLoad": 30000
    }
    options.unhandled_prompt_behavior = 'ignore'
    options.strict_file_interactability = False
    driver = webdriver.Chrome(options=options)
    # do something
    driver.quit()


# Configuring driver capabilities.
def general_capabilities_dict():
    """
    Configuring general capabilities by means of a dictionary
    """
    capabilities = {
        'browserName': 'chrome',
        'browserVersion': '111.0.5563.65',
        'platformName': 'windows',
        'pageLoadStrategy': 'normal',
        'acceptSslCerts': True,
        'acceptInsecureCerts': True,
        'timeouts': {
            "implicit": 4500,
            "script": 300,
            "pageLoad": 30000
        },
        'strictFileInteractability': False,
        'unhandledPromptBehavior': 'ignore'
    }
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    # do something
    driver.quit()


# TODO: add example configuration for firefox and edge.

if __name__ == '__main__':
    general_capabilities_att()
