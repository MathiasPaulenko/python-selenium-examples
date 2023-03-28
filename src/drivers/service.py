"""
The Service classes are for managing the starting and stopping of drivers. They are not applicable in Remote Drivers.
With the Service class can be configured:
    - executable_path: install path of the chromedriver executable, defaults to `chromedriver`.
    - port: Port for the service to run on, defaults to 0 where the operating system will decide.
    - service_args: (Optional) List of args to be passed to the subprocess when launching the executable.
    - log_path: (Optional) String to be passed to the executable as `--log-path`.
    - env: (Optional) Mapping of environment variables for the new process, defaults to `os.environ`.

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def chrome_service():
    """
    Configuration of a basic Service class.
    """
    args = [  # commands accepted by the driver
        '--start-maximized',
        '--ignore-certificate-errors',
        '--disable-popup-blocking',
        '--incognito',
    ]
    service = Service(  # instance of the Service object
        executable_path=ChromeDriverManager(path='../../resources').install(),  # path to the driver binary.
        port=16654,
        log_path='../../output/chrome.log',
        service_args=args  # driver command declared above
    )
    driver = webdriver.Chrome(service=service)
    # do something
    driver.quit()


# TODO: add Service class configuration for firefox and edge.

if __name__ == '__main__':
    chrome_service()
