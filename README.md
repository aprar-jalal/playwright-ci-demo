# Locator demo: how Playwright sees HTML, CSS and JS

A small shop page (`pages/shop.html`) plus tests that find the same elements in different ways. The goal is to show the difference between **what you see** (HTML styled by CSS) and **what Playwright's role locators see** (the accessibility tree).

## Setup and run

Same setup as `paradigm-shift-examples`:

```bash
cd locator-demo
pip install pytest-playwright
playwright install chromium

pytest -v                          # 15 tests, all pass
pytest --headed --slowmo 500       # watch it in a real browser
python show_accessibility_tree.py  # print what Playwright "sees"
```

Open `pages/shop.html` in your browser too, and read its comments next to the tests.

## The page in one picture

| Element on screen | HTML | In the accessibility tree |
| --- | --- | --- |
| Blue "Add to cart" button | `<button class="btn-x7f2" data-testid="add-coffee">Add to cart</button>` | `button "Add to cart"` |
| Orange badge showing `1` | `<span role="status" aria-label="Cart, 1 item" data-testid="cart-count">1</span>` | `status "Cart, 1 item": "1"` |
| Trash-can icon 🗑 | `<button aria-label="Remove Coffee Beans" data-testid="remove-item-btn">🗑</button>` | `button "Remove Coffee Beans"` |
| Name input | `<label for="name">Full name</label><input id="name">` | `textbox "Full name"` |
| Checkout form while cart is empty | `<form class="hidden">` (display:none) | **missing** |
| Nothing visible ("Price: " is 1px, clipped) | `<span class="sr-only">Price: </span>` | `text: "Price: $12.00"` |

Notice what disappears on the right: `class`, colours, `data-testid`, the emoji (replaced by the aria-label). Notice what appears: roles (`banner`, `region`, `article`, `alert`) that come from the tag names and `role=` attributes. The full before/after dump is in `accessibility_tree_output.txt`.

## Two views of one page

Think of the browser building two things from the same HTML:

1. **The render tree** (HTML + CSS): boxes, colours, positions. This is what your eyes see. `page.locator(".btn-x7f2")` and screenshots work at this level.
2. **The accessibility tree** (HTML + ARIA): a list of things with a *role* ("this is a button") and a *name* ("called Add to cart"). This is what a screen reader hears. `get_by_role`, `get_by_label` and `to_match_aria_snapshot` work at this level.

The accessible **name** comes from, in priority order: `aria-labelledby`, then `aria-label`, then a linked `<label>`, then the element's text. That's why the 🗑 button is named "Remove Coffee Beans" and the badge is named "Cart, 1 item" even though it shows "1".

CSS only touches the accessibility tree in one way: **hidden things leave it**. `display:none` and `visibility:hidden` remove an element; a visually-hidden `.sr-only` trick keeps it.

## What each test file shows

| File | Lesson |
| --- | --- |
| `test_1_four_ways_to_find_a_button.py` | The same button found by `get_by_test_id`, `get_by_role(name=)`, CSS class and text. Why two buttons with the same name trigger a **strict mode violation**, and how `.filter(has_text=...)` scopes to one product card |
| `test_2_icon_button_and_aria_label.py` | The icon-only button: `get_by_role` and `get_by_label` find it by aria-label, `get_by_text` can't (aria-label is an attribute, not text) |
| `test_3_what_css_does_and_does_not_change.py` | `display:none` hides the form from role queries even though it's in the DOM. `.sr-only` text stays findable. If you care about a style, assert it with `to_have_css`, don't locate by it. `to_match_aria_snapshot` checks a whole card the way Playwright sees it |
| `test_4_forms_and_javascript.py` | JS adds items after 500 ms; `expect()` auto-waits, no `sleep()`. `get_by_label` for inputs, `role="alert"` for the error message |

## Locator ranking for this page

1. `get_by_role("button", name="Remove Coffee Beans")`: tests what a user (or screen reader) actually experiences. If this breaks, real users are probably affected too.
2. `get_by_test_id("remove-item-btn")`: rock-solid, invisible to users, survives copy and design changes. Use it when there's no good accessible name.
3. `get_by_text("Add to cart")`: readable, but breaks when the copy changes.
4. `locator(".btn-x7f2")`: breaks when a designer renames a class. Avoid.

## Try it yourself

- Change `.hidden { display: none; }` to `.hidden { opacity: 0; }` in `shop.html` and rerun test 3. The form is now invisible to your eyes but still in the tree, so `to_have_count(0)` fails.
- Delete the `aria-label` line in the JS `render()` function. The 🗑 button's name becomes "🗑" and the role-based tests in test 2 fail, which is exactly the accessibility bug a screen reader user would hit.
- Rename `btn-x7f2` in the CSS and HTML. Only `test_by_css_class` fails.
