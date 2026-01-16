"""
Interfaces (Protocols) para repositórios do NewsGrid.

Este módulo define os contratos que os repositórios devem implementar,
permitindo desacoplamento e facilitando testes com mocks.
"""

from typing import Protocol

from app.models import Report


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
