class UserAlreadyExistsError(ValueError):
    """Erro para usuário já existente (HTTP 409)."""

    def __init__(self, message: str = "Usuário já existe"):
        super().__init__(message)


class InvalidCredentialsError(ValueError):
    """Erro para credenciais inválidas (HTTP 401)."""

    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message)


class BadRequestError(ValueError):
    """Erro para requisição inválida (HTTP 400)."""

    def __init__(self, message: str = "Requisição inválida"):
        super().__init__(message)
