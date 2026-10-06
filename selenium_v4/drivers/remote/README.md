# Remote / Selenium Grid Examples

Reference: https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/

> These examples require a reachable Selenium Grid or standalone server
> (default: `http://127.0.0.1:4444/wd/hub`).

| File | Topics |
|------|--------|
| `http_client.py` | Custom HTTP transport — `RemoteConnection` timeouts, CA bundle, keep-alive, custom headers, `ClientConfig` availability check |
| `local_file_detector.py` | `LocalFileDetector` for transferring local files to the remote node during uploads |
| `remote.py` | Connecting to a remote Grid — `webdriver.Remote` with browser-specific `Options` (Chrome, Firefox, Edge) |
| `session.py` | Remote session management — `session_id`, negotiated capabilities, `close()` vs `quit()` |
