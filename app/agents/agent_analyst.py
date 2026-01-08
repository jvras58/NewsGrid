"""
Agente Analista de Mercado
"""

from utils.llm import create_agent


class AnalystAgent:
    def __init__(self):
        self.agent = create_agent(
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
        return self.agent.run(prompt)
