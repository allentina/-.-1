from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Category, Product


def load_categories_from_json(path: str | Path) -> list[Category]:
    file_path = Path(path)
    raw = file_path.read_text(encoding="utf-8")

    try:
        data: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {file_path}") from exc

    if not isinstance(data, list):
        raise ValueError("Top-level JSON must be a list of categories")

    categories: list[Category] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each category must be a JSON object")

        products_data = item.get("products", [])
        if products_data is None:
            products_data = []
        if not isinstance(products_data, list):
            raise ValueError("Category 'products' must be a list")

        products: list[Product] = []
        for p in products_data:
            if not isinstance(p, dict):
                raise ValueError("Each product must be a JSON object")

            products.append(
                Product(
                    name=p["name"],
                    description=p["description"],
                    price=p["price"],
                    quantity=p["quantity"],
                )
            )

        categories.append(
            Category(
                name=item["name"],
                description=item["description"],
                products=products,
            )
        )

    return categories
