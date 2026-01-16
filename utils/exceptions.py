"""
Exceções de domínio para o NewsGrid.

Este módulo define exceções específicas do domínio para melhorar
o tratamento de erros e a manutenibilidade do código.
"""


class DomainException(Exception):
    """
    Exceção base do domínio.

    Todas as exceções específicas do domínio devem herdar desta classe.
    Fornece estrutura padronizada com mensagem e código de erro.
    """

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)


# =============================================================================
# Exceções de Usuário/Autenticação
# =============================================================================


class UserAlreadyExistsError(DomainException):
    """Erro para usuário já existente (HTTP 409)."""

    def __init__(self, message: str = "Usuário já existe"):
        super().__init__(message=message, code="USER_ALREADY_EXISTS")


class InvalidCredentialsError(DomainException):
    """Erro para credenciais inválidas (HTTP 401)."""

    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message=message, code="INVALID_CREDENTIALS")


class UnauthorizedAccessError(DomainException):
    """Erro para acesso não autorizado a um recurso (HTTP 403)."""

    def __init__(self, resource: str, user_id: int | None = None):
        if user_id:
            message = f"Usuário {user_id} não tem acesso a {resource}"
        else:
            message = f"Acesso não autorizado a {resource}"
        super().__init__(message=message, code="UNAUTHORIZED_ACCESS")


# =============================================================================
# Exceções de Relatório
# =============================================================================


class ReportNotFoundError(DomainException):
    """Erro para relatório não encontrado (HTTP 404)."""

    def __init__(self, task_id: str):
        super().__init__(
            message=f"Relatório não encontrado: {task_id}",
            code="REPORT_NOT_FOUND",
        )


class ReportCreationError(DomainException):
    """Erro ao criar relatório (HTTP 500)."""

    def __init__(self, task_id: str, reason: str = "Erro desconhecido"):
        super().__init__(
            message=f"Erro ao criar relatório {task_id}: {reason}",
            code="REPORT_CREATION_ERROR",
        )


# =============================================================================
# Exceções de Tarefa/Worker
# =============================================================================


class TaskNotFoundError(DomainException):
    """Erro para tarefa não encontrada (HTTP 404)."""

    def __init__(self, task_id: str):
        super().__init__(
            message=f"Tarefa não encontrada: {task_id}",
            code="TASK_NOT_FOUND",
        )


class TaskProcessingError(DomainException):
    """Erro ao processar tarefa (HTTP 500)."""

    def __init__(self, task_id: str, stage: str, reason: str = "Erro desconhecido"):
        super().__init__(
            message=f"Erro ao processar tarefa {task_id} na etapa '{stage}': {reason}",
            code="TASK_PROCESSING_ERROR",
        )


# =============================================================================
# Exceções de Requisição
# =============================================================================


class BadRequestError(DomainException):
    """Erro para requisição inválida (HTTP 400)."""

    def __init__(self, message: str = "Requisição inválida"):
        super().__init__(message=message, code="BAD_REQUEST")


class ValidationError(DomainException):
    """Erro de validação de dados (HTTP 422)."""

    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Erro de validação no campo '{field}': {reason}",
            code="VALIDATION_ERROR",
        )


# =============================================================================
# Exceções de Infraestrutura
# =============================================================================


class QueueConnectionError(DomainException):
    """Erro de conexão com a fila de mensagens."""

    def __init__(self, queue_name: str, reason: str = "Falha na conexão"):
        super().__init__(
            message=f"Erro ao conectar na fila '{queue_name}': {reason}",
            code="QUEUE_CONNECTION_ERROR",
        )


class CacheError(DomainException):
    """Erro de operação no cache."""

    def __init__(self, operation: str, reason: str = "Erro desconhecido"):
        super().__init__(
            message=f"Erro no cache durante '{operation}': {reason}",
            code="CACHE_ERROR",
        )
