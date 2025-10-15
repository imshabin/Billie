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
    SECRET_KEY: str = "d8f4b5a2e1c9a8b7e0d3f2a1c6b9d8f3e2a1b5c8d7e6f4a3" # Use a real random key!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
