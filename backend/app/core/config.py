
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_STR: str = "sqlite:///db.sqlite3"


settings = Settings()
