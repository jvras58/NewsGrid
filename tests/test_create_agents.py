from unittest.mock import Mock, patch

from app.agents.agent_analyst import AnalystAgent
from app.agents.agent_research import ResearchAgent


@patch("utils.base_agent.create_agent")
def test_research_agent_init(mock_create_agent):
    mock_agent = Mock()
    mock_create_agent.return_value = mock_agent
    agent = ResearchAgent()
    mock_create_agent.assert_called_once()
    assert agent.agent == mock_agent


@patch("utils.base_agent.create_agent")
def test_research_agent_run(mock_create_agent):
    mock_agent = Mock()
    mock_agent.run.return_value = Mock(content="Mocked research")
    mock_create_agent.return_value = mock_agent
    agent = ResearchAgent()
    response = agent.run("Test prompt")
    assert response.content == "Mocked research"


@patch("utils.base_agent.create_agent")
def test_analyst_agent_init(mock_create_agent):
    mock_agent = Mock()
    mock_create_agent.return_value = mock_agent
    agent = AnalystAgent()
    mock_create_agent.assert_called_once()
    assert agent.agent == mock_agent


@patch("utils.base_agent.create_agent")
def test_analyst_agent_run(mock_create_agent):
    mock_agent = Mock()
    mock_agent.run.return_value = Mock(content="Mocked analysis")
    mock_create_agent.return_value = mock_agent
    agent = AnalystAgent()
    response = agent.run("Test prompt")
    assert response.content == "Mocked analysis"
