from repaspromo.config import APP_TITLE, WINDOW_SIZE
from repaspromo.controllers.app_controller import AppController


def run() -> None:
    controller = AppController(title=APP_TITLE, geometry=WINDOW_SIZE)
    controller.run()
