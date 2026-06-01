# -*- coding: utf-8 -*-
"""
Locator Strategies examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/elements/locators/

Selenium supports 8 traditional locator strategies plus Relative Locators
introduced in Selenium 4.

Traditional locators:
    - By.CLASS_NAME
    - By.CSS_SELECTOR
    - By.ID
    - By.NAME
    - By.LINK_TEXT
    - By.PARTIAL_LINK_TEXT
    - By.TAG_NAME
    - By.XPATH

Relative locators (Selenium 4):
    - above()
    - below()
    - to_left_of()
    - to_right_of()
    - near()
    - chained combinations

HTML reference used in examples:
    <input class="information" type="text" id="fname" name="fname">
    <input class="information" type="text" id="lname" name="lname">
    <a href="www.selenium.dev">Selenium Official Page</a>
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from webdriver_manager.chrome import ChromeDriverManager

LOCATORS_PAGE = 'https://www.selenium.dev/selenium/web/locators_tests/locators.html'
RELATIVE_PAGE = 'https://www.selenium.dev/selenium/web/relative_locators.html'
EXAMPLE_URL = 'https://www.example.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Traditional locators
# ---------------------------------------------------------------------------

def locate_by_class_name():
    """
    By.CLASS_NAME — matches elements that have the given class in their class attribute.
    Returns the first matching element.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.CLASS_NAME, 'information')
    print(f'CLASS_NAME → tag: {element.tag_name}, value: {element.get_attribute("value")}')

    driver.quit()


def locate_by_css_selector():
    """
    By.CSS_SELECTOR — matches elements using standard CSS selector syntax.
    Very powerful and flexible; preferred over XPath for readability.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.CSS_SELECTOR, '#fname')
    print(f'CSS_SELECTOR → id: {element.get_attribute("id")}')

    driver.quit()


def locate_by_id():
    """
    By.ID — matches the element whose id attribute equals the given value.
    Most reliable locator when the id is unique and stable.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.ID, 'lname')
    print(f'ID → name attr: {element.get_attribute("name")}')

    driver.quit()


def locate_by_name():
    """
    By.NAME — matches elements whose name attribute equals the given value.
    Commonly used for form inputs.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.NAME, 'newsletter')
    print(f'NAME → type: {element.get_attribute("type")}')

    driver.quit()


def locate_by_link_text():
    """
    By.LINK_TEXT — matches <a> elements whose full visible text equals the given string.
    Case-sensitive exact match.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.LINK_TEXT, 'Selenium Official Page')
    print(f'LINK_TEXT → href: {element.get_attribute("href")}')

    driver.quit()


def locate_by_partial_link_text():
    """
    By.PARTIAL_LINK_TEXT — matches <a> elements whose visible text contains the given substring.
    Useful when the full link text is dynamic or too long.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.PARTIAL_LINK_TEXT, 'Official Page')
    print(f'PARTIAL_LINK_TEXT → text: {element.text}')

    driver.quit()


def locate_by_tag_name():
    """
    By.TAG_NAME — matches elements by their HTML tag name.
    Returns the first matching element; use find_elements for all matches.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    element = driver.find_element(By.TAG_NAME, 'h1')
    print(f'TAG_NAME → text: {element.text}')

    driver.quit()


def locate_by_xpath():
    """
    By.XPATH — matches elements using XPath expressions.
    Powerful but can be brittle if the DOM structure changes.
    """
    driver = _build_driver()
    driver.get(LOCATORS_PAGE)

    element = driver.find_element(By.XPATH, "//input[@value='f']")
    print(f'XPATH → value: {element.get_attribute("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Relative locators (Selenium 4)
# ---------------------------------------------------------------------------

def relative_locator_above():
    """
    locate_with().above() — find an element that is spatially above another element.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    email_locator = locate_with(By.TAG_NAME, 'input').above({By.ID: 'password'})
    email_field = driver.find_element(email_locator)
    print(f'above() → tag: {email_field.tag_name}')

    driver.quit()


def relative_locator_below():
    """
    locate_with().below() — find an element that is spatially below another element.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    password_locator = locate_with(By.TAG_NAME, 'input').below({By.ID: 'email'})
    password_field = driver.find_element(password_locator)
    print(f'below() → tag: {password_field.tag_name}')

    driver.quit()


def relative_locator_to_left_of():
    """
    locate_with().to_left_of() — find an element that is spatially to the left of another.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    cancel_locator = locate_with(By.TAG_NAME, 'button').to_left_of({By.ID: 'submit'})
    cancel_btn = driver.find_element(cancel_locator)
    print(f'to_left_of() → text: {cancel_btn.text}')

    driver.quit()


def relative_locator_to_right_of():
    """
    locate_with().to_right_of() — find an element that is spatially to the right of another.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    submit_locator = locate_with(By.TAG_NAME, 'button').to_right_of({By.ID: 'cancel'})
    submit_btn = driver.find_element(submit_locator)
    print(f'to_right_of() → text: {submit_btn.text}')

    driver.quit()


def relative_locator_near():
    """
    locate_with().near() — find an element within approximately 50 pixels of another.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    field_locator = locate_with(By.TAG_NAME, 'input').near({By.ID: 'lbl-email'})
    field = driver.find_element(field_locator)
    print(f'near() → tag: {field.tag_name}')

    driver.quit()


def relative_locator_chained():
    """
    Chain multiple relative locators to further narrow down the element.
    Finds a button that is both below the email field and to the right of cancel.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    submit_locator = (
        locate_with(By.TAG_NAME, 'button')
        .below({By.ID: 'email'})
        .to_right_of({By.ID: 'cancel'})
    )
    submit_btn = driver.find_element(submit_locator)
    print(f'chained relative locators → text: {submit_btn.text}')

    driver.quit()


if __name__ == '__main__':
    locate_by_class_name()
    locate_by_css_selector()
    locate_by_id()
    locate_by_xpath()
