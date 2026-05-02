# Projet_ingSI_2

Application Tkinter pour organiser un repas de promotion. Le projet inclut une interface complète, une séparation entre interface, contrôleur, logique métier et persistance SQLite locale.

## Structure

- `src/main.py` : point d'entrée principal
- `src/controllers/` : orchestration Tkinter et navigation
- `src/core/` : modèles, validation, repository SQLite et services métier
- `src/ui/` : thème, vues et widgets réutilisables
- `assets/` : images et icônes
- `data/repaspromo.sqlite3` : base SQLite créée automatiquement au lancement
- `tests/` : tests unitaires de la logique métier
- `assets/` : images et icônes

## Lancer l'application

```bash
PYTHONPATH=src python3 src/main.py
```

ou :

```bash
PYTHONPATH=src python3 scripts/run.py
```

## Lancer les tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Fonctionnalités

- Créer plusieurs repas avec objectifs par catégorie.
- Ajouter et supprimer des participants.
- Suivre les portions apportées pour les entrées, plats, desserts et boissons.
- Visualiser la viabilité du repas et les catégories manquantes.
- Consulter un tableau de bord avec jauges, conseils et détail des participants.
