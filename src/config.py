from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings."""

    model_config = SettingsConfigDict(env_file=".env")

    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None

    DB_USER_TEST: Optional[str] = None
    DB_PASS_TEST: Optional[str] = None
    DB_NAME_TEST: Optional[str] = None
    DB_HOST_TEST: Optional[str] = None
    DB_PORT_TEST: Optional[int] = None

    REDIS_PASS: Optional[str] = None
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None

    @property
    def db_url(self):
        """Product db url."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )

    @property
    def db_test_url(self):
        """Test db url."""
        return (
            f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@"
            f"{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"
        )

    @property
    def redis_url(self):
        """Redis url."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


settings = Settings()
