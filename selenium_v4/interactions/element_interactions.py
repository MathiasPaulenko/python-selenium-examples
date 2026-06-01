# -*- coding: utf-8 -*-
"""
Interacting with Web Elements examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/elements/interactions/

High-level instructions for manipulating form controls and elements.

Before performing any interaction, Selenium performs built-in validations:
    - The element must be visible (is_displayed == True)
    - The element must be enabled (is_enabled == True)

Topics covered:
    - Click
    - Send keys (type into input / textarea)
    - Clear (empty an input)
    - Select (dropdown)
    - Submit
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

INPUTS_PAGE = 'https://www.selenium.dev/selenium/web/inputs.html'
FORM_PAGE = 'https://www.selenium.dev/selenium/web/locators_tests/locators.html'
DROPDOWN_PAGE = 'https://www.selenium.dev/selenium/web/formPage.html'
EXAMPLE_URL = 'https://www.example.com/'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Click
# ---------------------------------------------------------------------------

def click_element():
    """
    Click a web element.
    Selenium validates that the element is visible and enabled before clicking.
    """
    driver = _build_driver()
    driver.get(INPUTS_PAGE)

    checkbox = driver.find_element(By.NAME, 'checkbox_input')
    print(f'Before click selected: {checkbox.is_selected()}')

    checkbox.click()
    print(f'After click selected: {checkbox.is_selected()}')

    driver.quit()


def click_link():
    """Click an anchor/link element to navigate to its href."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    link = driver.find_element(By.TAG_NAME, 'a')
    print(f'Clicking link: {link.text}')
    link.click()
    print(f'Navigated to: {driver.current_url}')

    driver.quit()


def click_button():
    """Click a button element."""
    driver = _build_driver()
    driver.get(FORM_PAGE)

    submit = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    submit.click()
    print(f'After submit URL: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Send keys
# ---------------------------------------------------------------------------

def send_keys_to_input():
    """
    Type text into an input or textarea element using send_keys().
    Characters are sent one by one, simulating actual keyboard input.
    """
    driver = _build_driver()
    driver.get(INPUTS_PAGE)

    text_input = driver.find_element(By.NAME, 'text_input')
    text_input.send_keys('Selenium automation')
    print(f'Input value: {text_input.get_property("value")}')

    driver.quit()


def send_keys_with_special_keys():
    """
    Use Keys constants to send special keys like Tab, Enter, Backspace, etc.
    """
    driver = _build_driver()
    driver.get(INPUTS_PAGE)

    text_input = driver.find_element(By.NAME, 'text_input')
    text_input.send_keys('Hello')
    text_input.send_keys(Keys.BACK_SPACE * 2)  # Delete last 2 chars → 'Hel'
    print(f'After backspace: {text_input.get_property("value")}')

    text_input.send_keys(Keys.CONTROL, 'a')   # Select all
    text_input.send_keys(Keys.DELETE)         # Delete selected
    print(f'After select+delete: {text_input.get_property("value")}')

    driver.quit()


def send_keys_to_textarea():
    """
    Type multiline text into a textarea element.
    """
    driver = _build_driver()
    driver.get(INPUTS_PAGE)

    textarea = driver.find_element(By.NAME, 'textarea_input')
    textarea.send_keys('Line 1\nLine 2\nLine 3')
    print(f'Textarea value: {textarea.get_property("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Clear
# ---------------------------------------------------------------------------

def clear_input():
    """
    Clear the current value of an editable element (input or textarea).
    Works only on editable and resettable elements.
    """
    driver = _build_driver()
    driver.get(INPUTS_PAGE)

    text_input = driver.find_element(By.NAME, 'text_input')
    text_input.send_keys('text to clear')
    print(f'Before clear: {text_input.get_property("value")}')

    text_input.clear()
    print(f'After clear: {text_input.get_property("value")}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Select dropdown
# ---------------------------------------------------------------------------

def select_by_visible_text():
    """
    Select an option from a <select> dropdown by its visible text.
    Requires wrapping the element with the Select helper class.
    """
    driver = _build_driver()
    driver.get(DROPDOWN_PAGE)

    dropdown = driver.find_element(By.NAME, 'selectomatic')
    select = Select(dropdown)

    select.select_by_visible_text('One')
    print(f'Selected: {select.first_selected_option.text}')

    driver.quit()


def select_by_value():
    """Select an option by its value attribute."""
    driver = _build_driver()
    driver.get(DROPDOWN_PAGE)

    dropdown = driver.find_element(By.NAME, 'selectomatic')
    select = Select(dropdown)

    select.select_by_value('two')
    print(f'Selected value: {select.first_selected_option.get_attribute("value")}')

    driver.quit()


def select_by_index():
    """Select an option by its zero-based index in the list."""
    driver = _build_driver()
    driver.get(DROPDOWN_PAGE)

    dropdown = driver.find_element(By.NAME, 'selectomatic')
    select = Select(dropdown)

    select.select_by_index(0)
    print(f'Selected index 0: {select.first_selected_option.text}')

    driver.quit()


def get_all_options():
    """Get all options available in a dropdown."""
    driver = _build_driver()
    driver.get(DROPDOWN_PAGE)

    dropdown = driver.find_element(By.NAME, 'selectomatic')
    select = Select(dropdown)

    options = select.options
    print(f'All options ({len(options)}):')
    for opt in options:
        print(f'  {opt.text} (value={opt.get_attribute("value")})')

    driver.quit()


if __name__ == '__main__':
    click_element()
    send_keys_to_input()
    send_keys_with_special_keys()
    clear_input()
    select_by_visible_text()
