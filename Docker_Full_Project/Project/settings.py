

import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """class for configuration settings"""

    model_config = SettingsConfigDict(
        env_file=os.getenv("env_file", "../.env.local"), env_file_encoding="utf-8"
    )
    APP_NAME: str
    HOST: str
    PORT: int
    DB_URL: str
    DB_NAME: str
    RELOAD: bool
    DRIVER_PATH: Path
    DATA_TRANSFORM_PATH: Path


settings = Settings()
