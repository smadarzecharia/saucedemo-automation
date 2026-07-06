"""Project fixtures. The `page` fixture itself comes from pytest-playwright."""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import pytest

from config import settings
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

log = logging.getLogger(__name__)

FAILURES_DIR = Path(__file__).parent / "reports" / "failures"


@pytest.fixture
def login_page(page) -> LoginPage:
    """A LoginPage already navigated to the login screen."""
    return LoginPage(page).load()


@pytest.fixture
def inventory_page(login_page) -> InventoryPage:
    """An InventoryPage with the standard user already logged in."""
    login_page.login(settings.STANDARD_USER)
    return InventoryPage(login_page.page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose each test's result on its node, so fixtures can ask
    "did this test fail?" during teardown."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _write_failure_log(folder: Path, rep) -> None:
    """A failure log a human can read top-down: reason first, then the steps
    the test took, then the full traceback for whoever needs it."""
    reprcrash = getattr(rep.longrepr, "reprcrash", None)
    reason = reprcrash.message if reprcrash else "(no assertion message captured)"

    sections = [
        f"TEST:   {rep.nodeid}",
        f"WHEN:   {datetime.now():%Y-%m-%d %H:%M:%S}",
        "RESULT: FAILED",
        "",
        "REASON",
        "------",
        reason,
        "",
        "STEPS THE TEST TOOK",
        "-------------------",
        rep.caplog or "(no log lines captured)",
        "",
        "FULL TRACEBACK",
        "--------------",
        rep.longreprtext,
        "",
    ]
    (folder / "test.log").write_text("\n".join(sections))


@pytest.fixture(autouse=True)
def logout_after_test(page, request):
    """Teardown for every test, pass or fail.

    On failure, capture the evidence FIRST — a screenshot of the failing state
    and a readable failure log — and only then log out. Cleanup must never
    mask the real test result, so logout failures are swallowed.
    """
    yield

    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = FAILURES_DIR / f"{request.node.name}_{stamp}"
        folder.mkdir(parents=True, exist_ok=True)

        _write_failure_log(folder, rep)
        try:
            page.screenshot(path=str(folder / "failure.png"), full_page=True)
        except Exception:
            log.warning("Could not capture failure screenshot for %s", request.node.name)

        log.info("Test failed — evidence folder: %s", folder)

    try:
        base = BasePage(page)
        if base.is_logged_in():
            base.logout()
    except Exception:
        pass
