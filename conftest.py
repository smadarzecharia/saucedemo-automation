"""Project fixtures. The `page` fixture itself comes from pytest-playwright."""
from __future__ import annotations

import pytest

from pages.base_page import BasePage
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page) -> LoginPage:
    """A LoginPage already navigated to the login screen."""
    return LoginPage(page).load()


@pytest.fixture(autouse=True)
def logout_after_test(page):
    """Teardown: log out after every test, pass or fail, if a session is open.

    Cleanup must never mask the real test result, so failures here are swallowed
    (e.g. the page was already closed by a crashed test).
    """
    yield
    try:
        base = BasePage(page)
        if base.is_logged_in():
            base.logout()
    except Exception:
        pass
