from __future__ import annotations

from typing import ClassVar, Iterable


class Product:
    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.quantity = quantity

        # Use the setter validation for initial value too.
        self.__price: float = 0.0
        self.price = price

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("price must be int or float")

        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        self.__price = float(value)

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


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
        self.__products: list[Product] = []

        # Class-level counters should update automatically on object creation.
        # Keep a single global counter across all Category instances (incl. subclasses).
        Category.category_count += 1

        if products is not None:
            # Materialize once (in case an iterator is passed) and validate types.
            products_list = list(products)
            for product in products_list:
                if not isinstance(product, Product):
                    raise TypeError("product must be a Product instance")

            self.__products.extend(products_list)
            Category.product_count += len(products_list)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("product must be a Product instance")

        self.__products.append(product)
        # Total products across all categories should be stored on the base class.
        Category.product_count += 1

    @property
    def products(self) -> str:
        lines: list[str] = []
        for product in self.__products:
            price = product.price
            if float(price).is_integer():
                price_out: int | float = int(price)
            else:
                price_out = price
            lines.append(
                f"{product.name}, {price_out} руб. Остаток: {product.quantity} шт.\n"
            )
        return "".join(lines)
