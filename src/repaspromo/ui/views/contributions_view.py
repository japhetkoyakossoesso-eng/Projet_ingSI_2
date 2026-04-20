import tkinter as tk
from tkinter import ttk

from repaspromo.core.validators import CATEGORIES


class ContributionsView(ttk.Frame):
    def __init__(self, parent, on_submit) -> None:
        super().__init__(parent, padding=24)
        self.on_submit = on_submit

        ttk.Label(self, text="Ajouter une contribution", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.category_var = tk.StringVar(value=CATEGORIES[0])
        self.quantity_var = tk.StringVar()

        fields = (
            ("Prenom", self.first_name_var),
            ("Nom", self.last_name_var),
            ("Quantite", self.quantity_var),
        )

        for row, (label, variable) in enumerate(fields, start=1):
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", pady=8)
            ttk.Entry(self, textvariable=variable, width=40).grid(row=row, column=1, sticky="ew", pady=8)

        ttk.Label(self, text="Categorie").grid(row=4, column=0, sticky="w", pady=8)
        ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=CATEGORIES,
            state="readonly",
            width=37,
        ).grid(row=4, column=1, sticky="ew", pady=8)

        ttk.Button(self, text="Enregistrer", command=self.submit).grid(row=5, column=1, sticky="e", pady=(16, 0))
        self.columnconfigure(1, weight=1)

    def submit(self) -> None:
        payload = {
            "first_name": self.first_name_var.get(),
            "last_name": self.last_name_var.get(),
            "category": self.category_var.get(),
            "quantity": self.quantity_var.get(),
        }
        self.on_submit(payload)

    def reset_form(self) -> None:
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.category_var.set(CATEGORIES[0])
        self.quantity_var.set("")
