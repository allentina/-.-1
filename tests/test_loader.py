import json

import pytest

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
    assert len(category._Category__products) == 2
    assert all(isinstance(p, Product) for p in category._Category__products)
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_load_categories_from_json_invalid_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON file:"):
        load_categories_from_json(path)

    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_categories_from_json_top_level_must_be_list(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(json.dumps({"name": "C1"}), encoding="utf-8")

    with pytest.raises(ValueError, match="Top-level JSON must be a list of categories"):
        load_categories_from_json(path)


def test_load_categories_from_json_each_category_must_be_object(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(json.dumps(["not an object"]), encoding="utf-8")

    with pytest.raises(ValueError, match="Each category must be a JSON object"):
        load_categories_from_json(path)


def test_load_categories_from_json_products_can_be_null(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(
        json.dumps(
            [
                {
                    "name": "C1",
                    "description": "D1",
                    "products": None,
                }
            ]
        ),
        encoding="utf-8",
    )

    categories = load_categories_from_json(path)

    assert len(categories) == 1
    assert categories[0]._Category__products == []
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_load_categories_from_json_products_must_be_list(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(
        json.dumps(
            [
                {
                    "name": "C1",
                    "description": "D1",
                    "products": {},
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Category 'products' must be a list"):
        load_categories_from_json(path)


def test_load_categories_from_json_each_product_must_be_object(tmp_path):
    path = tmp_path / "data.json"
    path.write_text(
        json.dumps(
            [
                {
                    "name": "C1",
                    "description": "D1",
                    "products": ["not an object"],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Each product must be a JSON object"):
        load_categories_from_json(path)


def test_load_products_json_file():
    categories = load_categories_from_json("products.json")

    assert len(categories) == 2
    assert Category.category_count == 2
    assert Category.product_count == 4
