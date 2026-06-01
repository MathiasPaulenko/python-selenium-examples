# -*- coding: utf-8 -*-
"""
File Upload examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/elements/file_upload/

Selenium cannot interact with the OS-level file picker dialog.
Instead, for <input type="file"> elements, use send_keys() with the
absolute path to the file — this bypasses the dialog entirely.

Topics:
    - Basic file upload via send_keys on <input type="file">
    - Upload and verify the result
    - Upload multiple files
    - Upload in headless mode
    - Remote file upload with LocalFileDetector
"""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

UPLOAD_PAGE = 'https://the-internet.herokuapp.com/upload'
RESOURCES_DIR = Path(__file__).parents[3] / 'resources'


def _build_driver(options: webdriver.ChromeOptions | None = None) -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options or webdriver.ChromeOptions())


def _get_upload_file() -> str:
    """Return absolute path to a file suitable for upload tests."""
    path = RESOURCES_DIR / 'chromedriver.exe'
    if not path.exists():
        raise FileNotFoundError(f'Upload test file not found: {path}')
    return str(path.resolve())


# ---------------------------------------------------------------------------
# 1. Basic file upload
# ---------------------------------------------------------------------------

def upload_file_basic():
    """
    Upload a file by sending its absolute path to the <input type="file"> element.
    Selenium bypasses the OS file dialog entirely — no dialog interaction needed.
    """
    driver = _build_driver()
    driver.get(UPLOAD_PAGE)

    upload_file = _get_upload_file()
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(upload_file)

    driver.find_element(By.ID, 'file-submit').click()

    wait = WebDriverWait(driver, 10)
    uploaded = wait.until(EC.visibility_of_element_located((By.ID, 'uploaded-files')))
    print(f'Uploaded file name: {uploaded.text}')

    driver.quit()


# ---------------------------------------------------------------------------
# 2. Upload and verify result
# ---------------------------------------------------------------------------

def upload_and_verify():
    """
    Upload a file and assert the server confirmed the correct filename.
    """
    driver = _build_driver()
    driver.get(UPLOAD_PAGE)

    upload_path = _get_upload_file()
    expected_filename = Path(upload_path).name

    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(upload_path)
    driver.find_element(By.ID, 'file-submit').click()

    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.visibility_of_element_located((By.ID, 'uploaded-files')))
    actual_filename = result.text

    assert actual_filename == expected_filename, (
        f'Expected "{expected_filename}", got "{actual_filename}"'
    )
    print(f'Upload verified: {actual_filename}')

    driver.quit()


# ---------------------------------------------------------------------------
# 3. Upload multiple files
# ---------------------------------------------------------------------------

def upload_multiple_files():
    """
    Send multiple file paths separated by newlines to upload several files at once.
    The <input> must have the 'multiple' attribute for this to work.
    """
    driver = _build_driver()
    driver.get(UPLOAD_PAGE)

    upload_path = _get_upload_file()

    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    # Separate multiple paths with a newline
    file_input.send_keys(f'{upload_path}\n{upload_path}')

    print('Multiple files sent to input (requires "multiple" attribute on input)')

    driver.quit()


# ---------------------------------------------------------------------------
# 4. Upload in headless mode
# ---------------------------------------------------------------------------

def upload_file_headless():
    """
    File upload via send_keys works identically in headless mode.
    No additional configuration is needed.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')

    driver = _build_driver(options)
    driver.get(UPLOAD_PAGE)

    upload_path = _get_upload_file()
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(upload_path)
    driver.find_element(By.ID, 'file-submit').click()

    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.visibility_of_element_located((By.ID, 'uploaded-files')))
    print(f'Headless upload result: {result.text}')

    driver.quit()


# ---------------------------------------------------------------------------
# 5. Remote file upload with LocalFileDetector
# ---------------------------------------------------------------------------

def upload_file_remote():
    """
    When running against a remote WebDriver (Selenium Grid), the file exists on
    the local machine but needs to be transferred to the remote node.
    LocalFileDetector handles this automatically.

    Requires a running Selenium Grid at GRID_URL.
    """
    from selenium.webdriver.remote.file_detector import LocalFileDetector

    GRID_URL = 'http://localhost:4444/wd/hub'
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Remote(
        command_executor=GRID_URL,
        options=chrome_options,
    )
    driver.file_detector = LocalFileDetector()

    driver.get(UPLOAD_PAGE)
    upload_path = os.path.abspath(str(RESOURCES_DIR / 'chromedriver.exe'))
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(upload_path)
    driver.find_element(By.ID, 'file-submit').click()

    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.visibility_of_element_located((By.ID, 'uploaded-files')))
    print(f'Remote upload result: {result.text}')

    driver.quit()


if __name__ == '__main__':
    upload_file_basic()
    upload_and_verify()
