from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Resume Job Hunter"
    environment: str = "local"
    frontend_origin: str = "http://localhost:5173"
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/resume_jobs"

    openai_api_key: str = Field(default="", repr=False)
    openai_model: str = "gpt-4.1"

    adzuna_app_id: str = ""
    adzuna_app_key: str = Field(default="", repr=False)
    greenhouse_companies: str = "browserstack,freshworks,razorpay,swiggy,thoughtworks"
    lever_companies: str = "atlan,gojek,postman,cred,meesho"

    google_service_account_json: str = Field(default="", repr=False)
    google_drive_folder_id: str = ""

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = Field(default="", repr=False)
    smtp_from_email: str = ""

    max_upload_mb: int = 8
    rate_limit_per_minute: int = 20
    request_timeout_seconds: int = 25
    daily_refresh_hour_utc: int = 2

    @field_validator("frontend_origin")
    @classmethod
    def normalize_origin(cls, value: str) -> str:
        return value.rstrip("/")

    @property
    def greenhouse_company_list(self) -> List[str]:
        return [item.strip() for item in self.greenhouse_companies.split(",") if item.strip()]

    @property
    def lever_company_list(self) -> List[str]:
        return [item.strip() for item in self.lever_companies.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
