"""
These allow you to execute custom actions in every time specific Selenium commands are sent

In Python and Selenium 4 there are two Listeners:
    - EventFiringWebDriver:
    A wrapper around an arbitrary WebDriver instance which supports firing events.
    - EventFiringWebElement:
    A wrapper around WebElement instance which supports firing events.

Both Listeners must be passed by parameter an AbstractEventListener subclass and it must be fully or partially
implemented.

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

These classes can be found at:
selenium/webdriver/support/events.py
selenium/webdriver/support/abstract_event_listener.py
selenium/webdriver/support/event_firing_webdriver.py
"""
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, EventFiringWebElement


# AbstractEventListener subclass declaration
class WebDriverListener(AbstractEventListener):
    """
    A subclass of AbstractEventListener where all or part of its methods can be implemented.
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


# Use of EventFiringWebElement and EventFiringWebElement
def listeners():
    """
    Configuring and using the Selenium 4 EventFiringWebElement and EventFiringWebElement listener events.
    """
    # Same as EventFiringWebDriver
    driver = WebDriver()
    listener_driver = EventFiringWebDriver(driver, WebDriverListener())
    listener_driver.get('https://www.example.com/')

    # EventFiringWebElement declaration
    web_element = driver.find_element(By.LINK_TEXT, 'More information...')
    listener_web_element = EventFiringWebElement(web_element, listener_driver)
    listener_web_element.click()
    listener_driver.quit()


if __name__ == '__main__':
    listeners()
