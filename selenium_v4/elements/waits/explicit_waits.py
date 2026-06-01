# -*- coding: utf-8 -*-
"""
Explicit Waits examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/waits/

Explicit waits poll the application for a specific condition to evaluate as
true before continuing. If the condition is not met within the timeout,
a TimeoutException is raised.

Key characteristics:
    - Scoped: applied per-call, not globally like implicit wait.
    - By default, WebDriverWait automatically waits for the element to exist.
    - More reliable than sleep() and more targeted than implicit waits.
    - Conditions can be lambdas, callables, or ExpectedConditions helpers.

Covered topics:
    - Basic WebDriverWait with lambda condition
    - WebDriverWait with ExpectedConditions (EC)
    - Waiting for element visibility, clickability, text, title, URL
    - Waiting for multiple elements
    - Handling TimeoutException
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

DYNAMIC_PAGE = 'https://www.selenium.dev/selenium/web/dynamic.html'
EXAMPLE_URL = 'https://www.example.com/'
DEFAULT_TIMEOUT = 5  # seconds


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Basic explicit wait with lambda
# ---------------------------------------------------------------------------

def explicit_wait_lambda():
    """
    Use WebDriverWait with a lambda as the condition.
    The wait polls until the lambda returns a truthy value or the timeout expires.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    revealed = driver.find_element(By.ID, 'revealed')
    driver.find_element(By.ID, 'reveal').click()

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    wait.until(lambda d: revealed.is_displayed())

    revealed.send_keys('Displayed')
    print(f'Input value: {revealed.get_property("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Explicit wait with ExpectedConditions
# ---------------------------------------------------------------------------

def explicit_wait_element_visible():
    """
    Wait for an element to become visible using EC.visibility_of_element_located.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'reveal').click()

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    revealed = wait.until(EC.visibility_of_element_located((By.ID, 'revealed')))
    print(f'Element visible: {revealed.is_displayed()}')

    driver.quit()


def explicit_wait_element_clickable():
    """
    Wait for an element to be visible and enabled (ready to click).
    EC.element_to_be_clickable is useful before performing a click action.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    adder = wait.until(EC.element_to_be_clickable((By.ID, 'adder')))
    adder.click()

    driver.quit()


def explicit_wait_element_present():
    """
    Wait for an element to be present in the DOM (not necessarily visible).
    EC.presence_of_element_located does not require the element to be displayed.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'adder').click()

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    box = wait.until(EC.presence_of_element_located((By.ID, 'box0')))
    print(f'Element present in DOM: {box.get_attribute("class")}')

    driver.quit()


def explicit_wait_element_invisible():
    """
    Wait for an element to disappear or become invisible.
    Useful after triggering a loading spinner or overlay.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    # Wait until the 'revealed' element is invisible (it starts hidden)
    wait.until(EC.invisibility_of_element_located((By.ID, 'revealed')))
    print('Element is not visible (as expected before reveal)')

    driver.quit()


def explicit_wait_text_present():
    """
    Wait until a specific text is present in a located element.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Example'))
    heading = driver.find_element(By.TAG_NAME, 'h1')
    print(f'Heading text: {heading.text}')

    driver.quit()


def explicit_wait_title():
    """
    Wait for the page title to contain a specific string.
    Useful after navigation or async page transitions.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    wait.until(EC.title_contains('Example'))
    print(f'Page title: {driver.title}')

    driver.quit()


def explicit_wait_url_contains():
    """
    Wait for the current URL to contain a specific substring.
    Useful after redirects or single-page application route changes.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    wait.until(EC.url_contains('example.com'))
    print(f'Current URL: {driver.current_url}')

    driver.quit()


def explicit_wait_multiple_elements():
    """
    Wait for all matching elements to be present in the DOM.
    EC.presence_of_all_elements_located returns a list once at least one is found.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'adder').click()
    driver.find_element(By.ID, 'adder').click()

    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'redbox')))
    print(f'Number of boxes found: {len(boxes)}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Handling TimeoutException
# ---------------------------------------------------------------------------

def explicit_wait_timeout_handling():
    """
    Demonstrate how to catch TimeoutException when the condition is never met.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    wait = WebDriverWait(driver, 1)  # Very short timeout — will likely fail
    try:
        # The 'revealed' element exists but is hidden; visibility wait will timeout
        wait.until(EC.visibility_of_element_located((By.ID, 'revealed')))
    except TimeoutException:
        print('TimeoutException caught: condition was not met within 1 second')
    finally:
        driver.quit()


if __name__ == '__main__':
    explicit_wait_lambda()
    explicit_wait_element_visible()
    explicit_wait_element_present()
