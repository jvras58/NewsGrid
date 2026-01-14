"""
Utilitários para criação e configuração de agentes LLM.
"""

from agno.agent import Agent
from agno.models.groq import Groq

from utils.settings import settings


def create_agent(
    model_id, tools=None, description="", instructions=None, markdown=False
):
    """
    Função centralizada para criar agentes LLM com configurações padronizadas.

    Args:
        model_id (str): ID do modelo LLM a ser utilizado.
        tools (list, optional): Lista de ferramentas a serem integradas ao agente. Padrão é None.
        description (str, optional): Descrição do agente. Padrão é string vazia.
        instructions (list, optional): Instruções específicas para o agente. Padrão é None.
        markdown (bool, optional): Indica se a saída deve ser formatada em Markdown. Padrão é False.

    Returns:
        Agent: Instância configurada do agente LLM.
    """

    model = Groq(id=model_id, api_key=settings.groq_api_key)
    return Agent(
        model=model,
        tools=tools,
        description=description,
        instructions=instructions,
        markdown=markdown,
    )
