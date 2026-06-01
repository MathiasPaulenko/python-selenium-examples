# -*- coding: utf-8 -*-
"""
The Service classes are for managing the starting and stopping of drivers. They are not applicable in Remote Drivers.
With the Service class can be configured:
    - executable_path: install the path of the chromedriver executable, defaults to `chromedriver`.
    - port: Port for the service to run on, defaults to 0 where the operating system will decide.
    - service_args: (Optional) List of args to be passed to the subprocess when launching the executable.
    - log_output: (Optional) destination for service logs (path, IO stream, or subprocess constants).
    - env: (Optional) Mapping of environment variables for the new process, defaults to `os.environ`.

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

EXAMPLE_URL = 'https://www.example.com/'
RETURN_DOC_TITLE = 'return document.title;'


def chrome_service():
    """
    Configure a local Chrome Service and browser options in Selenium 4.
    """
    browser_args = [
        '--start-maximized',
        '--ignore-certificate-errors',
        '--disable-popup-blocking',
        '--incognito',
    ]
    options = webdriver.ChromeOptions()
    for argument in browser_args:
        options.add_argument(argument)

    service = Service(  # instance of the Service object
        executable_path=ChromeDriverManager().install(),  # path to the driver binary.
        port=16654,
        log_output='../../output/chrome.log',
        service_args=['--append-log'],
    )
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(EXAMPLE_URL)
    title = driver.execute_script(RETURN_DOC_TITLE)
    print(f'Page title from JS: {title}')
    driver.quit()


def firefox_service():
    """
    Configure a local Firefox Service and browser options in Selenium 4.
    """
    browser_args = [
        '-private',
        '-devtools',
    ]
    options = webdriver.FirefoxOptions()
    for argument in browser_args:
        options.add_argument(argument)

    service = FirefoxService(
        executable_path=GeckoDriverManager().install(),
        port=16655,
        log_output='../../output/firefox.log',
    )
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(EXAMPLE_URL)
    title = driver.execute_script(RETURN_DOC_TITLE)
    print(f'Page title from JS: {title}')
    driver.quit()


def edge_service():
    """
    Configure a local Edge Service and browser options in Selenium 4.
    """
    browser_args = [
        '--start-maximized',
        '--ignore-certificate-errors',
        '--disable-popup-blocking',
        '--inprivate',
    ]
    options = webdriver.EdgeOptions()
    for argument in browser_args:
        options.add_argument(argument)

    service = EdgeService(
        executable_path=EdgeChromiumDriverManager().install(),
        port=16656,
        log_output='../../output/edge.log',
        service_args=['--append-log'],
    )
    driver = webdriver.Edge(service=service, options=options)
    driver.get(EXAMPLE_URL)
    title = driver.execute_script(RETURN_DOC_TITLE)
    print(f'Page title from JS: {title}')
    driver.quit()


if __name__ == '__main__':
    chrome_service()

