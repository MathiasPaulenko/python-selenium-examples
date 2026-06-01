# -*- coding: utf-8 -*-
"""
Starting and stopping remote sessions with Selenium 4.

Remote sessions require a valid Selenium Grid/remote endpoint URL and
browser-specific options.
"""
from selenium import webdriver


REMOTE_URL = 'http://127.0.0.1:4444/wd/hub'


def chrome_remote_session():
    """Create and close a remote Chrome session."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    # do something
    driver.quit()


def firefox_remote_session():
    """Create and close a remote Firefox session."""
    options = webdriver.FirefoxOptions()
    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    # do something
    driver.quit()


def edge_remote_session():
    """Create and close a remote Edge session."""
    options = webdriver.EdgeOptions()
    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    # do something
    driver.quit()


if __name__ == '__main__':
    chrome_remote_session()

