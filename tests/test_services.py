import tempfile
import unittest
from pathlib import Path

from core import ContributionRepository
from core import MealService
from core import ValidationError


class ContributionServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "repaspromo.sqlite3"
        self.repository = ContributionRepository(data_file=self.data_file)
        self.service = MealService(self.repository)
        self.meal = self.service.create_meal(
            "Repas test",
            {
                "Entrée": 1,
                "Plat": 7,
                "Dessert": 3,
                "Boisson": 2,
            },
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_contribution_persists_data(self) -> None:
        contribution = self.service.add_contribution(
            int(self.meal.id),
            "alice",
            "martin",
            "Dessert",
            "3",
        )

        contributions = self.repository.list_contributions(int(self.meal.id))
        self.assertEqual(contribution.first_name, "Alice")
        self.assertEqual(contributions[0].first_name, "Alice")
        self.assertEqual(contributions[0].quantity, 3)

    def test_summary_aggregates_categories(self) -> None:
        self.service.add_contribution(int(self.meal.id), "alice", "martin", "Dessert", "3")
        self.service.add_contribution(int(self.meal.id), "bob", "durand", "Plat", "7")
        self.service.add_contribution(int(self.meal.id), "claire", "bernard", "Boisson", "2")

        summary = self.service.get_summary(int(self.meal.id))
        self.assertEqual(summary.participants_count, 3)
        self.assertEqual(summary.totals["Dessert"], 3)
        self.assertFalse(summary.is_complete)
        self.assertEqual(summary.missing_categories, ["Entrée"])

    def test_summary_marks_complete_meal(self) -> None:
        self.service.add_contribution(int(self.meal.id), "alice", "martin", "Dessert", "3")
        self.service.add_contribution(int(self.meal.id), "bob", "durand", "Plat", "7")
        self.service.add_contribution(int(self.meal.id), "claire", "bernard", "Boisson", "2")
        self.service.add_contribution(int(self.meal.id), "dan", "leroy", "Entrée", "1")

        summary = self.service.get_summary(int(self.meal.id))
        self.assertTrue(summary.is_complete)
        self.assertEqual(summary.total_quantity, 13)

    def test_invalid_quantity_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.add_contribution(int(self.meal.id), "alice", "martin", "Dessert", "0")


if __name__ == "__main__":
    unittest.main()
