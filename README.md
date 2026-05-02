# RepasPromo

Application de bureau Tkinter pour organiser un repas de groupe. Elle permet de créer des repas, d'ajouter les participants, de suivre les portions par catégorie et de voir rapidement ce qu'il manque.

Le projet fonctionne avec Python seulement. SQLite est inclus dans Python, et l'image d'accueil utilise Tkinter directement. Aucune installation de dépendance externe n'est nécessaire.

## Lancement rapide

Depuis la racine du projet :

```bash
python run.py
```

Sur certains systèmes, la commande Python s'appelle `python3` :

```bash
python3 run.py
```

La base locale est créée automatiquement dans `data/repaspromo.sqlite3`.

## Tests

```bash
python -m unittest discover -s tests
```

ou :

```bash
python3 -m unittest discover -s tests
```

## Fonctionnalités principales

- Créer plusieurs repas avec objectifs par catégorie.
- Ajouter et supprimer des participants.
- Suivre les portions apportées pour les entrées, plats, desserts et boissons.
- Visualiser la viabilité du repas et les catégories manquantes.
- Consulter un tableau de bord avec jauges, conseils et détail des participants.

## Structure simple

- `run.py` : lanceur principal.
- `src/app.py` : démarrage de l'application.
- `src/controllers/` : navigation entre les pages.
- `src/core/` : modèles, validation, logique métier et SQLite.
- `src/ui/` : thème, vues et widgets Tkinter.
- `assets/` : image d'accueil.
- `tests/` : tests unitaires.
- `code brute/` : anciens prototypes conservés comme référence.

## Données

Les données de l'utilisateur restent en local dans SQLite. Le fichier de base n'est pas versionné, car il est généré à l'exécution.

Pour repartir de zéro, fermer l'application puis supprimer :

```text
data/repaspromo.sqlite3
```

## Note Tkinter

Tkinter est inclus avec la plupart des installations Python. Sur Linux, si la fenêtre ne s'ouvre pas, installer le paquet Tk de votre distribution, par exemple `python3-tk`.
