"""Part 1: the SAME button, found four different ways.

The "Add to cart" button for Coffee Beans in the HTML is:

    <button class="btn-x7f2" data-testid="add-coffee">Add to cart</button>

Each locator below reads a different part of that tag.
"""
import pytest
from playwright.sync_api import Error, Page, expect


def test_by_test_id(shop: Page):
    # Reads the data-testid attribute. It exists ONLY for tests, so designers
    # and copywriters have no reason to change it. Most stable.
    shop.get_by_test_id("add-coffee").click()
    expect(shop.get_by_test_id("cart-count")).to_have_text("1")


def test_by_role_and_name(shop: Page):
    # Reads the ACCESSIBILITY TREE: role=button, name="Add to cart".
    # Both buttons have that name, so we narrow to the product article first.
    coffee = shop.get_by_role("article").filter(has_text="Coffee Beans")
    coffee.get_by_role("button", name="Add to cart").click()
    expect(shop.get_by_test_id("cart-count")).to_have_text("1")


def test_by_css_class(shop: Page):
    # Reads the class attribute, a styling detail. Works today, but there are
    # THREE .btn-x7f2 buttons (two "Add to cart" + "Place order"), and the
    # class breaks the day a designer renames it.
    shop.locator(".btn-x7f2").first.click()
    expect(shop.get_by_test_id("cart-count")).to_have_text("1")


def test_by_text(shop: Page):
    # Reads visible text. Readable, but breaks when the copy changes
    # ("Add to cart" -> "Add to bag") and matches both buttons.
    shop.get_by_text("Add to cart").first.click()
    expect(shop.get_by_test_id("cart-count")).to_have_text("1")


def test_strict_mode_refuses_ambiguous_locator(shop: Page):
    # Two buttons share the name, so Playwright refuses to guess which one
    # to click. This is a feature: it stops a test from clicking the wrong one.
    with pytest.raises(Error, match="strict mode violation"):
        shop.get_by_role("button", name="Add to cart").click(timeout=1000)
