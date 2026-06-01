# BiDirectional Protocol (BiDi & CDP)

Reference: https://www.selenium.dev/documentation/webdriver/bidi/

WebDriver BiDi provides asynchronous, bidirectional communication with the browser over WebSockets. CDP (`execute_cdp_cmd`) is the temporary Chrome/Edge-specific alternative.

> **Note:** Most BiDi features require `options.enable_bidi = True`.

| File | Topics |
|------|--------|
| `cdp.py` | `execute_cdp_cmd` — set cookie, performance metrics, geolocation override, extra HTTP headers, block URLs, network throttling |
| `logging.py` | Real-time console message handlers (`add_console_message_handler`) and JavaScript exception handlers (`add_javascript_error_handler`) |
| `network.py` | Authentication handlers, request/response interception, remove/clear handlers |
| `script.py` | DOM mutation handlers — observe attribute changes in real time |
