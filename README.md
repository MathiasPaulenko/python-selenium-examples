# python-selenium-examples

Repository with comprehensive examples of [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) in Python, covering Selenium 4 features across drivers, browsers, elements, waits, interactions, actions, and BiDi/CDP.

## Requirements

- Python 3.10+
- `selenium>=4,<5`
- `webdriver-manager>=4,<5`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

| Directory | Description |
|-----------|-------------|
| `selenium_v4/browsers/` | Browser-specific configurations (Chrome, Firefox, Edge, Safari) |
| `selenium_v4/drivers/` | Driver management — local setup, remote/Grid, capabilities, proxy |
| `selenium_v4/elements/` | Web element topics — locators, finders, information, waits, file upload |
| `selenium_v4/interactions/` | Browser and element interactions — navigation, alerts, frames, cookies, windows |
| `selenium_v4/actions/` | Actions API — keyboard, mouse, and scroll wheel (ActionChains) |
| `selenium_v4/bidi/` | BiDirectional protocol — CDP commands, BiDi logging, network, DOM mutations |
| `selenium_v4/examples/` | Standalone general-purpose examples (reserved) |
| `resources/` | Static resources (e.g., `chromedriver.exe`) |
| `output/` | Generated outputs (screenshots, PDFs, logs) |

## Running Examples

Each Python file is self-contained and runnable directly:
```bash
python selenium_v4/interactions/navigation.py
python selenium_v4/actions/keyboard.py
python selenium_v4/bidi/logging.py
```

Files follow a consistent pattern: a private `_build_driver()` helper, modular single-purpose functions, and an `if __name__ == '__main__':` entry point.

## Documentation References

- [Selenium WebDriver Docs](https://www.selenium.dev/documentation/webdriver/)
- [Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/)
- [BiDirectional Protocol](https://www.selenium.dev/documentation/webdriver/bidi/)
- [Waits](https://www.selenium.dev/documentation/webdriver/waits/)
- [Web Elements](https://www.selenium.dev/documentation/webdriver/elements/)

