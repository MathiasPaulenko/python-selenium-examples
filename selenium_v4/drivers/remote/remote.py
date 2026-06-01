# -*- coding: utf-8 -*-
"""
Use Remote WebDriver to execute tests on Selenium Grid or another remote node.

In Selenium 4, the recommended way is passing a browser-specific Options object
(ChromeOptions, FirefoxOptions, EdgeOptions) to webdriver.Remote. Capabilities
are sent using the W3C format through options.

Common Remote parameters:
    - command_executor: URL of the remote server (for example, Grid endpoint).
    - options: browser options instance that defines browser and capabilities.
    - keep_alive: enables HTTP keep-alive for remote connection.
    - file_detector: custom detector for file uploads in remote sessions.
"""
from selenium import webdriver

URL = 'http://127.0.0.1:4444/wd/hub'


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

