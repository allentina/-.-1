import pytest

from shop.models import BaseProduct, Category, LawnGrass, Product, Smartphone


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


def test_product_str_formats_output():
    p = Product(name="P1", description="D", price=10, quantity=2)
    assert str(p) == "P1, 10 руб. Остаток: 2 шт."


def test_product_str_keeps_decimal_price():
    p = Product(name="P1", description="D", price=10.5, quantity=2)
    assert str(p) == "P1, 10.5 руб. Остаток: 2 шт."


def test_category_str_uses_total_quantity():
    p1 = Product(name="P1", description="D", price=10.0, quantity=2)
    p2 = Product(name="P2", description="D", price=20.0, quantity=5)
    c = Category(name="C1", description="D1", products=[p1, p2])
    assert str(c) == "C1, количество продуктов: 7 шт."


def test_product_add_returns_total_stock_value():
    p1 = Product(name="P1", description="D", price=10.0, quantity=2)
    p2 = Product(name="P2", description="D", price=20.0, quantity=5)
    assert (p1 + p2) == pytest.approx(120.0)


def test_product_add_with_non_product_is_type_error():
    p1 = Product(name="P1", description="D", price=10.0, quantity=2)
    with pytest.raises(TypeError):
        _ = p1 + 1


def test_smartphone_init():
    phone = Smartphone(
        name="Phone",
        description="Desc",
        price=100.0,
        quantity=2,
        efficiency=9.5,
        model="X",
        memory=256,
        color="black",
    )
    assert phone.efficiency == pytest.approx(9.5)
    assert phone.model == "X"
    assert phone.memory == 256
    assert phone.color == "black"


def test_lawngrass_init():
    grass = LawnGrass(
        name="Grass",
        description="Desc",
        price=10.0,
        quantity=5,
        country="RU",
        germination_period=7,
        color="green",
    )
    assert grass.country == "RU"
    assert grass.germination_period == 7
    assert grass.color == "green"


def test_product_add_requires_same_type():
    p = Product(name="P1", description="D", price=10.0, quantity=2)
    phone = Smartphone(
        name="Phone",
        description="Desc",
        price=100.0,
        quantity=1,
        efficiency=9.5,
        model="X",
        memory=256,
        color="black",
    )
    with pytest.raises(TypeError):
        _ = p + phone


def test_category_add_product_accepts_only_products():
    c = Category(name="C1", description="D1", products=[])
    c.add_product(Product(name="P1", description="D", price=10.0, quantity=1))
    assert len(c.products) == 1
    assert Category.product_count == 1

    with pytest.raises(TypeError):
        c.add_product("not a product")


def test_baseproduct_defines_abstract_protocol():
    assert {"__repr__", "__str__", "__add__"} <= set(BaseProduct.__abstractmethods__)


def test_init_print_mixin_prints_creation_info(capsys):
    _ = Product(name="P1", description="D", price=10.0, quantity=2)
    out = capsys.readouterr().out.strip()
    assert out.startswith("Created Product(")


def test_repr_from_mixin_is_used_for_subclasses():
    phone = Smartphone(
        name="Phone",
        description="Desc",
        price=100.0,
        quantity=1,
        efficiency=9.5,
        model="X",
        memory=256,
        color="black",
    )
    assert repr(phone).startswith("Created Smartphone(")
