# Intro OOP Homework

Implemented basic domain models:

- `Product` with fields `name`, `description`, `price`, `quantity`.
- `Category` with fields `name`, `description`, `products`.
- `Category.category_count` and `Category.product_count` are updated automatically on category initialization.
- JSON loader `load_categories_from_json()` creates objects from `products.json`.

Tests are written with `pytest` and coverage is generated to `coverage.xml`.
