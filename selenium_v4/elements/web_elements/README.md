# Web Elements — Locators, Finders, Information, File Upload

Reference: https://www.selenium.dev/documentation/webdriver/elements/

| File | Topics |
|------|--------|
| `locators.py` | 8 traditional locators (`By.ID`, `By.CLASS_NAME`, `By.CSS_SELECTOR`, `By.XPATH`, etc.) + Selenium 4 Relative Locators (`above`, `below`, `to_left_of`, `to_right_of`, `near`, chained combinations) |
| `finders.py` | `find_element` (first match, DOM scope, optimized locator) and `find_elements` (all matches, collection iteration, scoped search from an element, `active_element`) |
| `information.py` | Element state and properties — `is_displayed()`, `is_enabled()`, `is_selected()`, `tag_name`, `rect`, `value_of_css_property()`, `text`, `get_attribute()`, `get_property()`, `get_dom_attribute()` |
| `file_upload.py` | Upload via `send_keys()` on `<input type="file">`, basic upload, verification, multiple files, headless mode, remote upload with `LocalFileDetector` |
