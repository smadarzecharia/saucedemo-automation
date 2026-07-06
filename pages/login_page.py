"""Page object for the saucedemo login screen.

All locators use saucedemo's stable `data-test` attributes.
"""
from __future__ import annotations

import logging

from playwright.sync_api import Page

from config import settings
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_banner = page.locator('[data-test="error"]')

    def load(self) -> "LoginPage":
        self.goto("/")
        return self

    def login(self, username: str, password: str = settings.PASSWORD) -> None:
        log.info("Logging in as %r", username)
        if username:
            self.username_input.fill(username)
        if password:
            self.password_input.fill(password)
        self.login_button.click()
