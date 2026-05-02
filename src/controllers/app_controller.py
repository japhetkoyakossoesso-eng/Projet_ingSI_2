import tkinter as tk
from tkinter import messagebox

from config import DATA_FILE
from core import ContributionRepository, MealNotFoundError, MealService
from ui.theme import configure_theme
from ui.views.dashboard import DashboardView
from ui.views.home import HomeView
from ui.views.meal_create import MealCreateView
from ui.views.meal_list import MealListView
from ui.views.organisation import OrganisationView


class AppController:
    def __init__(self, title: str, geometry: str) -> None:
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.minsize(1024, 520)

        configure_theme(self.root)

        self.repository = ContributionRepository(DATA_FILE)
        self.service = MealService(self.repository)
        self.current_meal_id: int | None = None
        self.current_view: tk.Frame | None = None

        self.show_home()

    def run(self) -> None:
        self.root.mainloop()

    def _mount(self, view_class, *args) -> None:
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = view_class(self.root, self, *args)
        self.current_view.pack(fill="both", expand=True)

    def show_home(self) -> None:
        self.current_meal_id = None
        self._mount(HomeView)

    def show_meal_list(self) -> None:
        self._mount(MealListView)

    def show_meal_create(self) -> None:
        self._mount(MealCreateView)

    def show_organisation(self, meal_id: int) -> None:
        try:
            self.service.get_meal(meal_id)
        except MealNotFoundError:
            messagebox.showerror("Repas introuvable", "Le repas demandé n'existe plus.")
            self.current_meal_id = None
            self.show_meal_list()
            return
        self.current_meal_id = meal_id
        self._mount(OrganisationView, meal_id)

    def show_dashboard(self, meal_id: int | None = None) -> None:
        target_id = meal_id if meal_id is not None else self.current_meal_id
        if target_id is None:
            messagebox.showinfo("Tableau de bord", "Sélectionne d'abord un repas.")
            self.show_meal_list()
            return
        try:
            self.service.get_meal(target_id)
        except MealNotFoundError:
            messagebox.showerror("Repas introuvable", "Le repas demandé n'existe plus.")
            self.current_meal_id = None
            self.show_meal_list()
            return
        self.current_meal_id = target_id
        self._mount(DashboardView, target_id)
