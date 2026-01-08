"""
Worker responsável por analisar dados de pesquisa bruta e gerar relatórios executivos.
"""

import pika
import json
from utils.llm import create_agent

# TODO: Refatorar para um lugar mais apropriado e deixar reutilizável

analyst_agent = create_agent(
    model_id="llama-3.1-8b-instant",
    description="Você é um Analista de Mercado Sênior da XP ou BTG.",
    instructions=[
        "Seu objetivo é gerar um relatório executivo.",
        "Use tom profissional, direto e baseado em dados.",
        "Não invente fatos, use apenas o que foi fornecido na pesquisa.",
        "Formate a saída em Markdown limpo.",
    ],
    markdown=True,
)


def save_report(task_id, topic, report_content):
    filename = f"report_{task_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Relatório de Inteligência: {topic}\n\n")
        f.write(report_content)
    print(f" [V] Relatório salvo em: {filename}")


def process_analysis(ch, method, properties, body):
    data = json.loads(body)
    topic = data["topic"]
    raw_research = data["raw_research"]

    print(f" [x] Analisando dados sobre: {topic}...")

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
        print(" [x] Análise concluída e arquivada.")

    except Exception as e:
        print(f" [!] Erro na análise: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost", credentials=pika.PlainCredentials("user", "password")
    )
)
channel = connection.channel()

channel.queue_declare(queue="queue_analysis", durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="queue_analysis", on_message_callback=process_analysis)

print(" [*] Analyst Agent esperando dados para processar...")
channel.start_consuming()
