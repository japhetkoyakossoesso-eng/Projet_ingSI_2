from tkinter import ttk


class HomeView(ttk.Frame):
    def __init__(self, parent, on_refresh) -> None:
        super().__init__(parent, padding=24)
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Organisation du repas de promotion", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            self,
            text="Base de travail Tkinter avec navigation, donnees locales et logique metier separee.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 24))

        self.summary_label = ttk.Label(self, text="", style="Subtitle.TLabel")
        self.summary_label.grid(row=2, column=0, sticky="w")

        ttk.Button(self, text="Rafraichir", command=on_refresh).grid(row=3, column=0, sticky="w", pady=(20, 0))

    def render(self, summary: dict[str, object]) -> None:
        text = (
            f"{summary['total_contributions']} contribution(s) enregistree(s), "
            f"{summary['total_quantity']} unite(s) promises."
        )
        self.summary_label.config(text=text)
