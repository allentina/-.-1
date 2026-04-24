from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Iterable


@dataclass(slots=True)
class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __post_init__(self) -> None:
        if not isinstance(self.price, (int, float)):
            raise TypeError("price must be int or float")
        if self.price < 0:
            raise ValueError("price must be >= 0")

        if not isinstance(self.quantity, int):
            raise TypeError("quantity must be int")
        if self.quantity < 0:
            raise ValueError("quantity must be >= 0")

        self.price = float(self.price)


class Category:
    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: Iterable[Product] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.products: list[Product] = list(products) if products is not None else []

        for product in self.products:
            if not isinstance(product, Product):
                raise TypeError("products must contain only Product instances")

        type(self).category_count += 1
        type(self).product_count += len(self.products)
