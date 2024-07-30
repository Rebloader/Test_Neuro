from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    FILE_PATH: str
    MAX_CHUNK_SIZE: int

    class Config:
        env_file: str = f'{BASE_DIR}/.env'


settings = Settings()
