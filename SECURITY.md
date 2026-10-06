# Security Policy

## Supported Versions

This repository contains standalone example scripts and tracks the latest
Selenium 4 release line. Only the `main` branch is maintained.

| Version          | Supported          |
| ---------------- | ------------------ |
| `main`           | :white_check_mark: |

## Reporting a Vulnerability

The examples are teaching material and do not run as a deployed service, but
unsafe patterns can still teach bad practices (hardcoded credentials, insecure
downloads, disabled TLS verification, etc.). If you spot one:

- **Do not open a public issue** if the finding could be abused.
- Email **mathias.paulenko@outlook.com** with a description, the affected file
  and line, and steps to reproduce.

You can expect an acknowledgement within a few days. If the report is accepted,
a fix will land on `main` and the finding will be credited in the commit or
release notes unless you prefer to stay anonymous.

## Out of Scope

- Vulnerabilities in Selenium, webdriver-manager, browsers or drivers
  themselves — report those upstream.
- The third-party demo pages used by the examples (selenium.dev,
  the-internet.herokuapp.com, example.com).
