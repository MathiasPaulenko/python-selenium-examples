# -*- coding: utf-8 -*-
"""
WebDriver BiDi Script Features examples for Selenium 4.

Reference:
https://www.selenium.dev/documentation/webdriver/bidi/script/

Script features provide real-time observation of DOM mutations and JavaScript
execution events via the WebDriver BiDi protocol.

Requires BiDi to be enabled: options.enable_bidi = True

Topics covered:
    - DOM Mutation Handlers — observe when DOM attributes or nodes change
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

DYNAMIC_PAGE = 'https://www.selenium.dev/selenium/web/dynamic.html'
MUTATION_PAGE = 'https://www.selenium.dev/selenium/web/bidi/mutation_observer.html'


def _build_bidi_driver() -> webdriver.Chrome:
    """Build a Chrome driver with WebDriver BiDi enabled."""
    options = webdriver.ChromeOptions()
    options.enable_bidi = True
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ---------------------------------------------------------------------------
# 1. DOM Mutation Handlers
# ---------------------------------------------------------------------------

def add_dom_mutation_handler():
    """
    driver.script.add_dom_mutation_handler(callback) registers a callback
    that fires whenever a DOM attribute changes on any element in the page.

    The callback receives a DomMutationEvent object with:
        - element   : the WebElement whose attribute changed
        - attribute_name  : name of the changed attribute
        - current_value   : new value of the attribute
        - old_value       : previous value of the attribute

    Use cases:
        - Observe dynamic CSS class changes (e.g. active, hidden, selected)
        - Track attribute-driven state transitions without polling
        - Debug unexpected DOM changes during test execution
    """
    driver = _build_bidi_driver()
    driver.get(DYNAMIC_PAGE)

    mutations = []
    driver.script.add_dom_mutation_handler(mutations.append)

    # Trigger a DOM change — clicking 'reveal' shows a hidden element
    driver.find_element(By.ID, 'reveal').click()

    WebDriverWait(driver, 5).until(lambda _: mutations)

    for mutation in mutations:
        print(
            f'Element: {mutation.element.tag_name}, '
            f'Attribute: {mutation.attribute_name}, '
            f'Old: {mutation.old_value!r} → New: {mutation.current_value!r}'
        )

    driver.quit()


def remove_dom_mutation_handler():
    """
    add_dom_mutation_handler() returns a handler id.
    Pass it to remove_dom_mutation_handler(id) to stop observing mutations.
    """
    driver = _build_bidi_driver()
    driver.get(DYNAMIC_PAGE)

    mutations = []
    handler_id = driver.script.add_dom_mutation_handler(mutations.append)

    driver.script.remove_dom_mutation_handler(handler_id)

    driver.find_element(By.ID, 'reveal').click()

    print(f'Mutations after handler removed: {len(mutations)}')  # 0

    driver.quit()


def track_multiple_mutations():
    """
    Multiple DOM mutation handlers can be registered simultaneously.
    Each handler receives its own copy of every mutation event.
    """
    driver = _build_bidi_driver()
    driver.get(DYNAMIC_PAGE)

    attribute_changes = []
    all_events = []

    driver.script.add_dom_mutation_handler(
        lambda e: attribute_changes.append(e.attribute_name)
    )
    driver.script.add_dom_mutation_handler(all_events.append)

    driver.find_element(By.ID, 'reveal').click()

    WebDriverWait(driver, 5).until(lambda _: attribute_changes)

    print(f'Attribute names changed: {attribute_changes}')
    print(f'Total mutation events: {len(all_events)}')

    driver.quit()


if __name__ == '__main__':
    add_dom_mutation_handler()
    remove_dom_mutation_handler()
