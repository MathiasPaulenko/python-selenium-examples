# -*- coding: utf-8 -*-
"""
Starting and stopping local sessions (open/close browser) with Selenium 4.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Creating session with local driver
def local_driver():
    """
    Creates a local Chrome session and then closes it.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    # do something
    driver.quit()


def local_driver_firefox():
    """
    Creates a local Firefox session and then closes it.
    """
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    # do something
    driver.quit()


def local_driver_edge():
    """
    Creates a local Edge session and then closes it.
    """
    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    # do something
    driver.quit()


if __name__ == '__main__':
    local_driver()
    local_driver_firefox()
    local_driver_edge()



