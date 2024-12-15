from authx import AuthX, AuthXConfig
from fastapi.templating import Jinja2Templates
from pathlib import Path

class Settings:
    app_name: str = 'Best Airlines app'
    debug: bool = True
    # static_url: str = '/static'
    # static_dir: Path = Path(__file__).parent / 'static'

settings = Settings()


DATABASE_CONFIG = {
    "dbname": "airlines",
    "user": "psgs_admin",
    "password": "pg_admin_pass_1257",
    "host": "localhost",
    "port": 5432,
}

config = AuthXConfig()
config.JWT_SECRET_KEY = 'secret_key'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

templates = Jinja2Templates(directory="templates")