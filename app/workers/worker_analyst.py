"""
Worker responsável por analisar dados de pesquisa bruta e gerar relatórios executivos.
"""

import json
from utils.base_worker import BaseWorker
from utils.reporting import save_report
from app.agents.agent_analyst import AnalystAgent


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

        self.logger.info(f"Analisando dados sobre: {topic}...")

        try:
            prompt = (
                f"Analise os seguintes dados brutos coletados sobre '{topic}':\n\n"
                f"{raw_research}\n\n"
                "--- FIM DOS DADOS ---\n"
                "Crie um relatório com: 1. Resumo Executivo, 2. Principais Pontos, 3. Conclusão."
            )

            response = self.agent.run(prompt)
            final_report = response.content

            save_report(task_id, topic, final_report)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info("Análise concluída e arquivada.")

        except Exception as e:
            self.logger.error(f"Erro na análise de '{topic}' (task_id: {task_id}): {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":
    worker = AnalystWorker()
    worker.run()
