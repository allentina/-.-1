import json

from shop.loader import load_categories_from_json
from shop.models import Category, Product


def test_load_categories_from_json(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(
        json.dumps(
            [
                {
                    "name": "C1",
                    "description": "D1",
                    "products": [
                        {
                            "name": "P1",
                            "description": "PD1",
                            "price": 10.5,
                            "quantity": 2,
                        },
                        {
                            "name": "P2",
                            "description": "PD2",
                            "price": 20,
                            "quantity": 1,
                        },
                    ],
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    categories = load_categories_from_json(path)

    assert len(categories) == 1
    category = categories[0]
    assert isinstance(category, Category)
    assert category.name == "C1"
    assert category.description == "D1"
    assert len(category.products) == 2
    assert all(isinstance(p, Product) for p in category.products)
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_load_products_json_file():
    categories = load_categories_from_json("products.json")

    assert len(categories) == 2
    assert Category.category_count == 2
    assert Category.product_count == 4
