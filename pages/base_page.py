"""Shared base for all page objects: the page handle plus widgets that appear
on every logged-in screen (the burger menu)."""
from __future__ import annotations

from playwright.sync_api import Page

from config import settings


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.burger_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def goto(self, path: str = "/") -> None:
        self.page.goto(f"{settings.BASE_URL}{path}")

    def is_logged_in(self) -> bool:
        # The burger menu only exists on logged-in screens.
        return self.burger_button.is_visible()

    def logout(self) -> None:
        self.burger_button.click()
        self.logout_link.click()
