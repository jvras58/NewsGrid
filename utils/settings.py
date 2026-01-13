"""
Configurações da aplicação usando Pydantic Settings
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas do .env

    Args:
        None
    Returns:
        None
    """

    # Configurações de API Keys
    groq_api_key: str
    brave_api_key: str

    # Configurações da API
    api_title: str = "Agno Agent API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Configurações de logging e níveis específicos por handler
    log_level: str = "INFO"

    log_file: str = "logs/app.log"
    log_max_bytes: int = 10485760
    log_backup_count: int = 5
    log_console_level: str = "INFO"
    log_file_level: str = "WARNING"

    # Configurações opcionais
    debug: bool = False
    cors_origins: list[str] = ["*"]
    docs_url: Optional[str] = None
    redoc_url: Optional[str] = None

    # Configurações do pika (RabbitMQ)
    rabbitmq_host: str = "localhost"
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"

    # Configurações do Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Configurações de segurança
    secure_cookies: bool = False
    default_token: str = "12345678-1234-5678-9012-123456789012"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
