# -*- coding: utf-8 -*-
"""
Information about Web Elements examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/elements/information/

What you can learn about a located element:
    - is_displayed()    — Is the element visible on the page?
    - is_enabled()      — Is the element enabled (interactable)?
    - is_selected()     — Is the element selected (checkboxes/radios/options)?
    - tag_name          — HTML tag name of the element
    - rect              — Size and position (x, y, width, height)
    - value_of_css_property() — Computed CSS property value
    - text              — Visible inner text
    - get_attribute()   — HTML attribute value
    - get_property()    — DOM property value
    - get_dom_attribute() — Explicit HTML attribute (not property)
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

FORM_PAGE = 'https://www.selenium.dev/selenium/web/locators_tests/locators.html'
DYNAMIC_PAGE = 'https://www.selenium.dev/selenium/web/dynamic.html'
EXAMPLE_URL = 'https://www.example.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Is Displayed
# ---------------------------------------------------------------------------

def is_displayed():
    """
    is_displayed() returns True if the element is visible to the user.
    An element can be in the DOM but not displayed (e.g. hidden via CSS).
    """
    driver = _build_driver()
    driver.get(DYNAMIC_PAGE)

    # 'revealed' starts hidden; 'adder' button is always visible
    adder = driver.find_element(By.ID, 'adder')
    hidden = driver.find_element(By.ID, 'revealed')

    print(f'adder is_displayed: {adder.is_displayed()}')    # True
    print(f'revealed is_displayed: {hidden.is_displayed()}')  # False

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Is Enabled
# ---------------------------------------------------------------------------

def is_enabled():
    """
    is_enabled() returns True if the element is enabled and can be interacted with.
    Disabled form controls return False.
    """
    driver = _build_driver()
    driver.get(FORM_PAGE)

    fname = driver.find_element(By.ID, 'fname')
    submit = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')

    print(f'fname is_enabled: {fname.is_enabled()}')    # True
    print(f'submit is_enabled: {submit.is_enabled()}')  # True

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Is Selected
# ---------------------------------------------------------------------------

def is_selected():
    """
    is_selected() returns True for checkboxes and radio buttons that are checked,
    and for <option> elements that are selected in a <select>.
    """
    driver = _build_driver()
    driver.get(FORM_PAGE)

    male_radio = driver.find_element(By.CSS_SELECTOR, 'input[value="m"]')
    newsletter = driver.find_element(By.NAME, 'newsletter')

    print(f'male radio is_selected (default): {male_radio.is_selected()}')  # False
    print(f'newsletter is_selected (default): {newsletter.is_selected()}')  # False

    newsletter.click()
    print(f'newsletter is_selected (after click): {newsletter.is_selected()}')  # True

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Tag Name
# ---------------------------------------------------------------------------

def get_tag_name():
    """
    tag_name returns the lowercase HTML tag name of the element.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    heading = driver.find_element(By.TAG_NAME, 'h1')
    link = driver.find_element(By.TAG_NAME, 'a')

    print(f'heading tag_name: {heading.tag_name}')  # h1
    print(f'link tag_name: {link.tag_name}')        # a

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Size and Position
# ---------------------------------------------------------------------------

def get_size_and_position():
    """
    rect returns a dictionary with x, y, width, and height of the element.
    Useful for visual assertion and custom interaction logic.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    heading = driver.find_element(By.TAG_NAME, 'h1')
    rect = heading.rect

    print(f'x: {rect["x"]}, y: {rect["y"]}')
    print(f'width: {rect["width"]}, height: {rect["height"]}')

    driver.quit()


# ---------------------------------------------------------------------------
# 6. Get CSS Value
# ---------------------------------------------------------------------------

def get_css_value():
    """
    value_of_css_property() returns the computed CSS value for a given property.
    The value is the browser-computed one, not the raw CSS rule.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    body = driver.find_element(By.TAG_NAME, 'body')
    color = body.value_of_css_property('color')
    font_size = body.value_of_css_property('font-size')

    print(f'body color: {color}')
    print(f'body font-size: {font_size}')

    driver.quit()


# ---------------------------------------------------------------------------
# 7. Text Content
# ---------------------------------------------------------------------------

def get_text_content():
    """
    text returns the visible rendered text of an element and its descendants.
    Whitespace is collapsed. Hidden text is not included.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    heading = driver.find_element(By.TAG_NAME, 'h1')
    paragraph = driver.find_element(By.TAG_NAME, 'p')

    print(f'h1 text: {heading.text}')
    print(f'p text: {paragraph.text}')

    driver.quit()


# ---------------------------------------------------------------------------
# 8. Fetching Attributes or Properties
# ---------------------------------------------------------------------------

def get_attribute_vs_property():
    """
    get_attribute() returns the HTML attribute value (as seen in the source).
    get_property() returns the current DOM property value (may differ after JS changes).
    get_dom_attribute() explicitly returns the HTML attribute, never the property.

    Example: <input type="checkbox" checked>
        - get_attribute('checked')     → 'true'  (uses property fallback in Selenium)
        - get_dom_attribute('checked') → 'true'  (actual HTML attribute)
        - get_property('checked')      → True    (boolean DOM property)
    """
    driver = _build_driver()
    driver.get(FORM_PAGE)

    fname = driver.find_element(By.ID, 'fname')

    print(f'get_attribute("value"):     {fname.get_attribute("value")}')
    print(f'get_property("value"):      {fname.get_property("value")}')
    print(f'get_dom_attribute("value"): {fname.get_dom_attribute("value")}')
    print(f'get_dom_attribute("id"):    {fname.get_dom_attribute("id")}')

    # Modify value via JS and compare attribute vs property
    driver.execute_script("arguments[0].value = 'changed';", fname)
    print(f'After JS change:')
    print(f'  get_attribute("value"):     {fname.get_attribute("value")}')   # 'changed'
    print(f'  get_dom_attribute("value"): {fname.get_dom_attribute("value")}')  # 'Jane' (original HTML)
    print(f'  get_property("value"):      {fname.get_property("value")}')    # 'changed'

    driver.quit()


if __name__ == '__main__':
    is_displayed()
    is_enabled()
    is_selected()
    get_tag_name()
    get_size_and_position()
    get_text_content()
    get_attribute_vs_property()
