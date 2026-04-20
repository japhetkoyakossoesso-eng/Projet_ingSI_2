# Projet_ingSI_2

Base de projet Tkinter pour organiser un repas de promotion. Le squelette inclut une application exécutable, une séparation simple entre interface, logique métier et stockage JSON local, ainsi qu'un premier jeu de tests.

## Structure

- `src/main.py` : point d'entrée principal
- `src/repaspromo/` : package applicatif
- `src/repaspromo/controllers/` : orchestration Tkinter
- `src/repaspromo/core/` : modèles, validation, persistance, services
- `src/repaspromo/ui/` : thème, vues et widgets
- `data/` : données locales JSON
- `tests/` : tests unitaires de base
- `assets/` : images et icônes

## Lancer l'application

```bash
PYTHONPATH=src python3 src/main.py
```

## Lancer les tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
