"""Prints the page twice: as Playwright's accessibility tree, before and
after adding an item. Run it with:  python show_accessibility_tree.py

Compare the output with pages/shop.html: every class, colour and
data-testid is gone. What's left is roles, names and text.
"""
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

PAGE = (Path(__file__).parent / "pages" / "shop.html").resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(PAGE)

    print("=== BEFORE: empty cart ===")
    print(page.locator("body").aria_snapshot())

    page.get_by_test_id("add-coffee").click()
    expect(page.get_by_test_id("cart-count")).to_have_text("1")

    print("\n=== AFTER: one item in the cart ===")
    print(page.locator("body").aria_snapshot())
    browser.close()
