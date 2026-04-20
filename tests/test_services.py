import json
import tempfile
import unittest
from pathlib import Path

from repaspromo.core.repository import ContributionRepository
from repaspromo.core.services import ContributionService


class ContributionServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "contributions.json"
        self.data_file.write_text("[]", encoding="utf-8")
        self.repository = ContributionRepository(data_file=self.data_file)
        self.service = ContributionService(self.repository)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_contribution_persists_data(self) -> None:
        self.service.add_contribution("alice", "martin", "Dessert", "3")

        payload = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(payload[0]["first_name"], "Alice")
        self.assertEqual(payload[0]["quantity"], 3)

    def test_summary_aggregates_categories(self) -> None:
        self.service.add_contribution("alice", "martin", "Dessert", "3")
        self.service.add_contribution("bob", "durand", "Plat", "7")
        self.service.add_contribution("claire", "bernard", "Boisson", "2")

        summary = self.service.get_summary()
        self.assertEqual(summary["total_contributions"], 3)
        self.assertEqual(summary["categories"]["Dessert"], 1)
        self.assertTrue(summary["is_balanced"])


if __name__ == "__main__":
    unittest.main()
