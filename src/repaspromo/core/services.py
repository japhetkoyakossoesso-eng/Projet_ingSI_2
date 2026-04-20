from collections import Counter

from repaspromo.core.models import Contribution
from repaspromo.core.repository import ContributionRepository
from repaspromo.core.validators import normalize_name, validate_category, validate_quantity


class ContributionService:
    def __init__(self, repository: ContributionRepository) -> None:
        self.repository = repository

    def list_contributions(self) -> list[Contribution]:
        return self.repository.load_all()

    def add_contribution(
        self,
        first_name: str,
        last_name: str,
        category: str,
        quantity: str,
    ) -> Contribution:
        contribution = Contribution(
            first_name=normalize_name(first_name),
            last_name=normalize_name(last_name),
            category=validate_category(category),
            quantity=validate_quantity(quantity),
        )
        contributions = self.repository.load_all()
        contributions.append(contribution)
        self.repository.save_all(contributions)
        return contribution

    def get_summary(self) -> dict[str, object]:
        contributions = self.repository.load_all()
        categories = Counter(item.category for item in contributions)
        total_quantity = sum(item.quantity for item in contributions)
        return {
            "total_contributions": len(contributions),
            "total_quantity": total_quantity,
            "categories": dict(categories),
            "is_balanced": len(categories) >= 3 and total_quantity >= 10,
        }
