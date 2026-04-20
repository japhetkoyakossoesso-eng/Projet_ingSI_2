from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Contribution:
    first_name: str
    last_name: str
    category: str
    quantity: int

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)
