from pathlib import Path

import pytest

PAGE = (Path(__file__).parent / "pages" / "shop.html").resolve().as_uri()


@pytest.fixture
def shop(page):
    """Opens the demo shop straight from disk (no server needed)."""
    page.goto(PAGE)
    return page


# --- Sharding for CI -------------------------------------------------------
# GitHub Actions starts several machines (a "matrix"). Each one sets
# SHARD="1/2", "2/2", ... and runs only its slice of the tests.
# Locally SHARD is not set, so every test runs.
import os


def pytest_collection_modifyitems(config, items):
    shard = os.environ.get("SHARD")
    if not shard:
        return
    index, total = (int(n) for n in shard.split("/"))
    keep = [t for i, t in enumerate(items) if i % total == index - 1]
    skip = [t for t in items if t not in keep]
    items[:] = keep
    config.hook.pytest_deselected(items=skip)
