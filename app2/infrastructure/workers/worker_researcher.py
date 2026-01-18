"""
Worker responsável por realizar pesquisas detalhadas sobre tópicos fornecidos.
"""

import json

from app2.core.container import Container
from app2.infrastructure.agents.agent_research import ResearchAgent
from app2.infrastructure.workers.base_worker import BaseWorker
from utils.send_to_queue import send_to_queue


class ResearchWorker(BaseWorker):
    """
    Worker para pesquisa de tópicos.
    """

    def __init__(self):
        super().__init__("queue_research", ResearchAgent)
        self.container = Container()

    def process_message(self, ch, method, properties, body):
        """
        Processa mensagens da fila de pesquisa.

        Args:
            ch: Canal do RabbitMQ.
            method: Método de entrega.
            properties: Propriedades da mensagem.
            body: Corpo da mensagem (bytes).
        """
        data = json.loads(body)
        topic = data["topic"]
        task_id = data["task_id"]
        user_id = data.get("user_id")

        try:
            response = self.agent.run(f"Pesquise as últimas notícias sobre: {topic}")
            raw_research = response.content

            use_case = self.container.process_research_use_case()
            result = use_case.execute(
                task_id, topic, int(user_id) if user_id else 0, raw_research
            )

            send_to_queue("queue_analysis", result)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info(f"Pesquisa concluída para {task_id}")

        except Exception as e:
            self.container.task_status_repo().set_status(task_id, "FAILED")
            self.logger.error(f"Erro ao pesquisar {task_id}: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    worker = ResearchWorker()
    worker.run()


if __name__ == "__main__":
    main()
