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

    def __str__(self) -> str:
        price_str = str(int(self.price)) if self.price.is_integer() else str(self.price)
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if not isinstance(other, Product):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError("Can only add products of the same type")
        return (self.price * self.quantity) + (other.price * other.quantity)


@dataclass(slots=True)
class Smartphone(Product):
    efficiency: float
    model: str
    memory: int
    color: str


@dataclass(slots=True)
class LawnGrass(Product):
    country: str
    germination_period: int
    color: str


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
        self.__products: list[Product] = list(products) if products is not None else []

        for product in self.__products:
            if not isinstance(product, Product):
                raise TypeError("products must contain only Product instances")

        type(self).category_count += 1
        type(self).product_count += len(self.__products)

    @property
    def products(self) -> list[Product]:
        return self.__products

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Can only add Product or its subclasses to a category")
        self.__products.append(product)
        type(self).product_count += 1

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class CategoryProductsIterator:
    def __init__(self, category: Category) -> None:
        self._category = category
        self._index = 0

    def __iter__(self) -> CategoryProductsIterator:
        return self

    def __next__(self) -> Product:
        if self._index >= len(self._category.products):
            raise StopIteration
        item = self._category.products[self._index]
        self._index += 1
        return item
