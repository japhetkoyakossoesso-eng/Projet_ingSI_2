from __future__ import annotations

from .models import (
    CATEGORY_ORDER,
    DEFAULT_REQUIREMENTS,
    CategoryProgress,
    Contribution,
    Meal,
    MealSummary,
)
from .repository import ContributionRepository
from .validators import (
    ValidationError,
    normalize_category,
    normalize_meal_name,
    normalize_name,
    normalize_requirements,
    parse_quantity,
)


class MealNotFoundError(LookupError):
    pass


class MealService:
    def __init__(self, repository: ContributionRepository) -> None:
        self.repository = repository

    def create_meal(
        self,
        name: str,
        requirements: dict[str, str | int] | None = None,
    ) -> Meal:
        return self.repository.create_meal(
            normalize_meal_name(name),
            normalize_requirements(requirements),
        )

    def ensure_default_meal(self) -> Meal:
        meals = self.repository.list_meals()
        if meals:
            return meals[0]
        return self.create_meal("Mon Repas d'Anniversaire", DEFAULT_REQUIREMENTS)

    def list_meals(self) -> list[Meal]:
        return self.repository.list_meals()

    def get_meal(self, meal_id: int) -> Meal:
        meal = self.repository.get_meal(meal_id)
        if meal is None:
            raise MealNotFoundError(f"Repas introuvable: {meal_id}")
        return meal

    def delete_meal(self, meal_id: int) -> None:
        self.repository.delete_meal(meal_id)

    def add_contribution(
        self,
        meal_id: int,
        first_name: str,
        last_name: str,
        category: str,
        quantity: str | int,
    ) -> Contribution:
        self.get_meal(meal_id)
        return self.repository.add_contribution(
            meal_id=meal_id,
            first_name=normalize_name(first_name, "prénom"),
            last_name=normalize_name(last_name, "nom"),
            category=normalize_category(category),
            quantity=parse_quantity(quantity),
        )

    def list_contributions(self, meal_id: int) -> list[Contribution]:
        self.get_meal(meal_id)
        return self.repository.list_contributions(meal_id)

    def delete_contribution(self, contribution_id: int) -> None:
        self.repository.delete_contribution(contribution_id)

    def clear_contributions(self, meal_id: int) -> None:
        self.get_meal(meal_id)
        self.repository.clear_contributions(meal_id)

    def get_summary(self, meal_id: int) -> MealSummary:
        meal = self.get_meal(meal_id)
        contributions = self.repository.list_contributions(meal_id)
        totals = {category: 0 for category in CATEGORY_ORDER}
        for contribution in contributions:
            totals[contribution.category] += contribution.quantity

        progress = [
            CategoryProgress(
                category=category,
                current=totals[category],
                required=meal.requirements[category],
                missing=max(0, meal.requirements[category] - totals[category]),
            )
            for category in CATEGORY_ORDER
        ]

        return MealSummary(
            meal=meal,
            participants_count=len(contributions),
            total_quantity=sum(item.quantity for item in contributions),
            totals=totals,
            progress=progress,
        )

    def get_advice(self, meal_id: int) -> list[tuple[str, str]]:
        summary = self.get_summary(meal_id)
        if summary.is_complete:
            return [
                (
                    "Repas équilibré",
                    "Tous les besoins sont atteints. Les prochaines inscriptions peuvent rester libres.",
                )
            ]

        advice: list[tuple[str, str]] = []
        for item in summary.progress:
            if item.missing:
                advice.append(
                    (
                        f"Chercher pour {item.category.lower()}",
                        f"Il manque encore {item.missing} portion(s). Oriente les prochains inscrits vers cette catégorie.",
                    )
                )
        return advice


class ContributionService(MealService):
    """Compatibilité avec les premiers tests et le squelette initial."""

    def __init__(self, repository: ContributionRepository) -> None:
        super().__init__(repository)
        self.default_meal = self.ensure_default_meal()

    def add_contribution(  # type: ignore[override]
        self,
        first_name: str,
        last_name: str,
        category: str,
        quantity: str | int,
        meal_id: int | None = None,
    ) -> Contribution:
        return super().add_contribution(
            meal_id or int(self.default_meal.id),
            first_name,
            last_name,
            category,
            quantity,
        )

    def get_summary(self, meal_id: int | None = None) -> dict[str, object]:  # type: ignore[override]
        summary = super().get_summary(meal_id or int(self.default_meal.id))
        category_counts = {category: 0 for category in CATEGORY_ORDER}
        for contribution in self.repository.list_contributions(summary.meal.id):
            category_counts[contribution.category] += 1

        return {
            "meal": summary.meal,
            "total_contributions": summary.participants_count,
            "total_quantity": summary.total_quantity,
            "categories": category_counts,
            "category_totals": summary.totals,
            "missing_categories": summary.missing_categories,
            "is_balanced": summary.is_complete,
        }


__all__ = [
    "ContributionRepository",
    "ContributionService",
    "MealNotFoundError",
    "MealService",
    "ValidationError",
]
