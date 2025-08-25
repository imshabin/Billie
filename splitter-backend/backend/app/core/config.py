from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    app_port: int = 8080
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    redis_host: str
    redis_port: int
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
