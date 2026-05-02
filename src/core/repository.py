from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import CATEGORY_KEYS, CATEGORY_ORDER, Contribution, Meal


class ContributionRepository:
    """Persistance SQLite des repas et des contributions."""

    def __init__(self, data_file: str | Path) -> None:
        self.db_file = Path(data_file)
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_file)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    entree_required INTEGER NOT NULL DEFAULT 5,
                    plat_required INTEGER NOT NULL DEFAULT 12,
                    dessert_required INTEGER NOT NULL DEFAULT 10,
                    boisson_required INTEGER NOT NULL DEFAULT 12,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS contributions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_id INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_contributions_meal
                ON contributions(meal_id);
                """
            )

    def create_meal(self, name: str, requirements: dict[str, int]) -> Meal:
        values = {
            f"{CATEGORY_KEYS[category]}_required": requirements[category]
            for category in CATEGORY_ORDER
        }
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO meals (
                    name,
                    entree_required,
                    plat_required,
                    dessert_required,
                    boisson_required
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    values["entree_required"],
                    values["plat_required"],
                    values["dessert_required"],
                    values["boisson_required"],
                ),
            )
            meal_id = int(cursor.lastrowid)
        meal = self.get_meal(meal_id)
        if meal is None:
            raise RuntimeError("Le repas vient d'être créé mais reste introuvable.")
        return meal

    def list_meals(self) -> list[Meal]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM meals ORDER BY datetime(created_at) DESC, id DESC"
            ).fetchall()
        return [self._row_to_meal(row) for row in rows]

    def get_meal(self, meal_id: int) -> Meal | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM meals WHERE id = ?",
                (meal_id,),
            ).fetchone()
        return self._row_to_meal(row) if row else None

    def delete_meal(self, meal_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM meals WHERE id = ?", (meal_id,))

    def add_contribution(
        self,
        *,
        meal_id: int,
        first_name: str,
        last_name: str,
        category: str,
        quantity: int,
    ) -> Contribution:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO contributions (
                    meal_id,
                    first_name,
                    last_name,
                    category,
                    quantity
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (meal_id, first_name, last_name, category, quantity),
            )
            contribution_id = int(cursor.lastrowid)
            row = connection.execute(
                "SELECT * FROM contributions WHERE id = ?",
                (contribution_id,),
            ).fetchone()
        return self._row_to_contribution(row)

    def list_contributions(self, meal_id: int | None = None) -> list[Contribution]:
        with self._connect() as connection:
            if meal_id is None:
                rows = connection.execute(
                    "SELECT * FROM contributions ORDER BY datetime(created_at) DESC, id DESC"
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT * FROM contributions
                    WHERE meal_id = ?
                    ORDER BY datetime(created_at) DESC, id DESC
                    """,
                    (meal_id,),
                ).fetchall()
        return [self._row_to_contribution(row) for row in rows]

    def delete_contribution(self, contribution_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM contributions WHERE id = ?", (contribution_id,))

    def clear_contributions(self, meal_id: int | None = None) -> None:
        with self._connect() as connection:
            if meal_id is None:
                connection.execute("DELETE FROM contributions")
            else:
                connection.execute("DELETE FROM contributions WHERE meal_id = ?", (meal_id,))

    def _row_to_meal(self, row: sqlite3.Row) -> Meal:
        requirements = {
            category: int(row[f"{CATEGORY_KEYS[category]}_required"])
            for category in CATEGORY_ORDER
        }
        return Meal(
            id=int(row["id"]),
            name=str(row["name"]),
            requirements=requirements,
            created_at=str(row["created_at"]),
        )

    def _row_to_contribution(self, row: sqlite3.Row) -> Contribution:
        return Contribution(
            id=int(row["id"]),
            meal_id=int(row["meal_id"]),
            first_name=str(row["first_name"]),
            last_name=str(row["last_name"]),
            category=str(row["category"]),
            quantity=int(row["quantity"]),
            created_at=str(row["created_at"]),
        )
