"""
Interfaces (Protocols) para repositórios do NewsGrid.

Este módulo define os contratos que os repositórios devem implementar,
permitindo desacoplamento e facilitando testes com mocks.
"""

from typing import Protocol

from app.models import Report, User


class ReportRepository(Protocol):
    """
    Interface para repositório de relatórios.

    Define o contrato que qualquer implementação de repositório
    de relatórios deve seguir.
    """

    async def create(
        self,
        task_id: str,
        user_id: int,
        topic: str,
        content: str | None = None,
    ) -> dict:
        """
        Cria um novo relatório.

        Args:
            task_id: ID único da tarefa.
            user_id: ID do usuário owner.
            topic: Tópico do relatório.
            content: Conteúdo do relatório (opcional).

        Returns:
            dict: {'status': 'created', 'report_id': int}
        """
        ...

    async def get_by_task_id(self, task_id: str) -> Report | None:
        """
        Busca relatório por task_id.

        Args:
            task_id: ID da tarefa.

        Returns:
            Report ou None se não encontrado.
        """
        ...

    async def list_by_user(
        self,
        user_id: int,
        topic_filter: str | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> tuple[list[Report], int]:
        """
        Lista relatórios de um usuário com filtros e paginação.

        Args:
            user_id: ID do usuário.
            topic_filter: Filtro por tópico (opcional).
            page: Número da página (1-based).
            per_page: Itens por página.

        Returns:
            Tupla com lista de relatórios e total de itens.
        """
        ...


class UserRepository(Protocol):
    """
    Interface para repositório de usuários.

    Define o contrato que qualquer implementação de repositório
    de usuários deve seguir.
    """

    async def create(
        self,
        username: str,
        email: str,
        password: str,
    ) -> dict:
        """
        Cria um novo usuário.

        Args:
            username: Nome de usuário único.
            email: Email único.
            password: Senha em plain text.

        Returns:
            dict: {'status': 'created', 'user_id': int}
        """
        ...

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Busca usuário por ID.

        Args:
            user_id: ID do usuário.

        Returns:
            User ou None se não encontrado.
        """
        ...

    async def get_by_username(self, username: str) -> User | None:
        """
        Busca usuário por username.

        Args:
            username: Nome de usuário.

        Returns:
            User ou None se não encontrado.
        """
        ...

    async def get_by_email(self, email: str) -> User | None:
        """
        Busca usuário por email.

        Args:
            email: Email do usuário.

        Returns:
            User ou None se não encontrado.
        """
        ...

    async def list_usernames(self) -> list[str]:
        """
        Lista todos os usernames.

        Returns:
            Lista de usernames.
        """
        ...


class TaskStatusRepository(Protocol):
    """
    Interface para repositório de status de tarefas.

    Define o contrato para gerenciamento de status de tarefas,
    tipicamente usando Redis ou outro armazenamento em memória.
    """

    def set_status(self, task_id: str, status: str) -> bool:
        """
        Define o status de uma tarefa.

        Args:
            task_id: ID da tarefa.
            status: Status a ser definido.

        Returns:
            True se bem-sucedido.
        """
        ...

    def get_status(self, task_id: str) -> str | None:
        """
        Obtém o status de uma tarefa.

        Args:
            task_id: ID da tarefa.

        Returns:
            Status da tarefa ou None se não encontrado.
        """
        ...

    def exists(self, task_id: str) -> bool:
        """
        Verifica se o status de uma tarefa existe.

        Args:
            task_id: ID da tarefa.

        Returns:
            True se existe.
        """
        ...

    def delete(self, task_id: str) -> int:
        """
        Remove o status de uma tarefa.

        Args:
            task_id: ID da tarefa.

        Returns:
            Número de chaves removidas.
        """
        ...
