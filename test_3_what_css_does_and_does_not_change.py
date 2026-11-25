"""Part 3: how CSS affects what Playwright sees.

Rule of thumb: CSS colours, fonts, layout and class names are invisible to
get_by_role / get_by_text. Only "is it hidden?" matters.
"""
from playwright.sync_api import Page, expect


def test_display_none_removes_element_from_role_queries(shop: Page):
    # The form is in the HTML but has class="hidden" (display:none) until the
    # cart has an item. It is in the DOM, but NOT in the accessibility tree.
    expect(shop.locator("#checkout-form")).to_have_count(1)        # in the DOM
    expect(shop.locator("#checkout-form")).to_be_hidden()          # not shown
    expect(shop.get_by_role("button", name="Place order")).to_have_count(0)

    shop.get_by_test_id("add-coffee").click()
    # JS removes the class; now the button appears in the tree.
    expect(shop.get_by_role("button", name="Place order")).to_be_visible()


def test_visually_hidden_text_is_still_in_the_tree(shop: Page):
    # ".sr-only" squeezes "Price: " into a 1px box, so sighted users don't
    # see it, but it stays in the accessibility tree for screen readers.
    expect(shop.get_by_text("Price:").first).to_be_attached()
    coffee = shop.get_by_role("article").filter(has_text="Coffee Beans")
    expect(coffee).to_contain_text("Price: $12.00")


def test_css_styles_are_checked_with_to_have_css(shop: Page):
    # If you DO care about a style, assert it directly. Don't locate by it.
    add = shop.get_by_test_id("add-coffee")
    expect(add).to_have_css("background-color", "rgb(37, 99, 235)")   # #2563eb
    expect(add).to_have_class("btn-x7f2")


def test_whole_section_matches_an_aria_snapshot(shop: Page):
    # This is literally what Playwright "sees" for the Coffee Beans card:
    # roles, names and text. No classes, no colours, no data-testid.
    expect(shop.get_by_test_id("product-coffee")).to_match_aria_snapshot("""
        - article:
          - heading "Coffee Beans" [level=3]
          - text: "Price: $12.00"
          - button "Add to cart"
    """)
