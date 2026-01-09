"""
Agente Pesquisador
"""

from agno.tools.bravesearch import BraveSearchTools
from utils.settings import settings
from utils.llm import create_agent


class ResearchAgent:
    def __init__(self):
        self.agent = create_agent(
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
        return self.agent.run(prompt)
