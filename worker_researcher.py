import pika
import json
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from llm import create_agent

load_dotenv()

research_agent = create_agent(
    model_id="llama-3.1-8b-instant",
    tools=[DuckDuckGoTools()],
    description="Você é um pesquisador sênior. Busque fatos recentes e detalhados.",
    instructions=[
        "Retorne um resumo estruturado com as 3 principais fontes encontradas."
    ],
    markdown=True,
)


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
            host="localhost", credentials=pika.PlainCredentials("user", "password")
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
