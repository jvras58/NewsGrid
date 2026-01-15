"""
Worker responsável por analisar dados de pesquisa bruta e gerar relatórios executivos.
"""

import asyncio
import json

from app.agents.agent_analyst import AnalystAgent
from app.core.database import async_session
from app.services.report_service_sql import ReportServiceSQL
from app.services.task_status_service import task_status_service
from utils.base_worker import BaseWorker


class AnalystWorker(BaseWorker):
    """
    Worker para análise de dados e geração de relatórios.
    """

    def __init__(self):
        super().__init__("queue_analysis", AnalystAgent)

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

        user_id = data.get("user_id")

        try:
            task_status_service.set_analyzing(task_id)
            self.logger.info(f"Analisando dados sobre: {topic}...")

            prompt = (
                f"Analise os seguintes dados brutos coletados sobre '{topic}':\n\n"
                f"{raw_research}\n\n"
                "--- FIM DOS DADOS ---\n"
                "Crie um relatório com: 1. Resumo Executivo, 2. Principais Pontos, 3. Conclusão."
            )

            response = self.agent.run(prompt)
            final_report = response.content

            async def save_report():
                async with async_session() as session:
                    await ReportServiceSQL.create_report(
                        session,
                        task_id,
                        int(user_id) if user_id else None,
                        topic,
                        final_report,
                    )

            asyncio.run(save_report())
            task_status_service.set_completed(task_id)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info("Análise concluída e salva no Postgres.")

        except Exception as e:
            task_status_service.set_failed(task_id)
            self.logger.error(f"Erro na análise de '{topic}' (task_id: {task_id}): {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    worker = AnalystWorker()
    worker.run()


if __name__ == "__main__":
    main()
