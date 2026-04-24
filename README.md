# Intro OOP Homework

Небольшой учебный проект с базовыми доменными моделями:

- `Product` с полями `name`, `description`, `price`, `quantity`.
- `Category` с полями `name`, `description`, `products`.
- Счетчики `Category.category_count` и `Category.product_count` обновляются автоматически при создании объектов и добавлении продуктов.
- JSON-загрузчик `load_categories_from_json()` создает объекты из `products.json`.
- `Category` хранит продукты в приватном списке и предоставляет `add_product()` и свойство `products` (форматированный вывод).
- `Product.price` защищен через getter/setter, а `Product.new_product()` создает продукт из `dict`.

## Зависимости

- Python `>= 3.12`
- Dev-зависимости: `pytest`, `pytest-cov`, `flake8` (см. `pyproject.toml` или `requirements-dev.txt`)

## Установка (venv + pip, Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements-dev.txt
```

## Установка (Poetry, опционально)

```powershell
poetry install
```

## Тесты и покрытие

Запуск тестов (покрытие генерируется настройками в `pyproject.toml`):

```powershell
.\.venv\Scripts\python -m pytest
```

Артефакты покрытия:

- `coverage.xml` (XML-отчет)
- `coverage_report.txt` (краткий текстовый отчет)
