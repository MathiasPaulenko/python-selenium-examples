# Interactions

Browser and element-level interactions using the classic WebDriver API.

Reference: https://www.selenium.dev/documentation/webdriver/interactions/

| File | Topics |
|------|--------|
| `browser.py` | Browser information — `driver.title`, `driver.current_url` |
| `navigation.py` | Navigation commands — `driver.get()`, `driver.back()`, `driver.forward()`, `driver.refresh()` |
| `alerts.py` | JavaScript alerts, confirmations, and prompts — `switch_to.alert`, `accept()`, `dismiss()`, `send_keys()`, `NoAlertPresentException` |
| `windows.py` | Window/tab management — `current_window_handle`, `window_handles`, `switch_to.window`, `switch_to.new_window`, `close()`, sizing/positioning, `maximize()`, `minimize()`, `fullscreen()`, screenshots (page & element), `execute_script`, `execute_async_script`, `print_page()` to PDF |
| `frames.py` | Frame/iframe switching — `switch_to.frame` (by element, name/id, index), `default_content()`, `parent_frame()` |
| `cookies.py` | Cookie management — `add_cookie()`, `get_cookie()`, `get_cookies()`, `delete_cookie()`, `delete_all_cookies()`, `SameSite` attribute (Strict, Lax) |
| `element_interactions.py` | Element actions — `click()`, `send_keys()` (including special keys like `Keys.BACK_SPACE`, `Keys.CONTROL`, `Keys.DELETE`), `clear()`, `Select` dropdown (`select_by_visible_text`, `select_by_value`, `select_by_index`, `options`) |
