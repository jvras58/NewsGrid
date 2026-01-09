"""
Configuração de logging para a aplicação.
"""

import logging
import logging.handlers
from pathlib import Path
from utils.settings import settings
import threading

_logging_configured = False
_logging_lock = threading.Lock()

def setup_logging():
    """
    Configura o sistema de logging com handlers para console e arquivo rotativo.
    """
    global _logging_configured
    # Fast path: avoid locking if já configurado.
    if _logging_configured:
        return

    # Thread-safe initialization using a lock to evitar configuração duplicada.
    with _logging_lock:
        if _logging_configured:
            return

        log_dir = Path(settings.log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger()
        logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(
            getattr(logging, settings.log_console_level.upper(), logging.INFO)
        )
        logger.addHandler(console_handler)

        file_handler = logging.handlers.RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_max_bytes,
            backupCount=settings.log_backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(
            getattr(logging, settings.log_file_level.upper(), logging.WARNING)
        )
        logger.addHandler(file_handler)

        logging.getLogger("pika").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

        _logging_configured = True
def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger com o nome especificado, configurando o logging se necessário.
    """
    setup_logging()
    return logging.getLogger(name)
