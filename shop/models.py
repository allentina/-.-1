from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Iterable


class BaseProduct(ABC):
    """Abstract base class for all products."""

    @abstractmethod
    def __repr__(self) -> str:  # pragma: no cover
        """Return a developer-friendly representation of the product."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:  # pragma: no cover
        """Return a user-friendly representation of the product."""
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: object) -> float:  # pragma: no cover
        """Sum stock value with another product of the same type."""
        raise NotImplementedError

    def __post_init__(self) -> None:
        if not isinstance(self.price, (int, float)):  # type: ignore[attr-defined]
            raise TypeError("price must be int or float")
        if self.price < 0:  # type: ignore[attr-defined]
            raise ValueError("price must be >= 0")

        if not isinstance(self.quantity, int):  # type: ignore[attr-defined]
            raise TypeError("quantity must be int")
        if self.quantity < 0:  # type: ignore[attr-defined]
            raise ValueError("quantity must be >= 0")

        # Normalize to float so downstream formatting is consistent.
        self.price = float(self.price)  # type: ignore[attr-defined]


class InitPrintMixin:
    """Mixin that prints creation info (via repr) when object is created."""

    def __post_init__(self) -> None:
        # Prefix the instance repr with creation marker.
        print(f"Created {self!r}")
        super().__post_init__()  # type: ignore[misc]


@dataclass(slots=True, repr=False)
class Product(InitPrintMixin, BaseProduct):
    name: str
    description: str
    price: float
    quantity: int

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the product."""
        cls_name = type(self).__name__
        fields = getattr(self, "__dataclass_fields__", {})
        parts = [f"{name}={getattr(self, name)!r}" for name in fields]
        return f"{cls_name}({', '.join(parts)})"

    def __str__(self) -> str:
        price_str = str(int(self.price)) if self.price.is_integer() else str(self.price)
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if not isinstance(other, BaseProduct):
            raise TypeError("Can only add another product")
        if type(self) is not type(other):
            raise TypeError("Can only add products of the same type")
        return (self.price * self.quantity) + (other.price * other.quantity)  # type: ignore[attr-defined]


@dataclass(slots=True, repr=False)
class Smartphone(Product):
    efficiency: float
    model: str
    memory: int
    color: str


@dataclass(slots=True, repr=False)
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
