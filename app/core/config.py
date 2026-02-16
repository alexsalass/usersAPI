from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "devdb"
    DB_USER: str = "dev"
    DB_PASSWORD: str = "dev123"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
