from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_server: str = Field(default=r".\SQLEXPRESS")
    db_name: str = Field(default="shoplite")
    db_user: str = Field(default="sa")
    db_password: str = Field(default="dss")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
