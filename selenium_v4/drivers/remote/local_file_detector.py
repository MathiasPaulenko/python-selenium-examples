# -*- coding: utf-8 -*-
"""
The Local File Detector allows the transfer of files from the client machine to the remote server. For example, if a
test needs to upload a file to a web application, a remote WebDriver can automatically transfer the file from the local
machine to the remote web server during runtime. This allows the file to be uploaded from the remote machine running the
test.
It is not enabled by default and can be enabled using the LocalFileDetector object.
"""
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector

UPLOAD_PAGE = 'https://the-internet.herokuapp.com/upload'
GRID_URL = 'http://127.0.0.1:4444/wd/hub'


def _sample_upload_file() -> str:
    """Create (if needed) and return a local file to upload."""
    path = Path(__file__).resolve().parents[3] / 'resources' / 'upload_example.txt'
    if not path.exists():
        path.write_text('Sample file for Selenium file-upload examples.\n')
    return str(path)


def local_file_detector():
    """
    Configure LocalFileDetector on a Selenium 4 Remote WebDriver session.

    Requires a running Selenium Grid at GRID_URL. The page under test is the
    public upload demo at the-internet.herokuapp.com/upload.
    """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=GRID_URL,
        options=chrome_options
    )

    driver.file_detector = LocalFileDetector()
    driver.get(UPLOAD_PAGE)

    file_input = driver.find_element(By.ID, 'file-upload')
    file_input.send_keys(_sample_upload_file())
    driver.find_element(By.ID, 'file-submit').click()

    uploaded = driver.find_element(By.ID, 'uploaded-files')
    print(f'Uploaded file: {uploaded.text}')

    driver.quit()


if __name__ == '__main__':
    local_file_detector()
