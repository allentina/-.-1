from shop.models import Category, Product


def main() -> None:
    product1 = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    category = Category(
        "Смартфоны",
        (
            "Смартфоны, как средство не только коммуникации, но и получение "
            "дополнительных функций для удобства жизни"
        ),
    )
    category.add_product(product1)
    category.add_product(product2)

    print(category.name)
    print(category.description)
    print(category.products, end="")
    print(Category.category_count)
    print(Category.product_count)


if __name__ == "__main__":
    main()
