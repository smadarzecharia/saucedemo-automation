"""Shared base for all page objects: the page handle plus widgets that appear
on every logged-in screen (the burger menu)."""
from __future__ import annotations

import logging

from playwright.sync_api import Page

from config import settings

log = logging.getLogger(__name__)


def product_slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (as used in data-test ids)."""
    return product_name.lower().replace(" ", "-")


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.burger_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')
        # Header widgets, present on every logged-in screen.
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')

    def goto(self, path: str = "/") -> None:
        url = f"{settings.BASE_URL}{path}"
        log.info("Navigating to %s", url)
        self.page.goto(url)

    def is_logged_in(self) -> bool:
        # The burger menu only exists on logged-in screens.
        return self.burger_button.is_visible()

    def logout(self) -> None:
        log.info("Logging out via burger menu")
        self.burger_button.click()
        self.logout_link.click()
