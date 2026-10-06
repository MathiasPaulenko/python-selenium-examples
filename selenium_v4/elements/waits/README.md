# Waits

Reference: https://www.selenium.dev/documentation/webdriver/waits/

| File | Topics |
|------|--------|
| `implicit_waits.py` | `driver.implicitly_wait()` — global timeout for `find_element`, set via `timeouts` capability or driver method, reset to 0 |
| `explicit_waits.py` | `WebDriverWait` + `expected_conditions` — lambda conditions, `presence_of_element_located`, `element_to_be_clickable`, `text_to_be_present_in_element`, `TimeoutException` |
| `fluent_waits.py` | Custom `poll_frequency`, `ignored_exceptions` (e.g. `NoSuchElementException`), timeout message, side-effect polling |
