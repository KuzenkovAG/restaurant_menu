from pathlib import Path

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

    RABBIT_USER: str | None = None
    RABBIT_PASS: str | None = None
    RABBIT_HOST: str | None = None

    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)

    # Celery db update settings
    DB_UPDATE_PERIOD_IN_SECONDS: int = 15
    ADMIN_EXCEL_PATH: str = BASE_DIR + '/src/admin/Menu.xlsx'
    GOOGLE_SHEET_ID: str = '1Fk0z7zcl8A5ugGeoZ-DKi9vB_j9XUQyBUSo2sz3W0DA'
    ADMIN_GOOGLE_SHEET: str = (
        f'https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=xlsx&id={GOOGLE_SHEET_ID}'
    )
    FROM_GOOGLE_SHEETS: bool = True

    # discount
    DEFAULT_DISCOUNT: int = 0

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

    @property
    def rabbit_url(self) -> str:
        """Rabbit url."""
        return f'amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}@{self.RABBIT_HOST}//'


settings = Settings()
