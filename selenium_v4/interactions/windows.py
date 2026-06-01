# -*- coding: utf-8 -*-
"""
Working with windows and tabs examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/interactions/windows/

WebDriver does not distinguish between windows and tabs — both are
identified by a unique window handle string.

Topics covered:
    - Get window handle
    - Get all window handles
    - Switch between windows/tabs
    - Open new window or tab and switch
    - Close a window or tab
    - Quit the browser
    - Window management (size, position, maximize, minimize, fullscreen)
    - Take screenshot (full page and element)
    - Execute JavaScript
    - Print page to PDF
"""

from __future__ import annotations

import base64
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

EXAMPLE_URL = 'https://www.example.com/'
SELENIUM_URL = 'https://www.selenium.dev/'
OUTPUT_DIR = Path(__file__).parents[3] / 'output'


def _build_driver(options: webdriver.ChromeOptions | None = None) -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options or webdriver.ChromeOptions())


# ---------------------------------------------------------------------------
# 1. Window handles
# ---------------------------------------------------------------------------

def get_window_handle():
    """
    Get the handle of the current window.
    Each window/tab has a unique identifier string.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    handle = driver.current_window_handle
    print(f'Current window handle: {handle}')

    driver.quit()


def get_all_window_handles():
    """
    Get all open window handles in the current session.
    Returns a set of handle strings.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    handles = driver.window_handles
    print(f'Total open windows: {len(handles)}')
    for h in handles:
        print(f'  handle: {h}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Switching windows or tabs
# ---------------------------------------------------------------------------

def switch_to_window():
    """
    Switch focus to a specific window or tab using its handle.
    After switching, all WebDriver commands target the new window.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    original_handle = driver.current_window_handle

    # Open a link that opens a new window/tab
    driver.execute_script("window.open('https://www.selenium.dev/', '_blank');")

    wait = WebDriverWait(driver, 5)
    wait.until(EC.number_of_windows_to_be(2))

    for handle in driver.window_handles:
        if handle != original_handle:
            driver.switch_to.window(handle)
            break

    print(f'Switched to: {driver.current_url}')

    # Switch back to original
    driver.switch_to.window(original_handle)
    print(f'Switched back to: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Create new window or tab and switch
# ---------------------------------------------------------------------------

def open_new_tab():
    """
    Open a new tab and switch to it using driver.switch_to.new_window('tab').
    Selenium 4 introduces this API to open new tabs without JavaScript tricks.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.switch_to.new_window('tab')
    driver.get(SELENIUM_URL)
    print(f'New tab URL: {driver.current_url}')

    driver.quit()


def open_new_window():
    """
    Open a new browser window and switch to it.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.switch_to.new_window('window')
    driver.get(SELENIUM_URL)
    print(f'New window URL: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Close window or tab
# ---------------------------------------------------------------------------

def close_window_and_switch_back():
    """
    Close the current window/tab and switch back to the previous one.
    Always switch to another handle before closing, or the session ends.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)
    original_handle = driver.current_window_handle

    driver.switch_to.new_window('tab')
    driver.get(SELENIUM_URL)

    driver.close()  # Close the new tab

    driver.switch_to.window(original_handle)
    print(f'Back to original: {driver.current_url}')

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Window management — size and position
# ---------------------------------------------------------------------------

def get_window_size():
    """Get the current window width and height in pixels."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    size = driver.get_window_size()
    print(f'Width: {size["width"]}, Height: {size["height"]}')

    driver.quit()


def set_window_size():
    """Set the browser window to a specific width and height."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.set_window_size(1024, 768)
    size = driver.get_window_size()
    print(f'Set size — Width: {size["width"]}, Height: {size["height"]}')

    driver.quit()


def get_window_position():
    """Get the current x, y position of the browser window on screen."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    position = driver.get_window_position()
    print(f'X: {position["x"]}, Y: {position["y"]}')

    driver.quit()


def set_window_position():
    """Move the browser window to a specific screen coordinate."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.set_window_position(100, 200)
    position = driver.get_window_position()
    print(f'Position — X: {position["x"]}, Y: {position["y"]}')

    driver.quit()


def maximize_window():
    """Maximize the browser window to fill the screen."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.maximize_window()
    print(f'Maximized size: {driver.get_window_size()}')

    driver.quit()


def minimize_window():
    """Minimize the browser window to the taskbar."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.minimize_window()
    print('Window minimized')

    driver.quit()


def fullscreen_window():
    """Set the browser to fullscreen mode (like pressing F11)."""
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    driver.fullscreen_window()
    print('Window in fullscreen mode')

    driver.quit()


# ---------------------------------------------------------------------------
# 6. Screenshots
# ---------------------------------------------------------------------------

def take_screenshot():
    """
    Capture a screenshot of the current viewport and save it to a file.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    path = OUTPUT_DIR / 'screenshot.png'
    driver.save_screenshot(str(path))
    print(f'Screenshot saved: {path}')

    driver.quit()


def take_element_screenshot():
    """
    Capture a screenshot of a specific element only.
    Useful for visual comparison of individual components.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    heading = driver.find_element(By.TAG_NAME, 'h1')
    path = OUTPUT_DIR / 'element_screenshot.png'
    heading.screenshot(str(path))
    print(f'Element screenshot saved: {path}')

    driver.quit()


# ---------------------------------------------------------------------------
# 7. Execute JavaScript
# ---------------------------------------------------------------------------

def execute_script():
    """
    Execute synchronous JavaScript in the context of the current page.
    Use execute_script() to interact with the DOM directly or run JS logic.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    title = driver.execute_script('return document.title;')
    print(f'Title via JS: {title}')

    driver.execute_script("document.title = 'Modified by Selenium';")
    print(f'Modified title: {driver.title}')

    driver.quit()


def execute_async_script():
    """
    Execute asynchronous JavaScript — useful for waiting on Promises or callbacks.
    The script must call the callback (last argument) to signal completion.
    """
    driver = _build_driver()
    driver.get(EXAMPLE_URL)

    result = driver.execute_async_script(
        'var callback = arguments[arguments.length - 1];'
        'setTimeout(function() { callback("async done"); }, 500);'
    )
    print(f'Async result: {result}')

    driver.quit()


# ---------------------------------------------------------------------------
# 8. Print page to PDF
# ---------------------------------------------------------------------------

def print_page_to_pdf():
    """
    Print the current page as a base64-encoded PDF.
    Requires headless mode to work in Chrome.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')

    driver = _build_driver(options)
    driver.get(EXAMPLE_URL)

    pdf_base64 = driver.print_page()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / 'page.pdf'
    pdf_path.write_bytes(base64.b64decode(pdf_base64))
    print(f'PDF saved to: {pdf_path}')

    driver.quit()


if __name__ == '__main__':
    get_window_handle()
    switch_to_window()
    open_new_tab()
    take_screenshot()
    execute_script()
