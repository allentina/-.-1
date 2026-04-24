"""Project domain package."""

from .loader import load_categories_from_json
from .models import Category, Product

__all__ = ["Category", "Product", "load_categories_from_json"]
