import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path
from typing import ClassVar

load_dotenv()


class Settings(BaseModel):
    HOST: str = os.getenv("HOST")
    USER: str = os.getenv("USER")
    PASSWORD: str = os.getenv("PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    PORT: str = os.getenv("PORT")
    PG_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_COOKIE_NAME: str = os.getenv("ACCESS_TOKEN_COOKIE_NAME")
    IS_SUPER_ADMIN_PASSWORD: str = os.getenv("IS_SUPER_ADMIN_PASSWORD")
    BASE_DIR: ClassVar[Path] = Path(__file__).parent

    url: str = PG_URL
    echo: bool = False

    private_key_path: Path = BASE_DIR / "certs" / "private.key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


settings = Settings()
