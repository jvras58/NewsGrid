"""
Worker responsável por realizar pesquisas detalhadas sobre tópicos fornecidos.
"""

import pika
import json
from utils.settings import settings
from app.agents.agent_research import ResearchAgent

# TODO: Refatorar para um lugar mais apropriado e deixar reutilizável

research_agent = ResearchAgent()


def process_research(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Pesquisando sobre: {data['topic']}")

    try:
        response = research_agent.run(
            f"Pesquise as últimas notícias sobre: {data['topic']}"
        )
        research_data = response.content

        next_stage_payload = {
            "task_id": data["task_id"],
            "topic": data["topic"],
            "raw_research": research_data,
        }

        send_to_next_queue("queue_analysis", next_stage_payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Pesquisa concluída e enviada para análise.")

    except Exception as e:
        print(f" [!] Erro: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def send_to_next_queue(queue_name, data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            credentials=pika.PlainCredentials(
                settings.rabbitmq_user, settings.rabbitmq_password
            ),
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange="", routing_key=queue_name, body=json.dumps(data))
    connection.close()


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost", credentials=pika.PlainCredentials("user", "password")
    )
)
channel = connection.channel()
channel.queue_declare(queue="queue_research", durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="queue_research", on_message_callback=process_research)

print(" [*] Researcher Agent esperando mensagens...")
channel.start_consuming()
