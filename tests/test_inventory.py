"""Inventory-page scenarios: adding products to the cart."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.happy
def test_added_items_are_counted_in_cart_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")


@pytest.mark.happy
def test_add_button_turns_into_remove(inventory_page):
    inventory_page.add_to_cart(BACKPACK)

    # The product's button flips to "Remove" once it's in the cart.
    expect(
        inventory_page.page.locator('[data-test="remove-sauce-labs-backpack"]')
    ).to_be_visible()
