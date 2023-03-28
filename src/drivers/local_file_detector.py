"""
The Local File Detector allows the transfer of files from the client machine to the remote server. For example, if a
test needs to upload a file to a web application, a remote WebDriver can automatically transfer the file from the local
machine to the remote web server during runtime. This allows the file to be uploaded from the remote machine running the
test.
It is not enabled by default and can be enabled using the LocalFileDetector object.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector


def local_file_detector():
    """
    Configuring the LocalFileDetector object on a remote drive instance.
    """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444',
        options=chrome_options
    )

    driver.file_detector = LocalFileDetector()
    driver.get('https://www.example.com/')
    element = driver.find_element(By.ID, 'file_upload')
    element.send_keys('path/to/file.jpg')
    # do something
    driver.quit()


if __name__ == '__main__':
    local_file_detector()
