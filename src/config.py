from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "repaspromo.sqlite3"
ASSETS_DIR = BASE_DIR / "assets"
HERO_IMAGE = ASSETS_DIR / "images" / "image_hero.png"
APP_TITLE = "RepasPromo"
WINDOW_SIZE = "1180x760"
