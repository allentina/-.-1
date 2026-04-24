import pytest

from shop.models import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_product_init():
    product = Product(
        name="Milk",
        description="2.5% fat",
        price=79.90,
        quantity=3,
    )

    assert product.name == "Milk"
    assert product.description == "2.5% fat"
    assert product.price == pytest.approx(79.90)
    assert product.quantity == 3


def test_category_init():
    p1 = Product(name="Tea", description="Black", price=199.0, quantity=5)
    p2 = Product(name="Coffee", description="Arabica", price=399.0, quantity=2)

    category = Category(
        name="Drinks",
        description="Hot drinks",
        products=[p1, p2],
    )

    assert category.name == "Drinks"
    assert category.description == "Hot drinks"
    assert category.products == [p1, p2]


def test_category_count():
    Category(name="C1", description="D1", products=[])
    Category(name="C2", description="D2", products=[])

    assert Category.category_count == 2


def test_product_count():
    p1 = Product(name="P1", description="D", price=10.0, quantity=1)
    p2 = Product(name="P2", description="D", price=20.0, quantity=1)
    p3 = Product(name="P3", description="D", price=30.0, quantity=1)

    Category(name="C1", description="D1", products=[p1, p2])
    Category(name="C2", description="D2", products=[p3])

    assert Category.product_count == 3


def test_products_must_be_product_instances():
    with pytest.raises(TypeError):
        Category(name="Bad", description="Bad", products=["not a product"])
