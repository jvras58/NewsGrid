"""
Worker responsável por realizar pesquisas detalhadas sobre tópicos fornecidos.
"""

import json
from utils.base_worker import BaseWorker
from utils.send_to_queue import send_to_queue
from app.agents.agent_research import ResearchAgent


class ResearchWorker(BaseWorker):
    """
    Worker para pesquisa de tópicos.
    """

    def __init__(self):
        super().__init__("queue_research", ResearchAgent)

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

        self.logger.info(f"Pesquisando sobre: {topic}")

        try:
            response = self.agent.run(f"Pesquise as últimas notícias sobre: {topic}")

            next_stage_payload = {
                "task_id": task_id,
                "topic": topic,
                "raw_research": response.content,
            }

            send_to_queue("queue_analysis", next_stage_payload)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info("Pesquisa concluída e enviada para análise.")

        except Exception as e:
            self.logger.error(
                f"Erro ao pesquisar tópico '{topic}' (task_id: {task_id}): {e}"
            )
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":
    worker = ResearchWorker()
    worker.run()
