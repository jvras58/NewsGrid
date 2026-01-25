from unittest.mock import patch

from app.infrastructure.agents.agent_research import ResearchAgent


def test_research_agent_run():
    agent = ResearchAgent()
    with patch.object(agent.agent, "run", return_value="Resposta mockada"):
        result = agent.run("Prompt de teste")
        assert result == "Resposta mockada"
