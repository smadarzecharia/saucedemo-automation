"""Cart-page scenarios: removing products from the cart."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.happy
def test_removed_item_disappears_from_cart(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)

    cart = inventory_page.open_cart()
    expect(cart.cart_items).to_have_count(2)

    cart.remove(BACKPACK)

    expect(cart.cart_items).to_have_count(1)
    expect(cart.item_names).to_have_text([BIKE_LIGHT])
    expect(cart.cart_badge).to_have_text("1")


@pytest.mark.negative
def test_removing_last_item_leaves_empty_cart(inventory_page):
    inventory_page.add_to_cart(BACKPACK)

    cart = inventory_page.open_cart()
    cart.remove(BACKPACK)

    expect(cart.cart_items).to_have_count(0)
    # The badge disappears entirely when the cart is empty.
    expect(cart.cart_badge).not_to_be_visible()
