from tkinter import ttk


class PlanningView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=24)
        ttk.Label(self, text="Organisation", style="Title.TLabel").pack(anchor="w")
        self.content = ttk.Label(self, text="", style="Subtitle.TLabel", justify="left")
        self.content.pack(anchor="w", pady=(16, 0))

    def render(self, summary: dict[str, object]) -> None:
        categories = summary["categories"]
        if categories:
            details = "\n".join(f"- {name}: {count}" for name, count in categories.items())
        else:
            details = "- Aucune categorie enregistree"
        balance = "Oui" if summary["is_balanced"] else "Non"
        self.content.config(
            text=f"Equilibre alimentaire atteint: {balance}\n\nRepartition actuelle:\n{details}"
        )
