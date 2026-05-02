"""Pages de l'application."""

from .dashboard import DashboardView
from .home import HomeView
from .meal_create import MealCreateView
from .meal_list import MealListView
from .organisation import OrganisationView

__all__ = [
    "DashboardView",
    "HomeView",
    "MealCreateView",
    "MealListView",
    "OrganisationView",
]
