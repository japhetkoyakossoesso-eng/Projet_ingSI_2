from __future__ import annotations

import tkinter as tk

from ui import theme


class TopBar(tk.Frame):
    def __init__(self, parent: tk.Widget, controller, title: str = "RepasPromo") -> None:
        super().__init__(parent, bg=theme.BG_CARD, height=63)
        self.controller = controller
        self.pack_propagate(False)

        content = tk.Frame(self, bg=theme.BG_CARD, height=60)
        content.pack(fill="x", side="top")
        content.pack_propagate(False)

        tk.Label(
            content,
            text=title,
            bg=theme.BG_CARD,
            fg=theme.TEXT_MAIN,
            font=("Helvetica", 15, "bold"),
        ).pack(side="left", padx=22)

        actions = tk.Frame(content, bg=theme.BG_CARD)
        actions.pack(side="right", padx=18)

        buttons = [
            ("Accueil", "accent", lambda: controller.show_home()),
            ("Repas", "accent", lambda: controller.show_meal_list()),
            ("Créer", "accent", lambda: controller.show_meal_create()),
        ]
        current = controller.current_meal_id
        if current is not None:
            buttons.append(("Organisation", "light", lambda: controller.show_organisation(current)))
            buttons.append(("Tableau de bord", "primary", lambda: controller.show_dashboard(current)))

        for text, variant, command in buttons:
            theme.make_button(actions, text, command, variant=variant).pack(
                side="left",
                padx=4,
                pady=10,
            )

        tk.Frame(self, bg=theme.ACCENT_ORANGE, height=3).pack(fill="x", side="bottom")
