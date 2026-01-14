"""
Classe base para agentes que usam create_agent.
"""

from abc import ABC, abstractmethod

from utils.llm import create_agent


class BaseAgent(ABC):
    """
    Classe base para agentes. Encapsula a criação do agente via create_agent.
    """

    def __init__(
        self,
        model_id: str,
        description: str,
        instructions: list,
        tools=None,
        markdown: bool = False,
    ):
        """
        Inicializa o agente base.

        Args:
            model_id (str): ID do modelo LLM.
            description (str): Descrição do agente.
            instructions (list): Lista de instruções.
            tools: Ferramentas opcionais (ex.: BraveSearchTools).
            markdown (bool): Se deve usar Markdown na saída.
        """
        self.agent = create_agent(
            model_id=model_id,
            description=description,
            instructions=instructions,
            tools=tools,
            markdown=markdown,
        )

    @abstractmethod
    def run(self, prompt: str):
        """
        Executa o agente com o prompt fornecido.

        Args:
            prompt (str): Prompt de entrada.

        Returns:
            Response: Resposta do agente.
        """
        pass
