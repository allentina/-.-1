import pytest

from shop.models import Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
