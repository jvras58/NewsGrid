"""
Utilitários para criação e configuração de agentes LLM.
"""

from agno.agent import Agent
from utils.settings import settings
from agno.models.groq import Groq


def create_agent(
    model_id, tools=None, description="", instructions=None, markdown=False
):
    """
    Função centralizada para criar agentes LLM com configurações padronizadas.
    """

    model = Groq(id=model_id, api_key=settings.groq_api_key)
    return Agent(
        model=model,
        tools=tools,
        description=description,
        instructions=instructions,
        markdown=markdown,
    )
