"""
Agente Analista de Mercado
"""

from app.infrastructure.agents.base_agent import BaseAgent


class AnalystAgent(BaseAgent):
    """
    Agente para análise de mercado e geração de relatórios executivos.
    """

    def __init__(self):
        """
        Inicializa o Agente Analista com configurações específicas.
        """
        super().__init__(
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

    def run(self, prompt):
        """
        Executa o agente com o prompt fornecido.

        Args:
            prompt (str): Prompt de entrada.

        Returns:
            Response: Resposta do agente.
        """
        return self.agent.run(prompt)
