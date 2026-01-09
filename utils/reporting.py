"""
Módulo utilitário para funções de geração e salvamento de relatórios.
"""

from utils.logging import get_logger

logger = get_logger("save_report")


def save_report(task_id: str, topic: str, report_content: str):
    """
    Salva o relatório gerado em um arquivo markdown.

    Args:
        task_id (str): ID da tarefa associada ao relatório.
        topic (str): Tópico do relatório.
        report_content (str): Conteúdo do relatório a ser salvo.

    Returns:
        None
    """
    filename = f"report_{task_id}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Relatório de Inteligência: {topic}\n\n")
        f.write(report_content)
    logger.info(f"Relatório salvo em: {filename}")
