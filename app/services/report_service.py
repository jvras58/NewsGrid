"""Serviço para manipulação de relatórios no Redis."""

import json
from typing import Optional
from utils.redis_client import get_redis_client
from utils.logging import get_logger

logger = get_logger("report_service")


class ReportService:
    @staticmethod
    def save(task_id: str, topic: str, content: str, user_id: Optional[str] = None):
        """
        Salva um relatório no Redis com o ID da tarefa, tópico, conteúdo e ID do usuário opcional fornecidos.

        Este método armazena os dados do relatório no Redis usando uma chave baseada no ID da tarefa. Se um ID de usuário for fornecido,
        o relatório também é associado a esse usuário adicionando o ID da tarefa ao conjunto de relatórios do usuário. Os dados do relatório
        são definidos para expirar após 24 horas (86400 segundos).

        Args:
            task_id (str): O identificador único para a tarefa/relatório. Deve ser uma string não vazia.
            topic (str): O tópico do relatório. Deve ser uma string não vazia.
            content (str): O conteúdo do relatório. Deve ser uma string não vazia.
            user_id (Optional[str]): O ID do usuário que possui o relatório. Se fornecido, deve ser uma string não vazia.
                Se None, o relatório não é associado a nenhum usuário.

        Raises:
            ValueError: Se task_id, topic ou content não forem strings não vazias, ou se user_id for fornecido mas vazio,
                ou se ocorrer um erro durante o salvamento no Redis.
        """
        if not task_id or not isinstance(task_id, str):
            raise ValueError("task_id deve ser uma string não vazia")
        if not topic or not isinstance(topic, str):
            raise ValueError("topic deve ser uma string não vazia")
        if not content or not isinstance(content, str):
            raise ValueError("content deve ser uma string não vazia")
        if user_id is not None and not user_id.strip():
            raise ValueError("user_id deve ser uma string não vazia ou None")

        redis = get_redis_client()
        key = f"report:{task_id}"

        data = {
            "task_id": task_id,
            "topic": topic,
            "content": content,
            "owner": user_id,
        }

        try:
            pipeline = redis.pipeline()
            pipeline.set(key, json.dumps(data), ex=86400)

            if user_id:
                pipeline.sadd(f"user:{user_id}:reports", task_id)

            pipeline.execute()
            logger.info(f"Relatório {task_id} salvo para {user_id}")
        except Exception as e:
            logger.exception(f"Erro ao salvar relatório {task_id}")
            raise ValueError(f"Erro ao salvar relatório: {e}") from e

    @staticmethod
    def get_by_id(task_id: str, user_id: Optional[str] = None):
        """
        Recupera um relatório pelo seu ID de tarefa, aplicando controle de acesso baseado na propriedade do usuário.

        Este método busca os dados do relatório no Redis. Se o relatório tiver um proprietário (user_id), verifica se o
        usuário solicitante corresponde ao proprietário ou se nenhum usuário é especificado (embora o acesso seja negado nesse caso).
        Usado pela API para exibir detalhes do relatório.

        Args:
            task_id (str): O identificador único para a tarefa/relatório. Deve ser uma string não vazia.
            user_id (Optional[str]): O ID do usuário solicitando o relatório. Se o relatório for de propriedade, este deve
                corresponder ao proprietário. Se None e o relatório for de propriedade, o acesso é negado.

        Returns:
            dict: Um dicionário contendo os dados do relatório com chaves 'task_id', 'topic', 'content' e 'owner'.

        Raises:
            ValueError: Se task_id for inválido, o relatório não for encontrado ou o acesso for negado devido à propriedade.
        """
        if not task_id or not isinstance(task_id, str):
            raise ValueError("task_id deve ser uma string não vazia")
        if user_id is not None and not user_id.strip():
            raise ValueError("user_id deve ser uma string não vazia ou None")

        redis = get_redis_client()
        data = redis.get(f"report:{task_id}")

        if not data:
            raise ValueError("Relatório não encontrado")

        report = json.loads(data)

        if report.get("owner"):
            if not user_id:
                logger.warning(
                    f"Acesso negado: Usuário não autenticado tentou ler relatório de {report.get('owner')}"
                )
                raise ValueError("Acesso negado ao relatório")
            elif report.get("owner") != user_id:
                logger.warning(
                    f"Acesso negado: User {user_id} tentou ler report de {report.get('owner')}"
                )
                raise ValueError("Acesso negado ao relatório")

        return report

    @staticmethod
    def list_by_user(user_id: str):
        """
        Lista todos os IDs de relatórios associados a um determinado usuário.

        Este método recupera o conjunto de IDs de relatórios do Redis que estão vinculados ao usuário especificado. Usado pela
        API para listar relatórios de um usuário.

        Args:
            user_id (str): O ID do usuário cujos relatórios listar. Deve ser uma string não vazia.

        Returns:
            list: Uma lista de strings, cada uma sendo um ID de relatório associado ao usuário.

        Raises:
            ValueError: Se user_id não for uma string não vazia.
        """
        if not user_id or not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id deve ser uma string não vazia")

        redis = get_redis_client()
        report_ids = redis.smembers(f"user:{user_id}:reports")
        return [rid.decode("utf-8") for rid in report_ids]
