from pathlib import Path

import pytest

PAGE = (Path(__file__).parent / "pages" / "shop.html").resolve().as_uri()


@pytest.fixture
def shop(page):
    """Opens the demo shop straight from disk (no server needed)."""
    page.goto(PAGE)
    return page
