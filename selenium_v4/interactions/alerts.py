# -*- coding: utf-8 -*-
"""
JavaScript Alerts, Prompts and Confirmations examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/interactions/alerts/

WebDriver provides an API for working with the three types of native popup
messages offered by JavaScript. These popups are styled by the browser and
offer limited customisation.

Types:
    - Alert    — Shows a message with a single OK button.
    - Confirm  — Shows a message with OK and Cancel buttons.
    - Prompt   — Shows a message with a text input field plus OK and Cancel.

All three are accessed via driver.switch_to.alert after the popup appears.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager

ALERTS_PAGE = 'https://www.selenium.dev/selenium/web/alerts.html'


def _build_driver() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


# ---------------------------------------------------------------------------
# 1. Alert
# ---------------------------------------------------------------------------

def handle_alert_accept():
    """
    Accept (dismiss) a JavaScript alert by clicking OK.
    switch_to.alert gives access to the open alert popup.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    # Trigger the alert via JS or by clicking a button
    driver.find_element(By.ID, 'alert').click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    print(f'Alert text: {alert.text}')
    alert.accept()  # Click OK

    driver.quit()


def handle_alert_text():
    """
    Read the text of a JavaScript alert before accepting it.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    driver.execute_script("alert('This is a test alert');")

    wait = WebDriverWait(driver, 5)
    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()

    print(f'Alert message was: {text}')
    driver.quit()


# ---------------------------------------------------------------------------
# 2. Confirm
# ---------------------------------------------------------------------------

def handle_confirm_accept():
    """
    Accept a JavaScript confirmation dialog by clicking OK.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    driver.find_element(By.ID, 'confirm').click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    print(f'Confirm text: {alert.text}')
    alert.accept()  # Click OK

    driver.quit()


def handle_confirm_dismiss():
    """
    Dismiss a JavaScript confirmation dialog by clicking Cancel.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    driver.find_element(By.ID, 'confirm').click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    alert.dismiss()  # Click Cancel

    print('Confirm dismissed')
    driver.quit()


# ---------------------------------------------------------------------------
# 3. Prompt
# ---------------------------------------------------------------------------

def handle_prompt_send_text():
    """
    Interact with a JavaScript prompt by sending text and accepting.
    alert.send_keys() types into the prompt's text field.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    driver.find_element(By.ID, 'prompt').click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    print(f'Prompt text: {alert.text}')
    alert.send_keys('Selenium input')
    alert.accept()

    print('Prompt accepted with text input')
    driver.quit()


def handle_prompt_dismiss():
    """
    Dismiss a JavaScript prompt without entering any text.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    driver.find_element(By.ID, 'prompt').click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.alert_is_present())

    alert = driver.switch_to.alert
    alert.dismiss()

    print('Prompt dismissed (no input sent)')
    driver.quit()


# ---------------------------------------------------------------------------
# 4. Unexpected alert handling
# ---------------------------------------------------------------------------

def check_no_alert_present():
    """
    Verify no alert is open. NoAlertPresentException is raised when
    switch_to.alert is called with no active popup.
    """
    driver = _build_driver()
    driver.get(ALERTS_PAGE)

    try:
        driver.switch_to.alert
        print('An alert is open')
    except NoAlertPresentException:
        print('No alert present (expected)')
    finally:
        driver.quit()


if __name__ == '__main__':
    handle_alert_accept()
    handle_confirm_dismiss()
    handle_prompt_send_text()
