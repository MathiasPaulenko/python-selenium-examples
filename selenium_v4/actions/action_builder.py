# -*- coding: utf-8 -*-
"""
Actions API — Action Builder examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/actions_api/

The Actions API provides a low-level interface for virtualizing input device
actions (keyboard, mouse, pen, wheel). In Selenium 4, the W3C WebDriver
Protocol defines detailed building blocks for each device.

In practice, you rarely need to use the low-level builder directly because
ActionChains provides convenient methods that combine the lower-level commands.

Topics covered:
    - Pause (add a timed delay between actions)
    - Release all actions (reset all input device states)
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

MOUSE_PAGE = 'https://www.selenium.dev/selenium/web/mouse_interaction.html'
KEYBOARD_PAGE = 'https://www.selenium.dev/selenium/web/single_text_input.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Pause
# ---------------------------------------------------------------------------

def pause_between_actions():
    """
    ActionChains.pause() inserts a timed delay in the action sequence.
    Useful to synchronize actions with page animations or transitions.
    The duration is in seconds (float).
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    clickable = driver.find_element(By.ID, 'clickable')

    ActionChains(driver) \
        .move_to_element(clickable) \
        .pause(0.5) \
        .click_and_hold(clickable) \
        .pause(0.5) \
        .release() \
        .perform()

    print('Pause between actions performed')
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Release all actions
# ---------------------------------------------------------------------------

def release_all_actions():
    """
    driver.execute(Command.W3C_ACTIONS) or ActionChains.reset_actions() resets
    the state of all input devices (releases any held keys or mouse buttons).

    Selenium Python binding exposes this as ActionChains.reset_actions(),
    which sends a release for every device that has been used.
    """
    driver = _build_driver()
    driver.get(KEYBOARD_PAGE)

    actions = ActionChains(driver)

    # Start holding Shift
    actions.key_down('a').perform()

    # Release all inputs — equivalent to calling reset_actions
    actions.reset_actions()

    print('All actions released')
    driver.quit()


if __name__ == '__main__':
    pause_between_actions()
    release_all_actions()
