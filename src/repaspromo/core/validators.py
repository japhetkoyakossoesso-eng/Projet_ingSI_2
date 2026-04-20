CATEGORIES = ("Entree", "Plat", "Dessert", "Boisson", "Materiel")


def normalize_name(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) < 2:
        raise ValueError("Le nom et le prenom doivent contenir au moins 2 caracteres.")
    return cleaned.capitalize()


def validate_category(value: str) -> str:
    if value not in CATEGORIES:
        raise ValueError("Categorie inconnue.")
    return value


def validate_quantity(value: str) -> int:
    try:
        quantity = int(value)
    except ValueError as exc:
        raise ValueError("La quantite doit etre un entier.") from exc
    if quantity <= 0:
        raise ValueError("La quantite doit etre strictement positive.")
    return quantity
