# Intro OOP Homework

Учебный проект "магазин" с базовыми доменными моделями и тестами.

Реализовано:

- `Product` с полями `name`, `description`, `price`, `quantity`.
- Классы-наследники `Product`: `Smartphone` и `LawnGrass`.
- `Category` с полями `name`, `description`, приватным списком товаров и методом `add_product()`.
- Счетчики `Category.category_count` и `Category.product_count`.
- Ограничение сложения: складывать можно только товары одного и того же конкретного класса (`type(self) is type(other)`), иначе выбрасывается `TypeError`.
- JSON-загрузчик `load_categories_from_json()` создает категории и продукты из файла JSON.

## Зависимости

- Python `>= 3.12`
- Для разработки: `pytest`, `pytest-cov`, `flake8` (см. `pyproject.toml` / `requirements-dev.txt`)

## Тесты и покрытие

```powershell
.\.venv\Scripts\python -m pytest
```

Артефакты покрытия:

- `coverage.xml`
- `coverage_report.txt`

