from __future__ import annotations

from dataclasses import dataclass


CATEGORY_ORDER = ("Entrée", "Plat", "Dessert", "Boisson")

CATEGORY_KEYS = {
    "Entrée": "entree",
    "Plat": "plat",
    "Dessert": "dessert",
    "Boisson": "boisson",
}

DEFAULT_REQUIREMENTS = {
    "Entrée": 5,
    "Plat": 12,
    "Dessert": 10,
    "Boisson": 12,
}

CATEGORY_META = {
    "Entrée": {"icon": "E", "color": "#4f9d8f"},
    "Plat": {"icon": "P", "color": "#d09b2d"},
    "Dessert": {"icon": "D", "color": "#d96b75"},
    "Boisson": {"icon": "B", "color": "#4f83c2"},
}


@dataclass(frozen=True)
class Meal:
    id: int | None
    name: str
    requirements: dict[str, int]
    created_at: str = ""

    def required_for(self, category: str) -> int:
        return self.requirements.get(category, 0)


@dataclass(frozen=True)
class Contribution:
    id: int | None
    meal_id: int
    first_name: str
    last_name: str
    category: str
    quantity: int
    created_at: str = ""

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass(frozen=True)
class CategoryProgress:
    category: str
    current: int
    required: int
    missing: int

    @property
    def is_complete(self) -> bool:
        return self.missing == 0

    @property
    def ratio(self) -> float:
        if self.required <= 0:
            return 1.0
        return min(self.current / self.required, 1.0)


@dataclass(frozen=True)
class MealSummary:
    meal: Meal
    participants_count: int
    total_quantity: int
    totals: dict[str, int]
    progress: list[CategoryProgress]

    @property
    def missing_categories(self) -> list[str]:
        return [item.category for item in self.progress if not item.is_complete]

    @property
    def is_complete(self) -> bool:
        return not self.missing_categories
