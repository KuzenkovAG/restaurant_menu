from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings."""
    model_config = SettingsConfigDict(env_file='.env')

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: str

    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str

    @property
    def DB_URL(self):
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}'
            f'/{self.POSTGRES_DB}'
        )

    @property
    def DB_TEST_URL(self):
        return (
            f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@'
            f'{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
        )


settings = Settings()
