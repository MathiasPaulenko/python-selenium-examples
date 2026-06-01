# -*- coding: utf-8 -*-
"""
Listeners allow executing custom actions before and after WebDriver commands.

In Selenium 4 for Python, EventFiringWebDriver wraps a regular driver and
dispatches callbacks implemented in an AbstractEventListener subclass.

You can implement only the callbacks you need.

AbstractEventListener has the methods to implement:
    - before_navigate_to
    - after_navigate_to
    - before_navigate_back
    - after_navigate_back
    - before_navigate_forward
    - after_navigate_forward
    - before_find
    - after_find
    - before_click
    - after_click
    - before_change_value_of
    - after_change_value_of
    - before_execute_script
    - after_execute_script
    - before_close
    - after_close
    - before_quit
    - after_quit
    - on_exception

Relevant module:
selenium/webdriver/support/events.py
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver
from webdriver_manager.chrome import ChromeDriverManager

# AbstractEventListener subclass declaration
class WebDriverListener(AbstractEventListener):
    """
    Minimal custom listener with a few navigation/click/quit hooks.
    """

    def before_navigate_to(self, url, driver):
        """Action listener before navigating to a url."""
        print(f"Before navigate to {url}")

    def after_navigate_to(self, url, driver):
        """Action listener after navigating to a url."""
        print(f"After navigate to {url}")

    def before_quit(self, driver) -> None:
        """Action listener before driver quit"""
        print("Before close quit")

    def after_quit(self, driver) -> None:
        """Action listener after driver quit"""
        print("After close quit")

    def before_click(self, element, driver) -> None:
        """Action listener before web element click"""
        print(f"Before web element click: {element.text}")

    def after_click(self, element, driver) -> None:
        """Action listener after web element click"""
        print(f"After web element click: {element}")


# Use of EventFiringWebDriver
def listeners():
    """
    Configuring and using Selenium 4 EventFiringWebDriver listener events.
    """
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    listener_driver = EventFiringWebDriver(driver, WebDriverListener())
    listener_driver.get('https://www.example.com/')

    web_element = listener_driver.find_element(By.TAG_NAME, 'body')
    web_element.click()
    listener_driver.quit()


if __name__ == '__main__':
    listeners()

