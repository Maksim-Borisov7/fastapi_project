import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path
from pydantic_settings import BaseSettings

load_dotenv()

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")
PORT = os.getenv("PORT")
PG_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_COOKIE_NAME = os.getenv("ACCESS_TOKEN_COOKIE_NAME")
IS_SUPER_ADMIN_PASSWORD = os.getenv("IS_SUPER_ADMIN_PASSWORD")

BASE_DIR = Path(__file__).parent


class DbSettings(BaseModel):
    url: str = PG_URL
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
