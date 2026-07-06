"""Page object for the inventory (product list) screen."""
from __future__ import annotations

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage, product_slug
from pages.cart_page import CartPage

log = logging.getLogger(__name__)


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_list = page.locator('[data-test="inventory-list"]')
        self.product_images = page.locator('img[data-test$="-img"]')

    def add_to_cart(self, product_name: str) -> None:
        log.info("Adding %r to cart", product_name)
        self.page.locator(f'[data-test="add-to-cart-{product_slug(product_name)}"]').click()

    def remove_from_cart(self, product_name: str) -> None:
        log.info("Removing %r from cart (inventory page)", product_name)
        self.page.locator(f'[data-test="remove-{product_slug(product_name)}"]').click()

    def open_cart(self) -> CartPage:
        log.info("Opening the cart")
        self.cart_link.click()
        return CartPage(self.page)

    def product_image_sources(self) -> list[str]:
        srcs = [img.get_attribute("src") for img in self.product_images.all()]
        log.info("Product image sources: %s", srcs)
        return srcs
