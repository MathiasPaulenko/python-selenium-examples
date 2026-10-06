# Local Driver Examples

Reference: https://www.selenium.dev/documentation/webdriver/drivers/

| File | Topics |
|------|--------|
| `capabilities.py` | W3C capabilities — timeouts, page load strategy, accept insecure certs, unhandled prompt behavior, strict file interactability |
| `command_executors.py` | Execute raw WebDriver commands via `driver.execute(Command.*)` — get URL, page source, browser log |
| `install.py` | Driver installation strategies — Selenium Manager, webdriver-manager, PATH env var, hard-coded path |
| `listeners.py` | `EventFiringWebDriver` — `AbstractEventListener` hooks for navigate, find, click and quit events |
| `proxy.py` | Manual proxy configuration via `Proxy` object and `proxy` capability (http/ssl proxy, no-proxy list) |
| `service.py` | Service configuration — port, log output, service args for Chrome, Firefox and Edge |
| `session.py` | Local session creation and teardown for Chrome, Firefox and Edge |
| `user_agent.py` | User-Agent override — Chrome/Edge argument, CDP override, device metrics, runtime JS, Firefox preference |
