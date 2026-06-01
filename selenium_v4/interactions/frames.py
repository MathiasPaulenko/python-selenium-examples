# -*- coding: utf-8 -*-
"""
Working with IFrames and Frames examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/interactions/frames/

Frames are deprecated HTML layout elements. IFrames embed content from a
different document (possibly a different domain) and are still commonly used.

To interact with elements inside a frame or iframe, you must switch the
WebDriver context into that frame first.

Ways to switch to a frame:
    1. Using a WebElement reference
    2. Using a name or id attribute
    3. Using an index (0-based position in the DOM)

To leave a frame, use driver.switch_to.default_content() to return to the
top-level document, or driver.switch_to.parent_frame() to go one level up.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

IFRAME_PAGE = 'https://www.selenium.dev/selenium/web/iframes.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Switch using a WebElement
# ---------------------------------------------------------------------------

def switch_to_frame_by_element():
    """
    Locate the iframe as a WebElement and pass it to switch_to.frame().
    This is the most reliable method as it uses the standard locator API.
    """
    driver = _build_driver()
    driver.get(IFRAME_PAGE)

    # Locate the iframe element
    iframe = driver.find_element(By.TAG_NAME, 'iframe')

    # Switch context into the iframe
    driver.switch_to.frame(iframe)

    # Now we can interact with elements inside the iframe
    body = driver.find_element(By.TAG_NAME, 'body')
    print(f'Inside iframe body text: {body.text[:80]}')

    # Switch back to the top-level document
    driver.switch_to.default_content()
    print('Switched back to main document')

    driver.quit()


def switch_to_frame_by_element_with_wait():
    """
    Wait for the iframe to be available and then switch to it.
    EC.frame_to_be_available_and_switch_to_it handles both the wait and the switch.
    """
    driver = _build_driver()
    driver.get(IFRAME_PAGE)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        (By.TAG_NAME, 'iframe')
    ))

    body = driver.find_element(By.TAG_NAME, 'body')
    print(f'Iframe body (with wait): {body.text[:80]}')

    driver.switch_to.default_content()
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Switch using name or id
# ---------------------------------------------------------------------------

def switch_to_frame_by_name_or_id():
    """
    Switch to a frame using its name or id attribute value.
    The string passed to switch_to.frame() is matched against both attributes.
    """
    driver = _build_driver()
    driver.get(IFRAME_PAGE)

    # Switch using name or id attribute
    driver.switch_to.frame('iframe1')  # matches name="iframe1" or id="iframe1"

    body = driver.find_element(By.TAG_NAME, 'body')
    print(f'Switched by name/id: {body.text[:80]}')

    driver.switch_to.default_content()
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Switch using index
# ---------------------------------------------------------------------------

def switch_to_frame_by_index():
    """
    Switch to a frame using its zero-based index in the DOM.
    The first frame found is index 0, the second is index 1, and so on.
    Use as a last resort — index-based switching is fragile if page structure changes.
    """
    driver = _build_driver()
    driver.get(IFRAME_PAGE)

    driver.switch_to.frame(0)  # First iframe on the page

    body = driver.find_element(By.TAG_NAME, 'body')
    print(f'Switched by index 0: {body.text[:80]}')

    driver.switch_to.default_content()
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Leaving a frame
# ---------------------------------------------------------------------------

def leave_frame_default_content():
    """
    Return to the top-level document from inside any frame level.
    driver.switch_to.default_content() always goes to the root.
    """
    driver = _build_driver()
    driver.get(IFRAME_PAGE)

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)
    print('Inside iframe')

    driver.switch_to.default_content()
    print('Back to top-level document')

    # Now we can locate elements in the main page again
    driver.find_element(By.TAG_NAME, 'body')

    driver.quit()


def leave_frame_parent():
    """
    Move one level up in the frame hierarchy using switch_to.parent_frame().
    Useful with nested frames — goes to parent without jumping to root.
    """
    driver = _build_driver()
    driver.get(IFRAME_PAGE)

    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)
    print('Inside iframe')

    driver.switch_to.parent_frame()
    print('Moved to parent frame (top-level in this case)')

    driver.quit()


if __name__ == '__main__':
    switch_to_frame_by_element()
    switch_to_frame_by_index()
    leave_frame_default_content()
