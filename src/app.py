from config import APP_TITLE, WINDOW_SIZE
from controllers.app_controller import AppController


def run() -> None:
    controller = AppController(title=APP_TITLE, geometry=WINDOW_SIZE)
    controller.run()
