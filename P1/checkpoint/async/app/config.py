from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://username:password@postgres_async:5432/postgres_async'
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "my_dev_secret"
    log_level: str = "DEBUG"
   


settings = Settings()  