"""Part 4: a form, and JS that updates the page after a delay.

Adding to the cart waits 500 ms (fake network call). expect() retries until
the page catches up, so there is no time.sleep() anywhere.
"""
from playwright.sync_api import Page, expect


def test_checkout_happy_path(shop: Page):
    shop.get_by_test_id("add-mug").click()

    # Auto-wait: the form is display:none for 500 ms, then JS shows it.
    expect(shop.get_by_role("heading", name="Checkout")).to_be_visible()

    # get_by_label reads <label for="name">Full name</label>.
    shop.get_by_label("Full name").fill("Ada Lovelace")
    # get_by_placeholder reads the placeholder attribute (weaker than a label).
    shop.get_by_placeholder("you@example.com").fill("ada@example.com")
    shop.get_by_role("button", name="Place order").click()

    expect(shop.get_by_text("Thanks! Your order is placed.")).to_be_visible()


def test_validation_error_is_announced_as_alert(shop: Page):
    shop.get_by_test_id("add-mug").click()
    shop.get_by_label("Full name").fill("Ada")
    shop.get_by_label("Email").fill("not-an-email")
    shop.get_by_role("button", name="Place order").click()

    # role="alert" makes screen readers read the error out loud,
    # and gives tests a meaningful way to find it.
    expect(shop.get_by_role("alert")).to_have_text(
        "Please enter your name and a valid email."
    )
