
import json
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Django(BaseModel):
    secret_key: str
    allowed_hosts: list[str]
    public_host: str


class Database(BaseModel):
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: int


class Redis(BaseModel):
    host: str
    port: int


class JWT(BaseModel):
    access_lifetime: int
    refresh_lifetime: int


class Admin(BaseModel):
    name: str
    email: str
    password: str


class Celery(BaseModel):
    workers: int


class EmailAccount(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str
    use_tls: bool = True
    use_ssl: bool = False


class Settings(BaseSettings):
    name: str
    version: str
    timezone: str
    django: Django
    jwt: JWT
    redis: Redis
    celery: Celery
    database: Database
    admin: Admin
    emails: list[EmailAccount]

    model_config = SettingsConfigDict(
        extra="forbid",
        case_sensitive=True
    )

    @classmethod
    def settings_customise_sources(
        cls, settings_cls, init_settings,
        env_settings, file_secret_settings,
        dotenv_settings
    ):
        def json_config_settings():
            with open("env.json", encoding="utf-8") as f:
                return json.load(f)

        return (
            init_settings,
            json_config_settings,
            env_settings,
            file_secret_settings,
        )


@lru_cache(maxsize=1)
def get_config() -> Settings:
    return Settings()
