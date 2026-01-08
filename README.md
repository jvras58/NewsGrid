# NewsGrid - Pipeline de Inteligência de Mercado

Um sistema automatizado para análise de inteligência de mercado, utilizando IA para pesquisar, resumir e analisar notícias sobre temas específicos.

## Objetivo

O usuário solicita uma análise sobre um tema (ex: "Impacto da IA no mercado de ações em 2026"). O sistema pesquisa notícias recentes, resume cada uma, analisa o sentimento geral e gera um relatório consolidado.

## Funcionalidades

- Pesquisa automatizada de notícias relevantes.
- Resumo inteligente de artigos.
- Análise de sentimento com IA.
- Geração de relatórios consolidados.
- Integração com modelos Groq para processamento de linguagem natural.

## Instalação

1. Clone o repositório:
   ```sh
   git clone <url-do-repositorio>
   cd NewsGrid
   ```

2. Instale as dependências:
   ```sh
   uv sync
   ```

3. Configure as variáveis de ambiente:
   - Copie `.env-sample` para `.env` e preencha as chaves necessárias (ex: API key do Groq e API Key do Brave).
   -[Groq_Console](https://console.groq.com/home)
   -[Brave](https://api-dashboard.search.brave.com/app/)

4. Execute a Imagem do Rabbitmq (Obrigatorio):
   ```sh
   docker compose up
   ```

## Uso

1. Execute o script principal:
   ```sh
   uv run uvicorn api:app --reload
   ```

2. Rode os workers:
   - `uv run python worker_researcher.pyy` para pesquisa.
   - `uv run python worker_analyst.py` para análise.

Consulte [settings.py](settings.py) para configurações e [llm.py](llm.py) para a criação de agentes.

## Estrutura do Projeto

- `api.py`: API principal.
- `llm.py`: Configuração de agentes LLM.
- `worker_researcher.py`: Worker para pesquisa de notícias.
- `worker_analyst.py`: Worker para análise e relatórios.
- `settings.py`: Configurações globais.


## Referencias:
   -[Groq](https://console.groq.com/)
   -[Brave](https://api-dashboard.search.brave.com/app/)
   -[Agno](https://docs.agno.com/)
   -[Tools](https://docs.agno.com/integrations/toolkits/search/bravesearch)