"""Page object for the cart screen."""
from __future__ import annotations

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage, product_slug

log = logging.getLogger(__name__)


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')

    def remove(self, product_name: str) -> None:
        log.info("Removing %r from cart", product_name)
        self.page.locator(f'[data-test="remove-{product_slug(product_name)}"]').click()
