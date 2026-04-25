import pytest

from shop.models import Category, Product


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
    assert category._Category__products == [p1, p2]
    assert Category.product_count == 2
    assert (
        category.products
        == "Tea, 199 руб. Остаток: 5 шт.\nCoffee, 399 руб. Остаток: 2 шт.\n"
    )


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


def test_add_product_increments_product_count():
    category = Category(name="C1", description="D1", products=[])
    product = Product(name="P1", description="D", price=10.0, quantity=1)

    result = category.add_product(product)

    assert result is None
    assert Category.product_count == 1
    assert category._Category__products == [product]


def test_new_product_classmethod():
    product = Product.new_product(
        {
            "name": "P1",
            "description": "D1",
            "price": 99.9,
            "quantity": 7,
        }
    )

    assert isinstance(product, Product)
    assert product.name == "P1"
    assert product.description == "D1"
    assert product.price == pytest.approx(99.9)
    assert product.quantity == 7


def test_price_setter_rejects_non_number():
    with pytest.raises(TypeError, match="price must be int or float"):
        Product(name="P1", description="D1", price="oops", quantity=1)  # type: ignore[arg-type]


def test_products_property_formats_float_price():
    product = Product(name="Tea", description="Black", price=199.5, quantity=5)
    category = Category(name="Drinks", description="Hot drinks", products=[product])

    assert "199.5" in category.products


def test_price_setter_rejects_non_positive(capsys):
    product = Product(name="P1", description="D1", price=100.0, quantity=1)

    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == pytest.approx(100.0)
    product.price = -10
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == pytest.approx(100.0)
