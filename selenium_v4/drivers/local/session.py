# -*- coding: utf-8 -*-
"""
Starting and stopping local sessions (open/close browser) with Selenium 4.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Creating session with local driver
def local_driver():
    """
    Creates a local Chrome session and then closes it.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    # do something
    driver.quit()


# TODO: add example configuration for firefox and edge.

if __name__ == '__main__':
    local_driver()



