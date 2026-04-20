import tkinter as tk
from tkinter import messagebox, ttk

from repaspromo.core.repository import ContributionRepository
from repaspromo.core.services import ContributionService
from repaspromo.ui.theme import configure_theme
from repaspromo.ui.views.contributions_view import ContributionsView
from repaspromo.ui.views.dashboard_view import DashboardView
from repaspromo.ui.views.home_view import HomeView
from repaspromo.ui.views.planning_view import PlanningView


class AppController:
    def __init__(self, title: str, geometry: str) -> None:
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.minsize(960, 600)

        configure_theme(self.root)

        repository = ContributionRepository()
        self.service = ContributionService(repository)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=16)

        self.home_view = HomeView(self.notebook, on_refresh=self.refresh_views)
        self.dashboard_view = DashboardView(self.notebook)
        self.contributions_view = ContributionsView(
            self.notebook,
            on_submit=self.handle_add_contribution,
        )
        self.planning_view = PlanningView(self.notebook)

        self.notebook.add(self.home_view, text="Accueil")
        self.notebook.add(self.dashboard_view, text="Tableau de bord")
        self.notebook.add(self.contributions_view, text="Contributions")
        self.notebook.add(self.planning_view, text="Organisation")

        self.refresh_views()

    def handle_add_contribution(self, payload: dict[str, str]) -> None:
        try:
            self.service.add_contribution(
                first_name=payload["first_name"],
                last_name=payload["last_name"],
                category=payload["category"],
                quantity=payload["quantity"],
            )
        except ValueError as exc:
            messagebox.showerror("Saisie invalide", str(exc), parent=self.root)
            return

        messagebox.showinfo(
            "Contribution ajoutée",
            "La promesse d'apport a été enregistrée.",
            parent=self.root,
        )
        self.contributions_view.reset_form()
        self.refresh_views()
        self.notebook.select(self.dashboard_view)

    def refresh_views(self) -> None:
        contributions = self.service.list_contributions()
        summary = self.service.get_summary()
        self.home_view.render(summary)
        self.dashboard_view.render(summary, contributions)
        self.planning_view.render(summary)

    def run(self) -> None:
        self.root.mainloop()
