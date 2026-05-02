from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from core import CATEGORY_META, CATEGORY_ORDER, Contribution, ValidationError
from ui import theme
from ui.widgets import ScrollableFrame, TopBar


class OrganisationView(tk.Frame):
    def __init__(self, parent: tk.Widget, controller, meal_id: int) -> None:
        super().__init__(parent, bg=theme.BG_MAIN)
        self.controller = controller
        self.meal_id = meal_id
        self.meal = controller.service.get_meal(meal_id)
        self.summary = controller.service.get_summary(meal_id)

        default_category = self.summary.missing_categories[0] if self.summary.missing_categories else CATEGORY_ORDER[0]
        self.selected_category = tk.StringVar(value=default_category)
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.quantity_var = tk.IntVar(value=10)

        TopBar(self, controller, title=self.meal.name).pack(fill="x")

        body = tk.Frame(self, bg=theme.BG_MAIN)
        body.pack(fill="both", expand=True, padx=30, pady=24)

        left = tk.Frame(body, bg=theme.BG_MAIN, width=370)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(body, bg=theme.BG_MAIN)
        right.pack(side="left", fill="both", expand=True, padx=(22, 0))

        self._build_form(left)
        self._build_status(right)
        self._build_participants(right)

    def _build_form(self, parent: tk.Widget) -> None:
        form = theme.card(parent, padx=18, pady=16)
        form.pack(fill="x")

        tk.Label(form, text="Ajouter un participant", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 14, "bold")).pack(anchor="w")
        tk.Label(form, text="Chaque participant choisit une catégorie et le nombre de portions apportées.", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SMALL).pack(anchor="w", pady=(4, 14))

        tk.Label(form, text="Prénom", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_LABEL).pack(anchor="w")
        tk.Entry(form, textvariable=self.first_name_var, relief="solid", bd=1, font=("Helvetica", 12)).pack(fill="x", ipady=6, pady=(4, 10))

        tk.Label(form, text="Nom", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_LABEL).pack(anchor="w")
        tk.Entry(form, textvariable=self.last_name_var, relief="solid", bd=1, font=("Helvetica", 12)).pack(fill="x", ipady=6, pady=(4, 14))

        tk.Label(form, text="Catégorie", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_SECTION).pack(anchor="w")
        tiles = tk.Frame(form, bg=theme.BG_CARD)
        tiles.pack(fill="x", pady=(8, 14))
        for index, category in enumerate(CATEGORY_ORDER):
            self._category_tile(tiles, category).grid(row=index // 2, column=index % 2, sticky="ew", padx=5, pady=5)
        tiles.columnconfigure(0, weight=1)
        tiles.columnconfigure(1, weight=1)

        tk.Label(form, text="Quantité de portions", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_SECTION).pack(anchor="w")
        quantity = tk.Frame(form, bg=theme.BG_CARD)
        quantity.pack(fill="x", pady=(8, 16))
        theme.make_button(quantity, "-", lambda: self._increment_quantity(-1), variant="light", width=4).pack(side="left")
        tk.Label(quantity, textvariable=self.quantity_var, bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_BIG, width=6).pack(side="left", expand=True)
        theme.make_button(quantity, "+", lambda: self._increment_quantity(1), variant="light", width=4).pack(side="right")

        theme.make_button(form, "Valider l'ajout", self._add_contribution, variant="primary").pack(fill="x")

        nav = tk.Frame(parent, bg=theme.BG_MAIN)
        nav.pack(fill="x", pady=14)
        theme.make_button(nav, "Retour à la liste", self.controller.show_meal_list, variant="light").pack(fill="x")

    def _category_tile(self, parent: tk.Widget, category: str) -> tk.Radiobutton:
        meta = CATEGORY_META[category]
        return tk.Radiobutton(
            parent,
            text=f"{meta['icon']}  {category}",
            variable=self.selected_category,
            value=category,
            indicatoron=False,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MAIN,
            selectcolor="#f2f2f2",
            activebackground="#f2f2f2",
            activeforeground=theme.TEXT_MAIN,
            relief="solid",
            bd=1,
            padx=10,
            pady=8,
            cursor="hand2",
            font=theme.FONT_SECTION,
        )

    def _build_status(self, parent: tk.Widget) -> None:
        status = theme.card(parent, padx=18, pady=16)
        status.pack(fill="x")

        tk.Label(status, text="Viabilité du repas", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 15, "bold")).pack(anchor="w")

        if self.summary.is_complete:
            banner_bg = theme.SUCCESS_BG
            banner_fg = theme.SUCCESS_FG
            banner_text = "Le repas est complet."
        else:
            banner_bg = theme.ALERT_BG
            banner_fg = theme.ALERT_FG
            banner_text = "Il manque : " + ", ".join(category.lower() for category in self.summary.missing_categories)

        banner = tk.Frame(status, bg=banner_bg, padx=12, pady=10)
        banner.pack(fill="x", pady=(10, 14))
        tk.Label(banner, text=banner_text, bg=banner_bg, fg=banner_fg, font=theme.FONT_SECTION).pack(anchor="w")

        progress_grid = tk.Frame(status, bg=theme.BG_CARD)
        progress_grid.pack(fill="x")
        for index, item in enumerate(self.summary.progress):
            self._progress_item(progress_grid, item).grid(row=0, column=index, sticky="ew", padx=6)
            progress_grid.columnconfigure(index, weight=1)

    def _progress_item(self, parent: tk.Widget, item) -> tk.Frame:
        frame = tk.Frame(parent, bg=theme.BG_CARD)
        color = theme.SUCCESS_FG if item.is_complete else theme.ACCENT_ORANGE
        tk.Label(frame, text=item.category, bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SMALL).pack(anchor="w")
        tk.Label(frame, text=f"{item.current}/{item.required}", bg=theme.BG_CARD, fg=color, font=("Helvetica", 18, "bold")).pack(anchor="w")
        tk.Label(frame, text="OK" if item.is_complete else f"-{item.missing}", bg=theme.BG_CARD, fg=color, font=theme.FONT_SMALL).pack(anchor="w")
        return frame

    def _build_participants(self, parent: tk.Widget) -> None:
        panel = theme.card(parent, padx=0, pady=0)
        panel.pack(fill="both", expand=True, pady=(16, 0))

        header = tk.Frame(panel, bg=theme.BG_CARD, padx=16, pady=12)
        header.pack(fill="x")
        tk.Label(header, text=f"{self.summary.participants_count} participant(s)", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 14, "bold")).pack(side="left")
        theme.make_button(header, "Tout supprimer", self._clear_contributions, variant="danger").pack(side="right")

        tk.Frame(panel, bg=theme.BORDER, height=1).pack(fill="x")

        scroll = ScrollableFrame(panel, bg=theme.BG_CARD)
        scroll.pack(fill="both", expand=True)
        contributions = self.controller.service.list_contributions(self.meal_id)
        if not contributions:
            tk.Label(scroll.content, text="Aucun participant pour l'instant.", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=("Helvetica", 12)).pack(pady=34)
            return

        for contribution in contributions:
            self._participant_row(scroll.content, contribution)

    def _participant_row(self, parent: tk.Widget, contribution: Contribution) -> None:
        row = tk.Frame(parent, bg=theme.BG_CARD, padx=16, pady=10)
        row.pack(fill="x")

        initials = (contribution.first_name[:1] + contribution.last_name[:1]).upper()
        color = CATEGORY_META[contribution.category]["color"]
        tk.Label(row, text=initials, bg=color, fg="#ffffff", width=4, font=("Helvetica", 11, "bold"), padx=4, pady=7).pack(side="left", padx=(0, 12))

        info = tk.Frame(row, bg=theme.BG_CARD)
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=contribution.display_name, bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_SECTION).pack(anchor="w")
        tk.Label(info, text=f"{contribution.quantity} portion(s) - {contribution.category}", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SMALL).pack(anchor="w")

        theme.make_button(row, "Supprimer", lambda: self._delete_contribution(int(contribution.id)), variant="light").pack(side="right")
        tk.Frame(parent, bg=theme.BORDER, height=1).pack(fill="x", padx=16)

    def _increment_quantity(self, delta: int) -> None:
        self.quantity_var.set(max(1, min(999, self.quantity_var.get() + delta)))

    def _add_contribution(self) -> None:
        try:
            self.controller.service.add_contribution(
                self.meal_id,
                self.first_name_var.get(),
                self.last_name_var.get(),
                self.selected_category.get(),
                self.quantity_var.get(),
            )
        except ValidationError as exc:
            messagebox.showwarning("Formulaire incomplet", str(exc))
            return
        self.controller.show_organisation(self.meal_id)

    def _delete_contribution(self, contribution_id: int) -> None:
        self.controller.service.delete_contribution(contribution_id)
        self.controller.show_organisation(self.meal_id)

    def _clear_contributions(self) -> None:
        if messagebox.askyesno("Tout supprimer", "Supprimer tous les participants de ce repas ?"):
            self.controller.service.clear_contributions(self.meal_id)
            self.controller.show_organisation(self.meal_id)
