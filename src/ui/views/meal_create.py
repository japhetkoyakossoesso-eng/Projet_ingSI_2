from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from core import CATEGORY_ORDER, DEFAULT_REQUIREMENTS, ValidationError
from ui import theme
from ui.widgets import TopBar


class MealCreateView(tk.Frame):
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, bg=theme.BG_MAIN)
        self.controller = controller
        self.name_var = tk.StringVar()
        self.requirement_vars = {
            category: tk.IntVar(value=DEFAULT_REQUIREMENTS[category])
            for category in CATEGORY_ORDER
        }

        TopBar(self, controller, title="Créer un repas").pack(fill="x")

        body = tk.Frame(self, bg=theme.BG_MAIN)
        body.pack(fill="both", expand=True, padx=34, pady=28)

        tk.Label(body, text="Création d'un repas", bg=theme.BG_MAIN, fg=theme.TEXT_MAIN, font=theme.FONT_TITLE).pack(anchor="w")
        tk.Label(
            body,
            text="Définis l'objectif de portions par catégorie avant d'inviter les participants.",
            bg=theme.BG_MAIN,
            fg=theme.TEXT_MUTED,
            font=("Helvetica", 11),
        ).pack(anchor="w", pady=(4, 18))

        form = theme.card(body, padx=22, pady=20)
        form.pack(fill="x")

        tk.Label(form, text="Nom de l'événement", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_LABEL).pack(anchor="w")
        entry = tk.Entry(form, textvariable=self.name_var, font=("Helvetica", 13), relief="solid", bd=1)
        entry.pack(fill="x", ipady=8, pady=(4, 18))
        entry.focus_set()

        counters = tk.Frame(form, bg=theme.BG_CARD)
        counters.pack(fill="x")
        for index, category in enumerate(CATEGORY_ORDER):
            self._counter(counters, category).grid(row=index // 2, column=index % 2, sticky="ew", padx=8, pady=8)
        counters.columnconfigure(0, weight=1)
        counters.columnconfigure(1, weight=1)

        actions = tk.Frame(body, bg=theme.BG_MAIN)
        actions.pack(fill="x", pady=24)
        theme.make_button(actions, "Créer le repas", self._save, variant="primary", width=20).pack(side="left")
        theme.make_button(actions, "Annuler", controller.show_meal_list, variant="light", width=14).pack(side="left", padx=10)

    def _counter(self, parent: tk.Widget, category: str) -> tk.Frame:
        frame = tk.Frame(parent, bg=theme.BG_CARD, padx=12, pady=12, highlightbackground=theme.BORDER, highlightthickness=1)
        tk.Label(frame, text=f"Nombre de {category.lower()}s requis", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_SECTION).pack(anchor="w")

        row = tk.Frame(frame, bg=theme.BG_CARD)
        row.pack(fill="x", pady=(10, 0))
        theme.make_button(row, "-", lambda: self._increment(category, -1), variant="light", width=4).pack(side="left")
        tk.Label(row, textvariable=self.requirement_vars[category], bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 18, "bold"), width=6).pack(side="left", expand=True)
        theme.make_button(row, "+", lambda: self._increment(category, 1), variant="light", width=4).pack(side="right")
        return frame

    def _increment(self, category: str, delta: int) -> None:
        variable = self.requirement_vars[category]
        variable.set(max(0, min(99, variable.get() + delta)))

    def _save(self) -> None:
        requirements = {category: var.get() for category, var in self.requirement_vars.items()}
        try:
            meal = self.controller.service.create_meal(self.name_var.get(), requirements)
        except ValidationError as exc:
            messagebox.showwarning("Formulaire incomplet", str(exc))
            return
        self.controller.show_organisation(int(meal.id))
