"""Catches a bug saucedemo plants on purpose: `problem_user` sees the same
broken 404 image for every product.

This test FAILS by design — it exists to exercise the failure-forensics
pipeline: informative assertion message, captured logs, a screenshot of the
failing state (reports/failures/), and a Playwright trace (test-results/).
"""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from config import settings
from pages.inventory_page import InventoryPage


@pytest.mark.bug
def test_problem_user_sees_real_product_images(login_page):
    login_page.login(settings.PROBLEM_USER)

    inventory = InventoryPage(login_page.page)
    expect(inventory.inventory_list).to_be_visible()

    sources = inventory.product_image_sources()
    unique_sources = set(sources)
    assert len(unique_sources) == len(sources), (
        f"Every product should have its own image, but the {len(sources)} products "
        f"share only {len(unique_sources)} distinct image(s): {sorted(unique_sources)}"
    )
