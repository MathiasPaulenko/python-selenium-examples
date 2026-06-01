# -*- coding: utf-8 -*-
"""
Mouse Actions examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/actions_api/mouse/

A representation of any pointer device for interacting with a web page.
Uses ActionChains for high-level convenience methods.

Topics covered:
    - Click and hold
    - Click and release
    - Context click (right-click)
    - Back click
    - Forward click
    - Double click
    - Move to element (hover)
    - Move by offset — from element, viewport, current pointer
    - Drag and drop on element
    - Drag and drop by offset
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

MOUSE_PAGE = 'https://www.selenium.dev/selenium/web/mouse_interaction.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Click and hold
# ---------------------------------------------------------------------------

def click_and_hold():
    """
    click_and_hold() moves to the element's center and presses the left mouse
    button without releasing it. Useful for drag start or hold interactions.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    clickable = driver.find_element(By.ID, 'clickable')
    ActionChains(driver) \
        .click_and_hold(clickable) \
        .perform()

    status = driver.find_element(By.ID, 'click-status').text
    print(f'click_and_hold status: {status}')  # focused

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Click and release
# ---------------------------------------------------------------------------

def click_and_release():
    """
    click() combines move to element + left button press + release.
    Standard single left click.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    clickable = driver.find_element(By.ID, 'click')
    ActionChains(driver) \
        .click(clickable) \
        .perform()

    print(f'After click URL contains resultPage: {"resultPage.html" in driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Context click (right-click)
# ---------------------------------------------------------------------------

def context_click():
    """
    context_click() moves to the element and presses the right mouse button.
    Also known as right-click.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    clickable = driver.find_element(By.ID, 'clickable')
    ActionChains(driver) \
        .context_click(clickable) \
        .perform()

    status = driver.find_element(By.ID, 'click-status').text
    print(f'context_click status: {status}')  # context-clicked

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Double click
# ---------------------------------------------------------------------------

def double_click():
    """
    double_click() sends two consecutive left clicks on the target element.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    clickable = driver.find_element(By.ID, 'clickable')
    ActionChains(driver) \
        .double_click(clickable) \
        .perform()

    status = driver.find_element(By.ID, 'click-status').text
    print(f'double_click status: {status}')  # double-clicked

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Move to element (hover)
# ---------------------------------------------------------------------------

def move_to_element():
    """
    move_to_element() moves the mouse pointer to the center of an element.
    Triggers hover/mouseover events.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    hoverable = driver.find_element(By.ID, 'hover')
    ActionChains(driver) \
        .move_to_element(hoverable) \
        .perform()

    status = driver.find_element(By.ID, 'move-status').text
    print(f'move_to_element status: {status}')  # hovered

    driver.quit()


# ---------------------------------------------------------------------------
# 6. Move by offset — from element
# ---------------------------------------------------------------------------

def move_by_offset_from_element():
    """
    move_to_element(element, xoffset, yoffset) moves to the element center
    and then applies the given pixel offset (relative to element center).
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    driver.maximize_window()
    tracker = driver.find_element(By.ID, 'mouse-tracker')

    ActionChains(driver) \
        .move_to_element_with_offset(tracker, 8, 0) \
        .perform()

    location = driver.find_element(By.ID, 'relative-location').text
    print(f'move offset from element — relative location: {location}')

    driver.quit()


# ---------------------------------------------------------------------------
# 7. Move by offset — from viewport origin
# ---------------------------------------------------------------------------

def move_by_offset_from_viewport():
    """
    Move the mouse to an absolute position measured from the top-left
    corner of the viewport. Uses the low-level ActionChains.move_by_offset()
    after an initial move_to_element to a known position.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    # Move to absolute viewport coordinates (8, 12) via JS scroll + offset
    ActionChains(driver) \
        .move_by_offset(8, 12) \
        .perform()

    location = driver.find_element(By.ID, 'absolute-location').text
    print(f'move from viewport — absolute location: {location}')

    driver.quit()


# ---------------------------------------------------------------------------
# 8. Move by offset — from current pointer location
# ---------------------------------------------------------------------------

def move_by_offset_from_current_pointer():
    """
    move_by_offset() moves the pointer relative to its current position.
    Chain multiple offsets for cumulative movement.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    ActionChains(driver) \
        .move_by_offset(8, 11) \
        .move_by_offset(13, 15) \
        .perform()

    location = driver.find_element(By.ID, 'absolute-location').text
    print(f'move from current pointer — location: {location}')

    driver.quit()


# ---------------------------------------------------------------------------
# 9. Drag and drop on element
# ---------------------------------------------------------------------------

def drag_and_drop():
    """
    drag_and_drop(source, target) clicks and holds the source element,
    moves to the target element, and releases.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    draggable = driver.find_element(By.ID, 'draggable')
    droppable = driver.find_element(By.ID, 'droppable')

    ActionChains(driver) \
        .drag_and_drop(draggable, droppable) \
        .perform()

    status = driver.find_element(By.ID, 'drop-status').text
    print(f'drag_and_drop status: {status}')  # dropped

    driver.quit()


# ---------------------------------------------------------------------------
# 10. Drag and drop by offset
# ---------------------------------------------------------------------------

def drag_and_drop_by_offset():
    """
    drag_and_drop_by_offset(source, xoffset, yoffset) drags from the source
    element and releases at the given pixel offset from the source position.
    Compute the offset from the target element's coordinates for precision.
    """
    driver = _build_driver()
    driver.get(MOUSE_PAGE)

    draggable = driver.find_element(By.ID, 'draggable')
    droppable = driver.find_element(By.ID, 'droppable')

    start = draggable.rect
    finish = droppable.rect
    offset_x = finish['x'] - start['x']
    offset_y = finish['y'] - start['y']

    ActionChains(driver) \
        .drag_and_drop_by_offset(draggable, offset_x, offset_y) \
        .perform()

    status = driver.find_element(By.ID, 'drop-status').text
    print(f'drag_and_drop_by_offset status: {status}')  # dropped

    driver.quit()


if __name__ == '__main__':
    click_and_hold()
    click_and_release()
    context_click()
    double_click()
    move_to_element()
    drag_and_drop()
    drag_and_drop_by_offset()
