# -*- coding: utf-8 -*-
"""
Remote session management with Selenium 4.

Remote sessions require a valid Selenium Grid/remote endpoint URL and
browser-specific options. This file covers inspecting an active session
(session id, returned capabilities) and the difference between
driver.close() and driver.quit().
"""
from selenium import webdriver


REMOTE_URL = 'http://127.0.0.1:4444/wd/hub'


def remote_session_metadata():
    """
    Create a remote session and inspect its metadata.
    driver.session_id identifies the session on the Grid node.
    driver.capabilities returns the capabilities the remote end negotiated.
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)

    print(f'Session id: {driver.session_id}')
    print(f'Browser: {driver.capabilities["browserName"]} '
          f'{driver.capabilities.get("browserVersion")}')

    driver.quit()


def close_vs_quit():
    """
    driver.close() closes only the current window/tab.
    driver.quit() ends the whole session and shuts down the driver process.
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    driver.get('https://www.example.com/')

    original = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.close()                              # closes only the new tab
    driver.switch_to.window(original)
    print(f'Session still alive: {driver.session_id}')

    driver.quit()                               # ends the session entirely


if __name__ == '__main__':
    remote_session_metadata()
    close_vs_quit()
