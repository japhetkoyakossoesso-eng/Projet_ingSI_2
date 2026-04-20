from tkinter import ttk

from repaspromo.ui.widgets.stats_card import StatsCard


class DashboardView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=24)
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Tableau de bord", style="Title.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w"
        )

        self.cards = {
            "total": StatsCard(self, "Contributions"),
            "quantity": StatsCard(self, "Quantites"),
            "balance": StatsCard(self, "Equilibre"),
        }
        self.cards["total"].grid(row=1, column=0, sticky="nsew", padx=(0, 12), pady=16)
        self.cards["quantity"].grid(row=1, column=1, sticky="nsew", padx=6, pady=16)
        self.cards["balance"].grid(row=1, column=2, sticky="nsew", padx=(12, 0), pady=16)

        columns = ("prenom", "nom", "categorie", "quantite")
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        for key, label in zip(columns, ("Prenom", "Nom", "Categorie", "Quantite")):
            self.table.heading(key, text=label)
            self.table.column(key, anchor="center")
        self.table.grid(row=2, column=0, columnspan=3, sticky="nsew")

    def render(self, summary: dict[str, object], contributions: list) -> None:
        self.cards["total"].set_value(str(summary["total_contributions"]))
        self.cards["quantity"].set_value(str(summary["total_quantity"]))
        self.cards["balance"].set_value("OK" if summary["is_balanced"] else "A completer")

        for item in self.table.get_children():
            self.table.delete(item)
        for contribution in contributions:
            self.table.insert(
                "",
                "end",
                values=(
                    contribution.first_name,
                    contribution.last_name,
                    contribution.category,
                    contribution.quantity,
                ),
            )
