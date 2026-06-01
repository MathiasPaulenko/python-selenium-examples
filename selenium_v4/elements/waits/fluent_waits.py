# -*- coding: utf-8 -*-
"""
Fluent Waits examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/waits/

FluentWait is a customizable explicit wait that gives fine-grained control over:
    - Total timeout duration
    - Polling interval (how often the condition is checked)
    - Exceptions to ignore during polling
    - Custom timeout message

It is the underlying implementation that WebDriverWait extends.
Use FluentWait directly when you need more control than WebDriverWait provides.

Covered topics:
    - Basic FluentWait with custom polling and timeout
    - Ignoring specific exceptions during polling
    - Custom timeout error message
    - FluentWait with a callable condition
    - FluentWait with ExpectedConditions
    - Polling with side effects (performing actions inside the condition)
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from webdriver_manager.chrome import ChromeDriverManager

DYNAMIC_PAGE = 'https://www.selenium.dev/selenium/web/dynamic.html'
EXAMPLE_URL = 'https://www.example.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Basic FluentWait — custom timeout and polling interval
# ---------------------------------------------------------------------------

def fluent_wait_basic():
    """
    FluentWait with a 5-second timeout and 300ms polling interval.
    Polls every 300ms until the element is visible or 5s elapses.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    revealed = driver.find_element(By.ID, 'revealed')
    driver.find_element(By.ID, 'reveal').click()

    wait = (
        WebDriverWait(driver, timeout=5, poll_frequency=0.3)
    )
    wait.until(lambda d: revealed.is_displayed())

    revealed.send_keys('Displayed')
    print(f'Input value: {revealed.get_property("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Ignoring exceptions during polling
# ---------------------------------------------------------------------------

def fluent_wait_ignore_exceptions():
    """
    Ignore specific exceptions during polling so they don't abort the wait.
    Useful when the element may not yet be in the DOM (NoSuchElementException)
    or when it temporarily disappears (StaleElementReferenceException).
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'reveal').click()

    wait = WebDriverWait(
        driver,
        timeout=5,
        poll_frequency=0.3,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
    )
    revealed = wait.until(EC.visibility_of_element_located((By.ID, 'revealed')))
    print(f'Element found and visible: {revealed.is_displayed()}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Custom timeout message
# ---------------------------------------------------------------------------

def fluent_wait_custom_message():
    """
    Provide a descriptive message that appears in the TimeoutException
    when the condition is never met. Helps diagnose failures quickly.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    wait = WebDriverWait(driver, timeout=1, poll_frequency=0.2)
    try:
        wait.until(
            EC.visibility_of_element_located((By.ID, 'revealed')),
            message='Timed out waiting for #revealed to become visible',
        )
    except TimeoutException as exc:
        print(f'Caught: {exc.msg}')
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# 4. FluentWait with action inside the condition (side-effect polling)
# ---------------------------------------------------------------------------

def fluent_wait_action_in_condition():
    """
    Execute an action inside the condition callable.
    The wait retries the whole block until it returns True.
    ElementNotInteractableException is ignored so the input attempt is
    retried until the element becomes interactable.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    revealed = driver.find_element(By.ID, 'revealed')
    driver.find_element(By.ID, 'reveal').click()

    wait = WebDriverWait(
        driver,
        timeout=5,
        poll_frequency=0.3,
        ignored_exceptions=[ElementNotInteractableException],
    )

    def send_keys_when_ready(d):  # noqa: ANN001
        revealed.send_keys('Displayed')
        return True

    wait.until(send_keys_when_ready)
    print(f'Input value: {revealed.get_property("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 5. FluentWait for dynamically added element
# ---------------------------------------------------------------------------

def fluent_wait_dynamic_element():
    """
    Wait for a dynamically added element using FluentWait.
    The element does not exist at all until a button is clicked —
    NoSuchElementException is ignored during polling.
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    driver.find_element(By.ID, 'adder').click()

    wait = WebDriverWait(
        driver,
        timeout=5,
        poll_frequency=0.25,
        ignored_exceptions=[NoSuchElementException],
    )
    box = wait.until(EC.presence_of_element_located((By.ID, 'box0')))
    print(f'Dynamic element class: {box.get_attribute("class")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 6. FluentWait with ExpectedConditions and short poll
# ---------------------------------------------------------------------------

def fluent_wait_with_ec():
    """
    Combine FluentWait customization with standard ExpectedConditions helpers.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5)
    wait.until(EC.title_contains('Example'))
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

    heading = driver.find_element(By.TAG_NAME, 'h1')
    print(f'Heading: {heading.text}')

    driver.quit()


if __name__ == '__main__':
    fluent_wait_basic()
    fluent_wait_ignore_exceptions()
    fluent_wait_dynamic_element()
