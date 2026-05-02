from __future__ import annotations

from .models import CATEGORY_ORDER, DEFAULT_REQUIREMENTS


class ValidationError(ValueError):
    """Erreur de validation affichable dans l'interface."""


_CATEGORY_ALIASES = {
    "entree": "Entrée",
    "entrée": "Entrée",
    "entrees": "Entrée",
    "entrées": "Entrée",
    "plat": "Plat",
    "plats": "Plat",
    "dessert": "Dessert",
    "desserts": "Dessert",
    "boisson": "Boisson",
    "boissons": "Boisson",
}
_CATEGORY_ALIASES.update({category.casefold(): category for category in CATEGORY_ORDER})


def clean_text(value: str, field_name: str) -> str:
    text = " ".join(str(value).strip().split())
    if not text:
        raise ValidationError(f"Le champ {field_name} est obligatoire.")
    return text


def normalize_name(value: str, field_name: str) -> str:
    text = clean_text(value, field_name)
    return " ".join(part[:1].upper() + part[1:].lower() for part in text.split())


def normalize_meal_name(value: str) -> str:
    return clean_text(value, "nom du repas")


def normalize_category(value: str) -> str:
    key = clean_text(value, "catégorie").casefold()
    category = _CATEGORY_ALIASES.get(key)
    if category is None:
        accepted = ", ".join(CATEGORY_ORDER)
        raise ValidationError(f"Catégorie invalide. Valeurs acceptées : {accepted}.")
    return category


def parse_integer(
    value: str | int,
    field_name: str,
    *,
    min_value: int = 0,
    max_value: int = 999,
) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"Le champ {field_name} doit être un nombre entier.") from exc

    if number < min_value or number > max_value:
        raise ValidationError(
            f"Le champ {field_name} doit être compris entre {min_value} et {max_value}."
        )
    return number


def parse_quantity(value: str | int) -> int:
    return parse_integer(value, "quantité", min_value=1, max_value=999)


def normalize_requirements(values: dict[str, str | int] | None) -> dict[str, int]:
    values = values or DEFAULT_REQUIREMENTS
    requirements: dict[str, int] = {}
    for category in CATEGORY_ORDER:
        raw_value = values.get(category, DEFAULT_REQUIREMENTS[category])
        requirements[category] = parse_integer(
            raw_value,
            f"besoin {category.lower()}",
            min_value=0,
            max_value=99,
        )
    return requirements
