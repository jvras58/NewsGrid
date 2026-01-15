"""
Configurações da aplicação usando Pydantic Settings
"""

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
    docs_url: str | None = None
    redoc_url: str | None = None

    # Configurações do pika (RabbitMQ)
    rabbitmq_host: str = "localhost"
    rabbitmq_user: str = "user"
    rabbitmq_password: str = "password"

    # Configurações do Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    # Task Status Constants
    task_status_researching: str = "RESEARCHING"
    task_status_analyzing: str = "ANALYZING"
    task_status_completed: str = "COMPLETED"
    task_status_failed: str = "FAILED"

    # Task Status Key Pattern
    task_status_key_pattern: str = "task:{task_id}"

    # TTL for task status (24 hours in seconds)
    task_status_ttl_seconds: int = 86400

    # Configurações do banco de dados SQLAlchemy
    database_url: str = "sqlite+aiosqlite:///./app.db"
    echo_sql: bool = False

    # Configurações de segurança
    default_token: str = "12345678-1234-5678-9012-123456789012"

    # Configurações JWT
    jwt_secret_key: str = "chave-secreta-super-segura"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
