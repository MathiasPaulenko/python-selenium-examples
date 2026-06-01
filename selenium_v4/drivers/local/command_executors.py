# -*- coding: utf-8 -*-
"""
These allow you to set various parameters for the HTTP library
All the commands that can be executed can be found in:
/selenium/webdriver/remote/command.py

You can import the Command object from:
from selenium.webdriver.remote.command import Command
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager


# Used the execution commands
def command_executors():
    """
    Execute driver api commands directly by passing the command and a data dictionary (if necessary) to the driver api.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        driver.get('https://www.example.com/')
        current_url = driver.execute(Command.GET_CURRENT_URL)
        page_source = driver.execute(Command.GET_PAGE_SOURCE)
        try:
            browser_log = driver.execute(Command.GET_LOG, {'type': 'browser'})
        except (Exception,):
            browser_log = {'value': 'Browser logs are not available for this driver configuration.'}

        print(f"Current URL: {current_url}")
        print(f"Browser Logs: {browser_log}")
        print(f"Page Source length: {len(page_source.get('value', ''))}")
    finally:
        driver.quit()


if __name__ == '__main__':
    command_executors()

