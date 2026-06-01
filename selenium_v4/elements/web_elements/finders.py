# -*- coding: utf-8 -*-
"""
Finding Web Elements examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/elements/finders/

Covers how to locate elements from the driver and from other elements.

Topics:
    - First matching element (find_element)
    - Evaluating entire DOM vs subset of DOM
    - Shadow DOM
    - Optimized locators
    - All matching elements (find_elements)
    - Get element from a collection by index
    - Find elements from element (scoped search)
    - Get active element

HTML reference used in finders documentation:
    <ol id="vegetables">
        <li class="tomatoes"><span>Tomato is a Vegetable</span></li>
    </ol>
    <ul id="fruits">
        <li class="tomatoes"><span>Tomato is a Fruit</span></li>
    </ul>
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

FINDERS_PAGE = 'https://www.selenium.dev/selenium/web/locators_tests/locators.html'
EXAMPLE_URL = 'https://www.example.com/'
GOOGLE_URL = 'https://www.google.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. First matching element — find_element
# ---------------------------------------------------------------------------

def find_first_element():
    """
    find_element() returns the first element in the DOM that matches the locator.
    If no element is found, NoSuchElementException is raised.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    heading = driver.find_element(By.TAG_NAME, 'h1')
    print(f'First h1: {heading.text}')

    driver.quit()


def find_element_entire_dom():
    """
    By default find_element searches the entire DOM from the document root.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    # Searches across the whole document
    element = driver.find_element(By.CLASS_NAME, 'information')
    print(f'Entire DOM search → value: {element.get_attribute("value")}')

    driver.quit()


def find_element_subset_of_dom():
    """
    Calling find_element() on a WebElement scopes the search to that element's subtree.
    Useful when multiple elements share the same locator in different parts of the page.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    # First locate the parent, then search inside it
    form = driver.find_element(By.TAG_NAME, 'form')
    first_input = form.find_element(By.CLASS_NAME, 'information')
    print(f'Subset DOM search → id: {first_input.get_attribute("id")}')

    driver.quit()


def find_element_optimized_locator():
    """
    A single CSS selector that targets a specific element in one query is more efficient
    than finding a parent and then a child in two separate calls.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    # One call instead of two
    element = driver.find_element(By.CSS_SELECTOR, 'form .information')
    print(f'Optimized locator → name: {element.get_attribute("name")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. All matching elements — find_elements
# ---------------------------------------------------------------------------

def find_all_elements():
    """
    find_elements() returns a list of all matching elements.
    Returns an empty list (not an exception) if no elements are found.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print(f'Total <input> elements found: {len(inputs)}')
    for inp in inputs:
        print(f'  type={inp.get_attribute("type")}, name={inp.get_attribute("name")}')

    driver.quit()


def get_element_from_collection():
    """
    Access a specific element from a find_elements() result by index.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    inputs = driver.find_elements(By.CLASS_NAME, 'information')
    if inputs:
        second = inputs[1]  # zero-indexed
        print(f'Second .information input → id: {second.get_attribute("id")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Find elements from element (scoped search)
# ---------------------------------------------------------------------------

def find_elements_from_element():
    """
    find_elements() called on a WebElement restricts the search scope to its children.
    Prevents accidental matches from other parts of the page.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    form = driver.find_element(By.TAG_NAME, 'form')
    radio_buttons = form.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
    print(f'Radio buttons inside form: {len(radio_buttons)}')
    for radio in radio_buttons:
        print(f'  value: {radio.get_attribute("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Get active element
# ---------------------------------------------------------------------------

def get_active_element():
    """
    switch_to.active_element returns the element that currently has keyboard focus.
    Useful after tabbing through a page or after clicking an input.
    """
    driver = _build_driver()
    driver.get(FINDERS_PAGE)

    # Click an input to give it focus
    fname_input = driver.find_element(By.ID, 'fname')
    fname_input.click()

    active = driver.switch_to.active_element
    print(f'Active element id: {active.get_attribute("id")}')

    driver.quit()


if __name__ == '__main__':
    find_first_element()
    find_all_elements()
    find_element_subset_of_dom()
    get_active_element()
