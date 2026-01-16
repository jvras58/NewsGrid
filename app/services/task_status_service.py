"""
Serviço para gerenciamento de status de tarefas usando Redis.
"""

from utils.settings import settings
from utils.tasks_controller import (
    delete_task_status,
    get_all_task_statuses,
    get_task_status,
    set_task_status,
    task_status_exists,
)


class TaskStatusService:
    """Serviço para operações de status de tarefas."""

    @staticmethod
    def set_researching(task_id: str) -> bool:
        """Define o status da tarefa como RESEARCHING.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se bem-sucedido
        """
        return set_task_status(task_id, settings.task_status_researching)

    @staticmethod
    def set_analyzing(task_id: str) -> bool:
        """Define o status da tarefa como ANALYZING.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se bem-sucedido
        """
        return set_task_status(task_id, settings.task_status_analyzing)

    @staticmethod
    def set_completed(task_id: str) -> bool:
        """Define o status da tarefa como COMPLETED.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se bem-sucedido
        """
        return set_task_status(task_id, settings.task_status_completed)

    @staticmethod
    def set_failed(task_id: str) -> bool:
        """Define o status da tarefa como FAILED.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se bem-sucedido
        """
        return set_task_status(task_id, settings.task_status_failed)

    @staticmethod
    def get_status(task_id: str) -> [str] | None:
        """Obtém o status atual da tarefa.

        Args:
            task_id (str): ID da tarefa

        Returns:
            [str]: Status da tarefa ou None se não encontrado
        """
        return get_task_status(task_id)

    @staticmethod
    def is_researching(task_id: str) -> bool:
        """Verifica se a tarefa está em estado RESEARCHING.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se está pesquisando
        """
        status = get_task_status(task_id)
        return status == settings.task_status_researching

    @staticmethod
    def is_analyzing(task_id: str) -> bool:
        """Verifica se a tarefa está em estado ANALYZING.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se está analisando
        """
        status = get_task_status(task_id)
        return status == settings.task_status_analyzing

    @staticmethod
    def is_completed(task_id: str) -> bool:
        """Verifica se a tarefa está em estado COMPLETED.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se está completa
        """
        status = get_task_status(task_id)
        return status == settings.task_status_completed

    @staticmethod
    def is_failed(task_id: str) -> bool:
        """Verifica se a tarefa está em estado FAILED.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se falhou
        """
        status = get_task_status(task_id)
        return status == settings.task_status_failed

    @staticmethod
    def exists(task_id: str) -> bool:
        """Verifica se o status da tarefa existe.

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se existe
        """
        return task_status_exists(task_id)

    @staticmethod
    def delete(task_id: str) -> int:
        """Remove o status da tarefa.

        Args:
            task_id (str): ID da tarefa

        Returns:
            int: Número de chaves removidas
        """
        return delete_task_status(task_id)

    @staticmethod
    def get_all_statuses() -> dict[str, str]:
        """Obtém todos os status de tarefas.

        Returns:
            dict[str, str]: Dicionário com task_id: status
        """
        return get_all_task_statuses()

    @staticmethod
    def get_active_tasks() -> list[str]:
        """Obtém lista de tarefas ativas (RESEARCHING ou ANALYZING).

        Returns:
            list[str]: Lista de task_ids ativos
        """
        all_statuses = get_all_task_statuses()
        active_statuses = [
            settings.task_status_researching,
            settings.task_status_analyzing,
        ]
        return [
            task_id
            for task_id, status in all_statuses.items()
            if status in active_statuses
        ]

    @staticmethod
    def get_completed_tasks() -> list[str]:
        """Obtém lista de tarefas completadas.

        Returns:
            list[str]: Lista de task_ids completados
        """
        all_statuses = get_all_task_statuses()
        return [
            task_id
            for task_id, status in all_statuses.items()
            if status == settings.task_status_completed
        ]

    @staticmethod
    def get_failed_tasks() -> list[str]:
        """Obtém lista de tarefas que falharam.

        Returns:
            list[str]: Lista de task_ids que falharam
        """
        all_statuses = get_all_task_statuses()
        return [
            task_id
            for task_id, status in all_statuses.items()
            if status == settings.task_status_failed
        ]


# Instância global do serviço
task_status_service = TaskStatusService()
