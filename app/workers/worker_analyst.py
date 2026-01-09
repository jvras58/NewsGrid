"""
Worker responsável por analisar dados de pesquisa bruta e gerar relatórios executivos.
"""

import json
from app.agents.agent_analyst import AnalystAgent
from utils.broker import get_rabbitmq_connection
from utils.reporting import save_report
from utils.logging import get_logger

logger = get_logger("worker_analyst")


analyst_agent = AnalystAgent()


def process_analysis(ch, method, properties, body):
    """Processa mensagens da fila de análise

    Args:
        ch: Canal do RabbitMQ.
        method: Método de entrega da mensagem.
        properties: Propriedades da mensagem.
        body: Corpo da mensagem (dados em JSON).

    Returns:
        None
    """
    data = json.loads(body)
    topic = data["topic"]
    raw_research = data["raw_research"]

    logger.info(f"Analisando dados sobre: {topic}...")

    try:
        prompt = (
            f"Analise os seguintes dados brutos coletados sobre '{topic}':\n\n"
            f"{raw_research}\n\n"
            "--- FIM DOS DADOS ---\n"
            "Crie um relatório com: 1. Resumo Executivo, 2. Principais Pontos, 3. Conclusão."
        )

        response = analyst_agent.run(prompt)
        final_report = response.content

        save_report(data["task_id"], topic, final_report)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Análise concluída e arquivada.")

    except Exception as e:
        logger.error(
            f"Erro na análise de '{topic}' (task_id: {data.get('task_id')}): {e}"
        )
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue="queue_analysis", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue="queue_analysis", on_message_callback=process_analysis)

    logger.info("Analyst Agent esperando dados para processar...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
