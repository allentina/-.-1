from shop.models import Category, Product


def main() -> None:
    products = [
        Product(
            name="iPhone 15",
            description="Smartphone",
            price=129_990.00,
            quantity=10,
        ),
        Product(
            name="AirPods Pro",
            description="Headphones",
            price=26_990.00,
            quantity=5,
        ),
    ]

    category = Category(
        name="Electronics",
        description="Devices and accessories",
        products=products,
    )

    print(category.name)
    print(f"Products: {len(category.products)}")
    print(f"Category count: {Category.category_count}")
    print(f"Product count: {Category.product_count}")


if __name__ == "__main__":
    main()
