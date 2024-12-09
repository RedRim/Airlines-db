from authx import AuthX, AuthXConfig
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

DATABASE_CONFIG = {
    "dbname": "airlines",
    "user": "psgs_admin",
    "password": "pg_admin_pass_1257",
    "host": "localhost",
    "port": 5432,
}

class Settings:
    app_name: str = 'Best Airlines app'
    debug: bool = True
    static_url: str = '/static'
    static_dir: Path = Path(__file__).parent / 'static'

settings = Settings()

templates = Jinja2Templates(directory="templates")