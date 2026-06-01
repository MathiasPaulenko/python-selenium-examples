# -*- coding: utf-8 -*-
"""
Scroll Wheel Actions examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/actions_api/wheel/

A representation of a scroll wheel input device for interacting with a web page.
All scroll actions use ActionChains with the scroll_* methods introduced in Selenium 4.

Topics covered:
    - Scroll to element               — bring an element into the viewport
    - Scroll by given amount          — scroll by pixel delta from viewport
    - Scroll from element by amount   — scroll inside a scrollable container
    - Scroll from element with offset — scroll starting offset from element center
    - Scroll from viewport origin     — scroll from a fixed viewport point
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

SCROLL_PAGE_NESTED = (
    'https://www.selenium.dev/selenium/web/'
    'scrolling_tests/frame_with_nested_scrolling_frame_out_of_view.html'
)
SCROLL_PAGE = (
    'https://www.selenium.dev/selenium/web/'
    'scrolling_tests/frame_with_nested_scrolling_frame.html'
)


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Scroll to element
# ---------------------------------------------------------------------------

def scroll_to_element():
    """
    scroll_to_element() scrolls the page until the target element is visible
    in the viewport. Equivalent to scrollIntoView() in JavaScript.
    """
    driver = _build_driver()
    driver.get(SCROLL_PAGE_NESTED)

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    ActionChains(driver) \
        .scroll_to_element(iframe) \
        .perform()

    print(f'iframe in viewport after scroll: {iframe.is_displayed()}')
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Scroll by given amount
# ---------------------------------------------------------------------------

def scroll_by_given_amount():
    """
    scroll_by_amount(delta_x, delta_y) scrolls the page by the specified
    number of pixels from the current viewport position.
    Positive delta_y scrolls down; negative scrolls up.
    """
    driver = _build_driver()
    driver.get(SCROLL_PAGE_NESTED)

    footer = driver.find_element(By.TAG_NAME, 'footer')
    delta_y = footer.rect['y']

    ActionChains(driver) \
        .scroll_by_amount(0, delta_y) \
        .perform()

    print(f'footer visible after scroll: {footer.is_displayed()}')
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Scroll from element by given amount
# ---------------------------------------------------------------------------

def scroll_from_element_by_amount():
    """
    ScrollOrigin.from_element(element) sets the scroll origin to the element.
    scroll_from_origin() then scrolls by the specified amount from that origin.
    Useful to scroll inside a scrollable container element.
    """
    driver = _build_driver()
    driver.get(SCROLL_PAGE_NESTED)

    from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    scroll_origin = ScrollOrigin.from_element(iframe)

    ActionChains(driver) \
        .scroll_from_origin(scroll_origin, 0, 200) \
        .perform()

    driver.switch_to.frame(iframe)
    wait = WebDriverWait(driver, 5)
    checkbox = wait.until(EC.presence_of_element_located((By.NAME, 'scroll_checkbox')))
    print(f'checkbox visible inside iframe: {checkbox.is_displayed()}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Scroll from element with offset
# ---------------------------------------------------------------------------

def scroll_from_element_with_offset():
    """
    ScrollOrigin.from_element(element, x_offset, y_offset) offsets the scroll
    origin from the element's center before starting the scroll.
    Useful when the target element is partially off-screen.
    """
    driver = _build_driver()
    driver.get(SCROLL_PAGE_NESTED)

    from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

    footer = driver.find_element(By.TAG_NAME, 'footer')
    scroll_origin = ScrollOrigin.from_element(footer, 0, -50)

    ActionChains(driver) \
        .scroll_from_origin(scroll_origin, 0, 200) \
        .perform()

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

    wait = WebDriverWait(driver, 5)
    checkbox = wait.until(EC.presence_of_element_located((By.NAME, 'scroll_checkbox')))
    print(f'checkbox visible after offset scroll: {checkbox.is_displayed()}')

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Scroll from viewport origin by given amount
# ---------------------------------------------------------------------------

def scroll_from_viewport_origin():
    """
    ScrollOrigin.from_viewport(x, y) sets the scroll origin to a fixed point
    within the viewport (measured from the top-left corner).
    """
    driver = _build_driver()
    driver.get(SCROLL_PAGE)

    from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

    scroll_origin = ScrollOrigin.from_viewport(10, 10)

    ActionChains(driver) \
        .scroll_from_origin(scroll_origin, 0, 200) \
        .perform()

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

    wait = WebDriverWait(driver, 5)
    checkbox = wait.until(EC.presence_of_element_located((By.NAME, 'scroll_checkbox')))
    print(f'checkbox visible after viewport origin scroll: {checkbox.is_displayed()}')

    driver.quit()


if __name__ == '__main__':
    scroll_to_element()
    scroll_by_given_amount()
    scroll_from_element_by_amount()
    scroll_from_viewport_origin()
