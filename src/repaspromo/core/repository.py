import json
from pathlib import Path

from repaspromo.config import DATA_DIR, DATA_FILE
from repaspromo.core.models import Contribution


class ContributionRepository:
    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self.data_file = data_file
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self.save_all([])

    def load_all(self) -> list[Contribution]:
        raw_data = json.loads(self.data_file.read_text(encoding="utf-8"))
        return [Contribution(**item) for item in raw_data]

    def save_all(self, contributions: list[Contribution]) -> None:
        payload = [item.to_dict() for item in contributions]
        self.data_file.write_text(
            json.dumps(payload, ensure_ascii=True, indent=2),
            encoding="utf-8",
        )
