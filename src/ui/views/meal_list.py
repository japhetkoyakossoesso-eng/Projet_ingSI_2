from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from core import CATEGORY_ORDER, Meal
from ui import theme
from ui.widgets import ScrollableFrame, TopBar


class MealListView(tk.Frame):
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, bg=theme.BG_MAIN)
        self.controller = controller

        TopBar(self, controller, title="Liste des repas").pack(fill="x")

        body = tk.Frame(self, bg=theme.BG_MAIN)
        body.pack(fill="both", expand=True, padx=34, pady=28)

        header = tk.Frame(body, bg=theme.BG_MAIN)
        header.pack(fill="x", pady=(0, 18))
        tk.Label(header, text="Liste des repas", bg=theme.BG_MAIN, fg=theme.TEXT_MAIN, font=theme.FONT_TITLE).pack(side="left")
        theme.make_button(header, "+ Nouveau repas", controller.show_meal_create, variant="primary").pack(side="right")

        meals = controller.service.list_meals()
        if not meals:
            self._empty_state(body)
            return

        scroll = ScrollableFrame(body, bg=theme.BG_MAIN)
        scroll.pack(fill="both", expand=True)
        for meal in meals:
            self._meal_card(scroll.content, meal)

    def _empty_state(self, parent: tk.Widget) -> None:
        empty = theme.card(parent, padx=32, pady=28)
        empty.pack(fill="x")
        tk.Label(
            empty,
            text="Aucun repas créé pour l'instant",
            bg=theme.BG_CARD,
            fg=theme.TEXT_MAIN,
            font=("Helvetica", 17, "bold"),
        ).pack(anchor="w")
        tk.Label(
            empty,
            text="Crée ton premier repas pour commencer à suivre les entrées, plats, desserts et boissons.",
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED,
            font=("Helvetica", 11),
        ).pack(anchor="w", pady=(8, 16))
        theme.make_button(empty, "Créer un repas", self.controller.show_meal_create, variant="accent").pack(anchor="w")

    def _meal_card(self, parent: tk.Widget, meal: Meal) -> None:
        summary = self.controller.service.get_summary(int(meal.id))
        card = theme.card(parent, padx=18, pady=16)
        card.pack(fill="x", pady=7)

        top = tk.Frame(card, bg=theme.BG_CARD)
        top.pack(fill="x")
        tk.Label(top, text=meal.name, bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 15, "bold")).pack(side="left")
        state_text = "Complet" if summary.is_complete else "À compléter"
        state_color = theme.SUCCESS_FG if summary.is_complete else theme.ACCENT_RED
        tk.Label(top, text=state_text, bg=theme.BG_CARD, fg=state_color, font=theme.FONT_SECTION).pack(side="right")

        details = "  -  ".join(
            f"{summary.totals[category]}/{meal.requirements[category]} {category}s"
            for category in CATEGORY_ORDER
        )
        tk.Label(card, text=details, bg=theme.BG_CARD, fg=theme.ACCENT_RED, font=("Helvetica", 10)).pack(anchor="w", pady=(8, 0))
        tk.Label(
            card,
            text=f"{summary.participants_count} participant(s) - {summary.total_quantity} portion(s)",
            bg=theme.BG_CARD,
            fg=theme.TEXT_MUTED,
            font=theme.FONT_SMALL,
        ).pack(anchor="w", pady=(4, 10))

        actions = tk.Frame(card, bg=theme.BG_CARD)
        actions.pack(fill="x")
        theme.make_button(actions, "Organiser", lambda: self.controller.show_organisation(int(meal.id)), variant="primary").pack(side="left")
        theme.make_button(actions, "Tableau de bord", lambda: self.controller.show_dashboard(int(meal.id)), variant="accent").pack(side="left", padx=8)
        theme.make_button(actions, "Supprimer", lambda: self._delete_meal(meal), variant="danger").pack(side="right")

    def _delete_meal(self, meal: Meal) -> None:
        if messagebox.askyesno("Supprimer le repas", f"Supprimer « {meal.name} » et tous ses participants ?"):
            self.controller.service.delete_meal(int(meal.id))
            if self.controller.current_meal_id == meal.id:
                self.controller.current_meal_id = None
            self.controller.show_meal_list()
