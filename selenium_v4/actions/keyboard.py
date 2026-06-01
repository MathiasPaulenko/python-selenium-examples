# -*- coding: utf-8 -*-
"""
Keyboard Actions examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/actions_api/keyboard/

A representation of any key input device for interacting with a web page.
Uses ActionChains (the Python equivalent of the Java Actions builder).

Topics covered:
    - Key down    — Press and hold a key
    - Key up      — Release a held key
    - Send keys   — To the active element (focused)
    - Send keys   — To a designated element
    - Copy and paste — Using keyboard shortcuts
"""

from __future__ import annotations

import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

KEYBOARD_PAGE = 'https://www.selenium.dev/selenium/web/single_text_input.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Key down
# ---------------------------------------------------------------------------

def key_down():
    """
    key_down() presses a key and holds it.
    Here we hold Shift while sending 'abc' — resulting in uppercase 'ABC'.
    """
    driver = _build_driver()
    driver.get(KEYBOARD_PAGE)

    ActionChains(driver) \
        .key_down(Keys.SHIFT) \
        .send_keys('abc') \
        .perform()

    text_input = driver.find_element(By.ID, 'textInput')
    print(f'key_down result: {text_input.get_attribute("value")}')  # ABC

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Key up
# ---------------------------------------------------------------------------

def key_up():
    """
    key_up() releases a previously held key.
    Hold Shift for 'a' (uppercase 'A'), release Shift, then type 'b' (lowercase).
    Result: 'Ab'
    """
    driver = _build_driver()
    driver.get(KEYBOARD_PAGE)

    ActionChains(driver) \
        .key_down(Keys.SHIFT) \
        .send_keys('a') \
        .key_up(Keys.SHIFT) \
        .send_keys('b') \
        .perform()

    text_input = driver.find_element(By.ID, 'textInput')
    print(f'key_up result: {text_input.get_attribute("value")}')  # Ab

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Send keys — active element
# ---------------------------------------------------------------------------

def send_keys_to_active_element():
    """
    ActionChains.send_keys() sends keystrokes to whichever element currently
    has keyboard focus (the active element).
    No explicit element reference is needed.
    """
    driver = _build_driver()
    driver.get(KEYBOARD_PAGE)

    ActionChains(driver) \
        .send_keys('abc') \
        .perform()

    text_input = driver.find_element(By.ID, 'textInput')
    print(f'send_keys active element: {text_input.get_attribute("value")}')  # abc

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Send keys — designated element
# ---------------------------------------------------------------------------

def send_keys_to_designated_element():
    """
    ActionChains.send_keys_to_element() targets a specific element explicitly,
    regardless of which element currently has focus.
    """
    driver = _build_driver()
    driver.get(KEYBOARD_PAGE)

    driver.find_element(By.TAG_NAME, 'body').click()  # Remove focus from input
    text_input = driver.find_element(By.ID, 'textInput')

    ActionChains(driver) \
        .send_keys_to_element(text_input, 'Selenium!') \
        .perform()

    print(f'send_keys to element: {text_input.get_attribute("value")}')  # Selenium!

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Copy and paste
# ---------------------------------------------------------------------------

def copy_and_paste():
    """
    Demonstrate copy and paste using keyboard shortcuts.
    Uses COMMAND on macOS and CONTROL on other platforms.

    Sequence:
        1. Type 'Selenium!'
        2. Move cursor to start (ARROW_LEFT)
        3. Select all text (SHIFT + ARROW_UP)
        4. Cut (Ctrl/Cmd + x)
        5. Paste twice (Ctrl/Cmd + vv)
    Result: 'SeleniumSelenium!'
    """
    driver = _build_driver()
    driver.get(KEYBOARD_PAGE)

    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    text_input = driver.find_element(By.ID, 'textInput')

    ActionChains(driver) \
        .send_keys_to_element(text_input, 'Selenium!') \
        .send_keys(Keys.ARROW_LEFT) \
        .key_down(Keys.SHIFT) \
        .send_keys(Keys.ARROW_UP) \
        .key_up(Keys.SHIFT) \
        .key_down(cmd_ctrl) \
        .send_keys('xvv') \
        .key_up(cmd_ctrl) \
        .perform()

    print(f'copy_and_paste result: {text_input.get_attribute("value")}')  # SeleniumSelenium!

    driver.quit()


if __name__ == '__main__':
    key_down()
    key_up()
    send_keys_to_active_element()
    send_keys_to_designated_element()
    copy_and_paste()
