"""
Configurações da aplicação usando Pydantic Settings
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas do .env
    """

    # Configurações de API Keys
    groq_api_key: str
    brave_api_key: str

    # Configurações da API
    api_title: str = "Agno Agent API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    log_level: str = "INFO"

    # Configurações opcionais
    debug: bool = False
    cors_origins: list[str] = ["*"]
    docs_url: Optional[str] = None
    redoc_url: Optional[str] = None

    # Configurações do pika (RabbitMQ)
    rabbitmq_host: str = "localhost"
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
