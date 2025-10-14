
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tadmin"
    PROJECT_VERSION: str = "1.0.0"

    # 数据库配置
    DATABASE_TYPE: str = "sqlite"  # sqlite 或 postgresql
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./tadmin.db"
    POSTGRES_SERVER: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    # JWT配置
    SECRET_KEY: str = "change-this-to-a-secure-random-secret-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS配置
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:8848", "http://127.0.0.1:8848", "http://localhost:8849", "http://127.0.0.1:8849"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# 根据数据库类型设置数据库URI
settings = Settings()

if settings.DATABASE_TYPE == "postgresql":
    settings.SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    )
