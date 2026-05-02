from __future__ import annotations

import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent: tk.Widget, *, bg: str) -> None:
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=bg)

        self.content.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        def resize_content(event) -> None:
            self.canvas.itemconfig(window_id, width=event.width)

        self.canvas.bind("<Configure>", resize_content)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind(
            "<Enter>",
            lambda _event: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel),
        )
        self.canvas.bind(
            "<Leave>",
            lambda _event: self.canvas.unbind_all("<MouseWheel>"),
        )

    def _on_mousewheel(self, event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
