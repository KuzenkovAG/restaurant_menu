from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings."""
    model_config = SettingsConfigDict(env_file='.env')

    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str
    DB_HOST_TEST: str
    DB_PORT_TEST: str

    @property
    def DB_URL(self):
        return (
            f'postgresql+asyncpg://{self.DB_USER}:'
            f'{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}'
            f'/{self.DB_NAME}'
        )

    @property
    def DB_TEST_URL(self):
        return (
            f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@'
            f'{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
        )


settings = Settings()
