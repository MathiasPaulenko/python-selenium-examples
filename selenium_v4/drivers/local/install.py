# -*- coding: utf-8 -*-
"""
Through WebDriver, Selenium supports all major browsers on the market such as Chrome/Chromium, Firefox,
Internet Explorer, Edge, and Safari. Where possible, WebDriver drives the browser using the browser’s built-in support
for automation.

Since all the driver implementations except for Internet Explorer are provided by the browser vendors themselves,
they are not included in the standard Selenium distribution. This section explains the basic requirements for getting
started with the different browsers.

Four Ways to Use Drivers:
    1. Selenium Manager
    Selenium Manager helps you get a working environment out of the box. In Selenium 4, it can resolve compatible
    drivers automatically when they are not found on PATH.

    2. Driver Management Software
    Most machines automatically update the browser, but the driver does not. To make sure you get the correct driver
    for your browser, there are many third party libraries to assist you.

    3. The PATH Environment Variable
    This option first requires manually downloading the driver.
    This is a flexible option to change location of drivers without having to update your code, and will work on
    multiple machines without requiring that each machine put the drivers in the same place.
    You can either place the drivers in a directory that is already listed in PATH, or you can place them in a
    directory and add it to PATH.

    4. Hard Coded Location
    Similar to Option 3 above, you need to manually download the driver.
    Specifying the location in the code itself has the advantage of not needing to figure out Environment Variables on
    your system, but has the drawback of making the code much less flexible.

Download link for drivers:
    - Chrome: https://chromedriver.chromium.org/downloads
    - Firefox: https://github.com/mozilla/geckodriver/releases
    - Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    - Internet Explorer: https://www.selenium.dev/downloads/
    - Safari: Built in
"""
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://www.example.com/'


# first way to use the driver
def driver_selenium_manager():
    """
    Let Selenium Manager resolve and configure the driver automatically.
    """
    driver = webdriver.Chrome()
    driver.get(URL)
    # do something
    driver.quit()


# second way to use the driver
def driver_management_software():
    """
    Using the webdriver-manager library to manage the automatic download of driver binaries.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    # do something
    driver.quit()


# third way to use the driver
def driver_environment_variable():
    """
    Configuring the driver by environment variables.
    """
    driver_path = '../../resources'
    os.environ["PATH"] = driver_path + ';' + os.environ["PATH"]

    driver = webdriver.Chrome()
    driver.get(URL)
    # do something
    driver.quit()


# fourth way to use the driver
def driver_hard_code():
    """
    Configuring the driver hard code the path to the driver.
    """
    driver_path = '../../resources/chromedriver.exe'
    service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    # do something
    driver.quit()


if __name__ == '__main__':
    driver_management_software()

