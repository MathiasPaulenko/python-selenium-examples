# Driver Management

Examples for instantiating and configuring WebDriver locally or remotely.

| Subdirectory | Description |
|-------------|-------------|
| `local/` | Local browser driver setup — capabilities, service, install, proxy, listeners, user agent |
| `remote/` | Remote / Selenium Grid — HTTP client, remote session, file detector |

## Common Patterns

- **webdriver-manager**: Automatic driver binary resolution
- **Service objects**: Port, log output, service args
- **Options objects**: ChromeOptions, FirefoxOptions, etc.
- **Capabilities**: W3C capabilities via `options.set_capability()`
- **Listeners**: EventFiringWebDriver with AbstractEventListener
