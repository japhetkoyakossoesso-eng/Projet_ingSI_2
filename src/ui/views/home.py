from __future__ import annotations

import tkinter as tk

from config import HERO_IMAGE
from ui import theme
from ui.widgets import TopBar


class HomeView(tk.Frame):
    def __init__(self, parent: tk.Widget, controller) -> None:
        super().__init__(parent, bg=theme.BG_MAIN)
        self.controller = controller
        self.hero_photo = None
        self.hero_native_photo = None
        self.hero_source = None

        TopBar(self, controller, title="RepasPromo").pack(fill="x")

        body = tk.Frame(self, bg=theme.BG_MAIN)
        body.pack(fill="both", expand=True, padx=30, pady=(24, 26))

        self._build_hero(body)

        stats = tk.Frame(body, bg=theme.BG_MAIN)
        stats.pack(fill="x", pady=(18, 0))

        meals = controller.service.list_meals()
        participants = sum(controller.service.get_summary(int(meal.id)).participants_count for meal in meals)
        quantities = sum(controller.service.get_summary(int(meal.id)).total_quantity for meal in meals)

        for index, (label, value, caption) in enumerate(
            (
                ("Repas créés", len(meals), "Événements suivis dans SQLite"),
                ("Participants inscrits", participants, "Toutes contributions confondues"),
                ("Portions prévues", quantities, "Total des apports enregistrés"),
            )
        ):
            item = theme.card(stats)
            item.pack(side="left", fill="x", expand=True, padx=8)
            color = (theme.ACCENT_ORANGE, "#4f9d8f", "#4f83c2")[index]
            tk.Label(item, text=str(value), bg=theme.BG_CARD, fg=color, font=theme.FONT_BIG).pack(anchor="w")
            tk.Label(item, text=label, bg=theme.BG_CARD, fg=theme.TEXT_MAIN, font=theme.FONT_SECTION).pack(anchor="w")
            tk.Label(item, text=caption, bg=theme.BG_CARD, fg=theme.TEXT_MUTED, font=theme.FONT_SMALL).pack(anchor="w", pady=(4, 0))

    def _build_hero(self, parent: tk.Widget) -> None:
        self.hero_canvas = tk.Canvas(parent, height=410, bg=theme.BG_SOFT, highlightthickness=0)
        self.hero_canvas.pack(fill="x")

        try:
            from PIL import Image

            self.hero_source = Image.open(HERO_IMAGE).convert("RGB")
        except Exception:
            self.hero_source = None
            try:
                self.hero_native_photo = tk.PhotoImage(file=str(HERO_IMAGE))
            except Exception:
                self.hero_native_photo = None

        self.hero_canvas.bind("<Configure>", self._render_hero)

    def _render_hero(self, event) -> None:
        width = max(event.width, 1)
        height = max(event.height, 1)
        canvas = self.hero_canvas
        canvas.delete("all")

        if self.hero_source is not None:
            self._draw_cover_image(width, height)
        elif self.hero_native_photo is not None:
            canvas.create_image(width / 2, height / 2, image=self.hero_native_photo, anchor="center")
        else:
            canvas.create_rectangle(0, 0, width, height, fill=theme.BG_SOFT, outline="")
            canvas.create_rectangle(width * 0.55, 0, width, height, fill="#ead7bd", outline="")

        canvas.create_rectangle(0, 0, width, height, fill="#000000", stipple="gray25", outline="")
        canvas.create_rectangle(0, 0, min(620, width * 0.62), height, fill="#1a1a1a", stipple="gray50", outline="")

        left = 54
        top = 78
        canvas.create_text(
            left,
            top,
            text="RepasPromo",
            anchor="w",
            fill=theme.ACCENT_ORANGE,
            font=("Helvetica", 13, "bold"),
        )
        canvas.create_text(
            left,
            top + 100,
            text="Organisez des repas\nde groupe sans prise\nde tête.",
            anchor="w",
            fill="#ffffff",
            font=("Helvetica", 34, "bold"),
        )
        canvas.create_text(
            left,
            top + 205,
            text="Créez un repas, suivez les participants et repérez les catégories manquantes en temps réel.",
            anchor="w",
            width=460,
            fill="#f7efe5",
            font=("Helvetica", 13),
        )

        button_y = top + 278
        self._hero_button(
            left,
            button_y,
            150,
            "Voir les repas",
            self.controller.show_meal_list,
            theme.ACCENT_ORANGE,
        )
        self._hero_button(
            left + 168,
            button_y,
            158,
            "Créer un repas",
            self.controller.show_meal_create,
            "#ffffff",
            text_color=theme.TEXT_MAIN,
        )

    def _draw_cover_image(self, width: int, height: int) -> None:
        from PIL import Image, ImageTk

        source = self.hero_source
        source_ratio = source.width / source.height
        target_ratio = width / height

        if source_ratio > target_ratio:
            new_height = source.height
            new_width = int(new_height * target_ratio)
            left = (source.width - new_width) // 2
            box = (left, 0, left + new_width, source.height)
        else:
            new_width = source.width
            new_height = int(new_width / target_ratio)
            top = (source.height - new_height) // 2
            box = (0, top, source.width, top + new_height)

        resampling = getattr(Image, "Resampling", Image).LANCZOS
        image = source.crop(box).resize((width, height), resampling)
        self.hero_photo = ImageTk.PhotoImage(image)
        self.hero_canvas.create_image(0, 0, image=self.hero_photo, anchor="nw")

    def _hero_button(
        self,
        x: int,
        y: int,
        width: int,
        text: str,
        command,
        bg: str,
        *,
        text_color: str = "#ffffff",
    ) -> None:
        button = tk.Button(
            self.hero_canvas,
            text=text,
            command=command,
            bg=bg,
            fg=text_color,
            activebackground=bg,
            activeforeground=text_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
        )
        self.hero_canvas.create_window(x, y, window=button, anchor="nw", width=width, height=42)
