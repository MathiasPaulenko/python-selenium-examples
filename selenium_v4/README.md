# selenium_v4

Top-level directory for all Selenium 4 example modules.

Each subdirectory mirrors a major section of the official Selenium documentation:

| Subdirectory | Official Docs Section |
|-------------|----------------------|
| `browsers/` | Browser-specific options, service, and special capabilities |
| `drivers/` | Driver instantiation — local and remote/Grid |
| `elements/` | Web element locators, finders, information, waits |
| `interactions/` | Browser interactions — navigation, alerts, frames, cookies, windows |
| `actions/` | [Actions API](https://www.selenium.dev/documentation/webdriver/actions_api/) — keyboard, mouse, wheel |
| `bidi/` | [BiDirectional protocol](https://www.selenium.dev/documentation/webdriver/bidi/) — CDP and WebDriver BiDi |
| `examples/` | General-purpose standalone examples (reserved for future use) |

## Code Conventions

- `# -*- coding: utf-8 -*-` at the top of every file
- Extensive docstrings with links to official documentation
- Private `_build_driver()` helper for WebDriver initialization
- `if __name__ == '__main__':` block for direct execution
- Constants in `UPPER_CASE` at module level
