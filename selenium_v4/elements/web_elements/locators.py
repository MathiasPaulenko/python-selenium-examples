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
    The page contains stacked paragraphs (#above, #mid, #below).
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    locator = locate_with(By.TAG_NAME, 'p').above({By.ID: 'mid'})
    element = driver.find_element(locator)
    print(f'above(#mid) → id: {element.get_attribute("id")}, text: {element.text}')

    driver.quit()


def relative_locator_below():
    """
    locate_with().below() — find an element that is spatially below another element.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    locator = locate_with(By.TAG_NAME, 'p').below({By.ID: 'above'})
    element = driver.find_element(locator)
    print(f'below(#above) → id: {element.get_attribute("id")}, text: {element.text}')

    driver.quit()


def relative_locator_to_left_of():
    """
    locate_with().to_left_of() — find an element that is spatially to the left of another.
    The page contains a 3x3 table (#topLeft .. #bottomRight).
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    locator = locate_with(By.TAG_NAME, 'td').to_left_of({By.ID: 'center'})
    element = driver.find_element(locator)
    print(f'to_left_of(#center) → id: {element.get_attribute("id")}, text: {element.text}')

    driver.quit()


def relative_locator_to_right_of():
    """
    locate_with().to_right_of() — find an element that is spatially to the right of another.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    locator = locate_with(By.TAG_NAME, 'td').to_right_of({By.ID: 'center'})
    element = driver.find_element(locator)
    print(f'to_right_of(#center) → id: {element.get_attribute("id")}, text: {element.text}')

    driver.quit()


def relative_locator_near():
    """
    locate_with().near() — find an element within approximately 50 pixels of another.
    #rect2 sits right next to #rect1 in the proximity section.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    locator = locate_with(By.TAG_NAME, 'div').near({By.ID: 'rect1'})
    element = driver.find_element(locator)
    print(f'near(#rect1) → id: {element.get_attribute("id")}, text: {element.text[:40]}')

    driver.quit()


def relative_locator_chained():
    """
    Chain multiple relative locators to further narrow down the element.
    Finds the cell that is both above #bottom and to the right of #left → #center.
    """
    driver = _build_driver()
    driver.get(RELATIVE_PAGE)

    locator = (
        locate_with(By.TAG_NAME, 'td')
        .above({By.ID: 'bottom'})
        .to_right_of({By.ID: 'left'})
    )
    element = driver.find_element(locator)
    print(f'chained relative locators → id: {element.get_attribute("id")}, text: {element.text}')

    driver.quit()


if __name__ == '__main__':
    locate_by_class_name()
    locate_by_css_selector()
    locate_by_id()
    locate_by_name()
    locate_by_link_text()
    locate_by_partial_link_text()
    locate_by_tag_name()
    locate_by_xpath()
    relative_locator_above()
    relative_locator_below()
    relative_locator_to_left_of()
    relative_locator_to_right_of()
    relative_locator_near()
    relative_locator_chained()
