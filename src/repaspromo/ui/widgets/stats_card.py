from tkinter import ttk


class StatsCard(ttk.Frame):
    def __init__(self, parent, title: str) -> None:
        super().__init__(parent, padding=18, style="Card.TFrame")
        ttk.Label(self, text=title, style="CardTitle.TLabel").pack(anchor="w")
        self.value_label = ttk.Label(self, text="0", style="CardValue.TLabel")
        self.value_label.pack(anchor="w", pady=(10, 0))

    def set_value(self, value: str) -> None:
        self.value_label.config(text=value)
