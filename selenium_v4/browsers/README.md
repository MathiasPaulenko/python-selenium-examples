# Browser-Specific Configurations

Per-browser setup for Chrome, Firefox, Edge, and Safari.

Each browser folder follows a uniform layout:

| File | Purpose |
|------|---------|
| `options.py` | BrowserOptions — arguments, capabilities, experimental prefs, proxy, mobile emulation |
| `service.py` | Service configuration — driver path, port, log output, service args |
| `specials.py` | Advanced features — headless, incognito, network throttling, downloads, permissions, CDP features, print to PDF |

## Folders

- `chrome/` — ChromeOptions, ChromeService, Chrome-specific CDP features
- `firefox/` — FirefoxOptions, FirefoxService, Gecko-specific features (addons, profiles)
- `edge/` — EdgeOptions, EdgeService, IE compatibility mode, WebView2
- `safari/` — SafariOptions, SafariService, Safari Technology Preview (macOS-only)
