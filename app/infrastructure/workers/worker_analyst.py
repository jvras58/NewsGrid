"""
Worker responsável por analisar dados de pesquisa bruta e gerar relatórios executivos.
"""

import asyncio
import json

from app.core.container import Container
from app.core.database import async_session
from app.infrastructure.agents.agent_analyst import AnalystAgent
from app.infrastructure.workers.base_worker import BaseWorker


class AnalystWorker(BaseWorker):
    """
    Worker para análise de dados e geração de relatórios.
    """

    def __init__(self):
        super().__init__("queue_analysis", AnalystAgent)
        self.container = Container()

    def process_message(self, ch, method, properties, body):
        """
        Processa mensagens da fila de análise.

        Args:
            ch: Canal do RabbitMQ.
            method: Método de entrega.
            properties: Propriedades da mensagem.
            body: Corpo da mensagem (bytes).
        """
        data = json.loads(body)
        topic = data["topic"]
        raw_research = data["raw_research"]
        task_id = data["task_id"]
        user_id = int(data.get("user_id", 0))

        async def process():
            try:
                prompt = (
                    f"Analise os seguintes dados brutos coletados sobre '{topic}':\n\n"
                    f"{raw_research}\n\n"
                    "--- FIM DOS DADOS ---\n"
                    "Crie um relatório com: 1. Resumo Executivo, 2. Principais Pontos, 3. Conclusão."
                )
                response = self.agent.run(prompt)
                final_report = response.content

                use_case = self.container.process_analysis_use_case()
                async with async_session() as session:
                    await use_case.execute(
                        session, task_id, topic, raw_research, user_id, final_report
                    )

                ch.basic_ack(delivery_tag=method.delivery_tag)
                self.logger.info(f"Análise concluída para {task_id}")

            except Exception as e:
                self.container.task_status_repo().set_status(task_id, "FAILED")
                self.logger.error(f"Erro na análise {task_id}: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        asyncio.run(process())


def main():
    worker = AnalystWorker()
    worker.run()


if __name__ == "__main__":
    main()
