"""
Módulo utilitário para funções de geração e salvamento de relatórios.
"""


def save_report(task_id: str, topic: str, report_content: str):
    """
    Salva o relatório gerado em um arquivo markdown.
    """
    filename = f"report_{task_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Relatório de Inteligência: {topic}\n\n")
        f.write(report_content)
    print(f" [V] Relatório salvo em: {filename}")
