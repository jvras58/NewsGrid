"""
Worker responsável por realizar pesquisas detalhadas sobre tópicos fornecidos.
"""

import json
from utils.broker import get_rabbitmq_connection
from utils.send_to_queue import send_to_queue
from app.agents.agent_research import ResearchAgent

research_agent = ResearchAgent()


def process_research(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Pesquisando sobre: {data['topic']}")

    try:
        response = research_agent.run(
            f"Pesquise as últimas notícias sobre: {data['topic']}"
        )

        next_stage_payload = {
            "task_id": data["task_id"],
            "topic": data["topic"],
            "raw_research": response.content,
        }

        send_to_queue("queue_analysis", next_stage_payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Pesquisa concluída e enviada para análise.")

    except Exception as e:
        print(f" [!] Erro: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue="queue_research", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="queue_research", on_message_callback=process_research)

    print(" [*] Researcher Agent esperando mensagens...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
