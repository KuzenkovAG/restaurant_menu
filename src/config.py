from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings."""

    model_config = SettingsConfigDict(env_file='.env')

    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_NAME: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None

    DB_USER_TEST: str | None = None
    DB_PASS_TEST: str | None = None
    DB_NAME_TEST: str | None = None
    DB_HOST_TEST: str | None = None
    DB_PORT_TEST: int | None = None

    REDIS_PASS: str | None = None
    REDIS_HOST: str | None = None
    REDIS_PORT: int | None = None

    @property
    def db_url(self) -> str:
        """Product db url."""
        return (
            f'postgresql+asyncpg://{self.DB_USER}:'
            f'{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}'
            f'/{self.DB_NAME}'
        )

    @property
    def db_test_url(self) -> str:
        """Test db url."""
        return (
            f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@'
            f'{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
        )

    @property
    def redis_url(self) -> str:
        """Redis url."""
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'


settings = Settings()
