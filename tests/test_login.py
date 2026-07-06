"""Login scenarios against saucedemo.com.

Covers the happy path plus the classic negative cases: locked-out user,
wrong password, and missing-field validation.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import expect

from config import settings


@pytest.mark.happy
def test_standard_user_logs_in(login_page):
    login_page.login(settings.STANDARD_USER)

    expect(login_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(login_page.page.locator('[data-test="inventory-list"]')).to_be_visible()


@pytest.mark.negative
def test_locked_out_user_sees_error(login_page):
    login_page.login(settings.LOCKED_OUT_USER)

    expect(login_page.page).to_have_url(re.compile(r"saucedemo\.com/?$"))
    expect(login_page.error_banner).to_have_text(
        "Epic sadface: Sorry, this user has been locked out."
    )


@pytest.mark.negative
def test_wrong_password_sees_error(login_page):
    login_page.login(settings.STANDARD_USER, password="not-the-password")

    expect(login_page.error_banner).to_have_text(
        "Epic sadface: Username and password do not match any user in this service"
    )


@pytest.mark.negative
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        ("", settings.PASSWORD, "Epic sadface: Username is required"),
        (settings.STANDARD_USER, "", "Epic sadface: Password is required"),
    ],
    ids=["missing-username", "missing-password"],
)
def test_missing_field_validation(login_page, username, password, expected_error):
    login_page.login(username, password=password)

    expect(login_page.error_banner).to_have_text(expected_error)
