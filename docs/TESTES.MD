# 🧪 Testes do NewsGrid

Este documento descreve a estrutura e o funcionamento dos testes automatizados do projeto NewsGrid, utilizando pytest e uv.

## 📋 Introdução

Os testes garantem a qualidade e a integridade do código, verificando funcionalidades como criação de agentes, processamento de mensagens via RabbitMQ, geração de relatórios e análise de tópicos. Eles são executados com pytest, integrado ao uv para gerenciamento de dependências.

## 🏗️ Estrutura dos Testes

Os testes estão organizados no diretório `tests/`:

- **`conftest.py`**: ⚙️ Configurações compartilhadas, como fixtures para setup de testes.
- **`test_analyze.py`**: 🔍 Testa a API de análise de tópicos.
- **`test_create_agents.py`**: 🤖 Testa a criação e inicialização de agentes (ResearchAgent e AnalystAgent).
- **`test_report.py`**: 📄 Testa a geração e salvamento de relatórios em Markdown.
- **`test_rabbitmq_connection.py`**: 🐰 Testa a conexão e processamento de mensagens via RabbitMQ para workers.
- **`test_send_to_queue.py`**: 📨 Testa o envio de mensagens para filas RabbitMQ.
- **`test_workers.py`**: 👷 Testa o funcionamento geral dos workers (pesquisa e análise).

Cada arquivo foca em componentes específicos, usando mocks para isolar dependências externas (como conexões RabbitMQ ou APIs externas).

## ▶️ Como Executar os Testes

### 📋 Pré-requisitos
- Ambiente virtual ativado com `uv`.
- Dependências instaladas via `uv sync --group dev` (para incluir ferramentas de teste como pytest).

### 🚀 Comandos Básicos

- **Executar todos os testes**:
  ```
  uv run pytest
  ```

- **Executar testes de um arquivo específico**:
  ```
  uv run pytest tests/test_analyze.py
  ```

- **Executar um teste individual**:
  ```
  uv run pytest tests/test_analyze.py::test_request_analysis_success
  ```
  Substitua `test_request_analysis_success` pelo nome do teste desejado.

- **Executar testes com cobertura de código** (se `pytest-cov` estiver instalado):
  ```
  uv run pytest --cov=app --cov-report=html
  ```
  Isso gera um relatório HTML em `htmlcov/index.html`.

- **Executar testes em modo verbose** (mais detalhes):
  ```
  uv run pytest -v
  ```

- **Executar testes com saída de logs**:
  ```
  uv run pytest --log-cli-level=INFO
  ```

Para mais opções, consulte `uv run pytest --help`.

## 🛠️ Ferramentas e Dependências

- **pytest**: 🧪 Framework de testes, configurado em `pyproject.toml` com plugins como `pytest-asyncio` e `pytest-cov`.
- **uv**: 📦 Gerenciador de pacotes e execução de comandos.
- **unittest.mock**: 🎭 Para mocks e patches em testes.
- **pytest-cov** (opcional): 📊 Para geração de relatórios de cobertura.

## ➕ Adicionando Novos Testes

1. 📝 Crie um novo arquivo em `tests/` seguindo o padrão `test_*.py`.
2. 🔗 Use fixtures de `conftest.py` se aplicável.
3. ✍️ Escreva testes usando `def test_*()` ou `async def test_*()` para assíncronos.
4. 🎭 Use mocks para dependências externas (ex.: `@patch` para funções de conexão).
5. ✅ Execute os testes para validar.

Exemplo de teste simples:
```python
from utils.reporting import save_report

def test_save_report(tmp_path):
    # Teste de salvamento de relatório
    pass
```

## 📊 Cobertura de Código

A cobertura mede quantas linhas do código são executadas pelos testes. Execute com `--cov=app` para ver estatísticas. Relatórios HTML ajudam a identificar áreas não testadas.

## 💡 Dicas e Boas Práticas

- ✅ Execute testes antes de commits para evitar regressões.
- 🎭 Use mocks para testes unitários, evitando dependências reais.
- ⚡ Mantenha testes isolados e rápidos.
- 🐳 Para testes de integração, considere Docker para RabbitMQ.
- 🔍 Verifique logs em caso de falhas para depuração.
