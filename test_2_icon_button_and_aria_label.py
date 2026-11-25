"""Part 2: an icon-only button, where aria-label IS the name.

After adding Coffee Beans, JS creates:

    <button class="icon-btn" aria-label="Remove Coffee Beans"
            data-testid="remove-item-btn">🗑</button>

On screen you see a trash-can emoji. In the accessibility tree you see:
    - button "Remove Coffee Beans"
"""
from playwright.sync_api import Page, expect


def add_coffee(shop: Page):
    shop.get_by_test_id("add-coffee").click()


def test_role_uses_aria_label_not_the_emoji(shop: Page):
    add_coffee(shop)
    # aria-label overrides the visible content as the accessible name.
    remove = shop.get_by_role("button", name="Remove Coffee Beans")
    remove.click()
    expect(remove).to_have_count(0)
    expect(shop.get_by_text("Your cart is empty.")).to_be_visible()


def test_get_by_text_cannot_see_aria_label(shop: Page):
    add_coffee(shop)
    expect(shop.get_by_test_id("remove-item-btn")).to_be_visible()
    # aria-label is an attribute, not text content, so get_by_text misses it.
    expect(shop.get_by_text("Remove Coffee Beans")).to_have_count(0)
    # get_by_label DOES read aria-label (as well as <label for=...>).
    expect(shop.get_by_label("Remove Coffee Beans")).to_have_count(1)


def test_icon_by_test_id(shop: Page):
    add_coffee(shop)
    shop.get_by_test_id("remove-item-btn").click()
    expect(shop.get_by_test_id("remove-item-btn")).to_have_count(0)


def test_cart_badge_name_comes_from_aria_label(shop: Page):
    add_coffee(shop)
    # Visible text is "1", but the accessible name is "Cart, 1 item".
    expect(shop.get_by_role("status", name="Cart, 1 item")).to_have_text("1")
