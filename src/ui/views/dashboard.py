from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core import CATEGORY_META, CATEGORY_ORDER
from ui import theme
from ui.widgets import TopBar


class DashboardView(tk.Frame):
    def __init__(self, parent: tk.Widget, controller, meal_id: int) -> None:
        super().__init__(parent, bg=theme.BG_MAIN)
        self.controller = controller
        self.meal_id = meal_id
        self.meal = controller.service.get_meal(meal_id)
        self.summary = controller.service.get_summary(meal_id)

        TopBar(self, controller, title=f"Tableau de bord - {self.meal.name}").pack(fill="x")

        body = tk.Frame(self, bg=theme.BG_MAIN)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content(body)

    def _build_sidebar(self, parent: tk.Widget) -> None:
        sidebar = tk.Frame(parent, bg=theme.BG_SIDEBAR, width=300, padx=20, pady=24)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="CONSEILS POUR L'ORGANISATEUR",
            bg=theme.BG_SIDEBAR,
            fg=theme.TEXT_MAIN,
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w", pady=(0, 16))

        for title, text in self.controller.service.get_advice(self.meal_id):
            item = tk.Frame(sidebar, bg="#f0c5ad", padx=12, pady=12)
            item.pack(fill="x", pady=8)
            tk.Label(item, text=title, bg="#f0c5ad", fg=theme.ALERT_FG, font=theme.FONT_SECTION).pack(anchor="w")
            tk.Label(item, text=text, bg="#f0c5ad", fg=theme.ALERT_FG, font=theme.FONT_SMALL, justify="left", wraplength=230).pack(anchor="w", pady=(5, 0))

        theme.make_button(sidebar, "Retour organiser", lambda: self.controller.show_organisation(self.meal_id), variant="primary").pack(fill="x", pady=(18, 0))

    def _build_content(self, parent: tk.Widget) -> None:
        content = tk.Frame(parent, bg=theme.BG_MAIN)
        content.pack(side="left", fill="both", expand=True, padx=30, pady=26)

        tk.Label(content, text="Tableau de bord", bg=theme.BG_MAIN, fg=theme.TEXT_MAIN, font=theme.FONT_TITLE).pack(anchor="w")
        tk.Frame(content, bg=theme.ACCENT_DARK, height=2, width=250).pack(anchor="w", pady=(5, 18))

        self._build_stats(content)

        lower = tk.Frame(content, bg=theme.BG_MAIN)
        lower.pack(fill="both", expand=True, pady=(18, 0))
        self._build_progress(lower)
        self._build_table(lower)

    def _build_stats(self, parent: tk.Widget) -> None:
        stats = tk.Frame(parent, bg=theme.BG_MAIN)
        stats.pack(fill="x")

        data = [
            ("Participants", self.summary.participants_count, theme.TEXT_MAIN),
            ("Portions", self.summary.total_quantity, theme.ACCENT_ORANGE),
            ("Catégories OK", len(CATEGORY_ORDER) - len(self.summary.missing_categories), theme.SUCCESS_FG),
            ("Manquantes", len(self.summary.missing_categories), theme.ACCENT_RED if self.summary.missing_categories else theme.SUCCESS_FG),
        ]

        for index, (label, value, color) in enumerate(data):
            card = theme.card(stats)
            card.grid(row=0, column=index, sticky="ew", padx=7)
            tk.Label(card, text=str(value), bg=theme.BG_CARD, fg=color, font=theme.FONT_BIG).pack()
            tk.Label(card, text=label, bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SMALL).pack()
            stats.columnconfigure(index, weight=1)

    def _build_progress(self, parent: tk.Widget) -> None:
        panel = theme.card(parent)
        panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(panel, text="Jauges de besoin", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 14, "bold")).pack(anchor="w")

        for item in self.summary.progress:
            row = tk.Frame(panel, bg=theme.BG_CARD)
            row.pack(fill="x", pady=9)
            color = CATEGORY_META[item.category]["color"]
            tk.Frame(row, bg=color, width=12, height=12).pack(side="left", padx=(0, 8))
            tk.Label(row, text=item.category, bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_LABEL, width=9, anchor="w").pack(side="left")
            canvas = tk.Canvas(row, height=10, bg="#eeeeee", highlightthickness=0)
            canvas.pack(side="left", fill="x", expand=True, padx=8)
            canvas.create_rectangle(0, 0, 360 * item.ratio, 10, fill=color, outline="")
            tk.Label(row, text=f"{item.current}/{item.required}", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SMALL, width=8).pack(side="left")

        self._build_chart(panel)

    def _build_chart(self, parent: tk.Widget) -> None:
        tk.Label(parent, text="Répartition actuelle", bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SECTION).pack(anchor="w", pady=(16, 8))
        canvas = tk.Canvas(parent, width=520, height=210, bg="#ffffff", highlightbackground=theme.BORDER, highlightthickness=1)
        canvas.pack(fill="x")

        max_value = max([item.required for item in self.summary.progress] + [item.current for item in self.summary.progress] + [1])
        base_y = 170
        bar_width = 62
        spacing = 62
        start_x = 45

        canvas.create_line(30, base_y, 500, base_y, fill=theme.BORDER)
        for index, item in enumerate(self.summary.progress):
            x = start_x + index * (bar_width + spacing)
            current_h = int((item.current / max_value) * 120)
            required_h = int((item.required / max_value) * 120)
            color = CATEGORY_META[item.category]["color"]
            canvas.create_rectangle(x, base_y - required_h, x + bar_width, base_y, fill="#eeeeee", outline="")
            canvas.create_rectangle(x, base_y - current_h, x + bar_width, base_y, fill=color, outline="")
            canvas.create_text(x + bar_width / 2, base_y + 18, text=item.category, font=("Helvetica", 8))
            canvas.create_text(x + bar_width / 2, base_y - current_h - 10, text=str(item.current), font=("Helvetica", 8, "bold"), fill=theme.TEXT_MAIN)

    def _build_table(self, parent: tk.Widget) -> None:
        panel = theme.card(parent)
        panel.pack(side="left", fill="both", expand=True, padx=(10, 0))
        tk.Label(panel, text="Détail des participants", bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(0, 10))

        columns = ("Prénom", "Nom", "Catégorie", "Portions")
        tree = ttk.Treeview(panel, columns=columns, show="headings", height=12)
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=95, anchor="center")

        for contribution in self.controller.service.list_contributions(self.meal_id):
            tree.insert(
                "",
                "end",
                values=(
                    contribution.first_name,
                    contribution.last_name,
                    contribution.category,
                    contribution.quantity,
                ),
            )

        scroll = ttk.Scrollbar(panel, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")
