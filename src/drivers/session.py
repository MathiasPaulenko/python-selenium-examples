# -*- coding: utf-8 -*-
"""
Starting and stopping a session is for opening and closing a browser.

Creating Sessions:
Creating a new session corresponds with the W3C command for New session.
The session is created automatically by initializing a new Driver class object.

    Local Driver:
    The primary unique argument for starting a local driver includes information about starting the required driver
    service on the local machine.

    Remote Driver:
    The primary unique argument for starting a remote driver includes information about where to execute the code.

Quitting Sessions:
Quitting a session corresponds to W3C command for Deleting a Session.
Important note: the quit method is different from the close method, and it is recommended to always use quit
to end the session
"""
from selenium import webdriver


# Creating session with local driver
def local_driver():
    """
    Creates a local Chrome session and then closes it.
    """
    driver = webdriver.Chrome()
    # do something
    driver.quit()


# Creating session with remote driver
def remote_driver():
    """
    Creates a remote session and then closes it.
    """
    driver = webdriver.Remote(
        command_executor='https://www.example.com/'  # Set here a valid URL for Selenium remote connection.
    )
    # do something
    driver.quit()


# TODO: add example configuration for firefox and edge.

if __name__ == '__main__':
    local_driver()
