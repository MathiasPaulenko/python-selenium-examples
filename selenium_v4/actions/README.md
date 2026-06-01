# Actions API

Low-level virtualized device input actions via `ActionChains`.

Reference: https://www.selenium.dev/documentation/webdriver/actions_api/

| File | Topics |
|------|--------|
| `action_builder.py` | Pause between actions, `reset_actions()` (release all held keys/buttons) |
| `keyboard.py` | `key_down`, `key_up`, `send_keys` to active/designated element, copy & paste with `Keys.COMMAND`/`Keys.CONTROL` |
| `mouse.py` | `click_and_hold`, `click`, `context_click`, `double_click`, `move_to_element`, `move_by_offset` (3 variants), `drag_and_drop`, `drag_and_drop_by_offset` |
| `wheel.py` | `scroll_to_element`, `scroll_by_amount`, `scroll_from_origin` (from element, with offset, from viewport) |
