# -*- coding: utf-8 -*-
"""
You can use WebDriver remotely the same way you would use it locally. The primary difference is that a remote WebDriver
needs to be configured so that it can run your tests on a separate machine.

A remote WebDriver is composed of two pieces: a client and a server. The client is your WebDriver test and the server
is simply a Java servlet, which can be hosted in any modern JEE app server.

To run a remote WebDriver client, we first need to connect to the RemoteWebDriver. We do this by pointing the URL to
the address of the server running our tests. In order to customize our configuration, we set desired capabilities.

The Selenium Remote object accepts the following parameters:
    - command_executor - Either a string representing URL of the remote server or a custom
    remote_connection.RemoteConnection object. Defaults to 'http://127.0.0.1:4444/wd/hub'.
    - desired_capabilities - A dictionary of capabilities to request when starting the browser session.
    Required parameter.
    - browser_profile - A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object. Only used if Firefox is
    requested. Optional.
    - proxy - A selenium.webdriver.common.proxy.Proxy object. The browser session will be started with given proxy
    settings, if possible. Optional.
    - keep_alive - Whether to configure remote_connection.RemoteConnection to use HTTP keep-alive. Defaults to True.
    - file_detector - Pass custom file detector object during instantiation. If None, then default LocalFileDetector()
    will be used.
    - options - instance of a driver options.Options class
"""
from selenium import webdriver

URL = 'https://www.example.com/'


# Creating session with remote chrome driver
def chrome_remote_driver():
    """
    Creates a remote chrome session and then closes it.
    """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=URL,  # Set here a valid URL for Selenium remote connection.
        options=chrome_options
    )
    # do something
    driver.quit()


# Creating session with remote firefox driver
def firefox_remote_driver():
    """
    Creates a remote firefox session and then closes it.
    """
    firefox_options = webdriver.FirefoxOptions()
    driver = webdriver.Remote(
        command_executor=URL,  # Set here a valid URL for Selenium remote connection.
        options=firefox_options,
    )
    # do something
    driver.quit()


# Creating session with remote edge driver
def edge_remote_driver():
    """
    Creates a remote edge session and then closes it.
    """
    edge_options = webdriver.EdgeOptions()
    driver = webdriver.Remote(
        command_executor=URL,  # Set here a valid URL for Selenium remote connection.
        options=edge_options,
    )
    # do something
    driver.quit()


if __name__ == '__main__':
    chrome_remote_driver()
