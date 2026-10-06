# Contributing

Thanks for your interest in improving these Selenium 4 examples. This document
explains how to contribute.

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. You will need a browser (Chrome, Firefox, Edge) installed locally. Safari
   examples require macOS. `drivers/remote/` examples require a running
   Selenium Grid.

## Project Conventions

When adding or modifying an example, follow the existing conventions:

- `# -*- coding: utf-8 -*-` header at the top of every file.
- One feature per function, named after the behavior it demonstrates
  (`send_keys_to_input`, `locate_by_id`, ...).
- Private `_build_driver()` helper for WebDriver creation in
  browser-driving modules.
- Docstrings explain *what the API does* and link to the official Selenium
  docs when relevant.
- Module-level constants in `UPPER_CASE` (URLs, paths, credentials for
  public demo pages).
- `if __name__ == '__main__':` block executes every self-contained function.
  Functions needing external resources (Grid, env vars, Cast devices) stay
  defined but commented out, with the reason noted.
- Paths are resolved from `__file__`, never from the current working directory.
- Generated artifacts go to `output/`; sample inputs go to `resources/`
  (both are gitignored).

## Before Submitting

- Verify the example actually runs: `python selenium_v4/<area>/<file>.py`.
- Compile-check everything: `python -m compileall selenium_v4`.
- If you change a file's scope, update its README row and the module docstring
  so documentation and code stay in sync.
- Keep PRs atomic: one topic per pull request.

## Reporting Bugs

Open an issue using the **Bug Report** template and include the Python/Selenium
versions, browser and driver versions, and the full traceback.

## Suggesting Examples

Open an issue with the **Feature Request** template describing the Selenium
feature you'd like covered and a link to the relevant official documentation.
