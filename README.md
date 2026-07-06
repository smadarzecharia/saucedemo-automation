# saucedemo-automation — Playwright E2E practice against saucedemo.com

Interview-prep project: pytest + Playwright (Python, sync API) against
[Swag Labs](https://www.saucedemo.com), the demo shop most interview exercises use.

**Step 1 (current):** login scenarios — happy path, locked-out user, wrong
password, missing-field validation.

## Setup

```bash
cd saucedemo-automation
cp .env.example .env        # credentials & users live here (gitignored)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
```

## Running

```bash
.venv/bin/pytest                 # headless, all tests
.venv/bin/pytest --headed        # watch the browser
.venv/bin/pytest -m happy        # only happy-path tests
.venv/bin/pytest -m negative     # only error/validation tests
```

## Layout

```
config/      # base URL & credentials — env-var overridable (SAUCEDEMO_BASE_URL, ...)
pages/       # page objects (data-test locators only, no assertions)
tests/       # pytest scenarios, markers: happy / negative
conftest.py  # login_page fixture (LoginPage already loaded)
```

## Credentials cheat-sheet

Password for every user: `secret_sauce`

| Username | Behavior |
|---|---|
| `standard_user` | Everything works |
| `locked_out_user` | Login rejected with error |
| `problem_user` | Logs in, but UI is intentionally broken |
| `performance_glitch_user` | Slow page loads |
| `error_user` | Some actions silently fail |
| `visual_user` | Visual layout glitches |

## Next steps

Cart badge + price-sorting assertions → full checkout happy path → optional
restful-booker API suite.
