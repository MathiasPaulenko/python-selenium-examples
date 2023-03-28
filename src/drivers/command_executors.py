# -*- coding: utf-8 -*-
"""
These allow you to set various parameters for the HTTP library
All the commands that can be executed can be found in:
/selenium/webdriver/remote/command.py

You can import the Command object from:
from selenium.webdriver.remote.command import Command
"""
from selenium import webdriver
from selenium.webdriver.remote.command import Command


# Used the execution commands
def command_executors():
    """
    Execute driver api commands directly by passing the command and a data dictionary (if necessary) to the driver api.
    """
    driver = webdriver.Chrome()

    driver.execute(Command.GET, {'url': 'https://www.example.com/'})
    browser_log = driver.execute(Command.GET_LOG, {"type": 'browser'})
    page_source = driver.execute(Command.GET_PAGE_SOURCE)
    print(f"Browser Logs: {browser_log}")
    print(f"Page Source: {page_source}")

    driver.quit()


if __name__ == '__main__':
    command_executors()
