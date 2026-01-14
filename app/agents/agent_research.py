"""
Agente Pesquisador
"""

from agno.tools.bravesearch import BraveSearchTools

from utils.base_agent import BaseAgent
from utils.settings import settings


class ResearchAgent(BaseAgent):
    """
    Agente para pesquisa de tópicos com ferramentas de busca.
    """

    def __init__(self):
        """
        Inicializa o Agente Pesquisador com ferramentas de busca integradas.
        """
        super().__init__(
            model_id="llama-3.1-8b-instant",
            tools=[
                BraveSearchTools(
                    api_key=settings.brave_api_key,
                    fixed_language="pt",
                    enable_brave_search=False,
                )
            ],
            description="Você é um pesquisador sênior. Busque fatos recentes e detalhados.",
            instructions=[
                "Retorne um resumo estruturado com as 3 principais fontes encontradas."
            ],
            markdown=True,
        )

    def run(self, prompt):
        """
        Executa o agente com o prompt fornecido.

        Args:
            prompt (str): Prompt de entrada.

        Returns:
            Response: Resposta do agente.
        """
        return self.agent.run(prompt)
