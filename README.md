# 🚀 NewsGrid - Pipeline de Inteligência de Mercado

Um sistema automatizado e inteligente para análise de inteligência de mercado, utilizando IA avançada para pesquisar, resumir e analisar notícias sobre temas específicos. 📊🤖

## 🎯 Objetivo

O usuário solicita uma análise sobre um tema (ex: "Impacto da IA no mercado de ações em 2026"). O sistema pesquisa notícias recentes, resume cada uma, analisa o sentimento geral e gera um relatório consolidado, fornecendo insights valiosos para tomada de decisões. 💡

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**, organizando o código em camadas bem definidas:

- **Domain**: Lógica de negócio pura, entidades, repositórios e use cases.
- **Infrastructure**: Implementações concretas (repositórios SQL/Redis, agentes, workers).
- **API**: Camada de apresentação (rotas, schemas, controllers).
- **Core**: Configurações centrais (banco de dados, container DI).

Isso garante desacoplamento, testabilidade e manutenção.

## ✨ Funcionalidades

- 🔍 **Pesquisa automatizada** de notícias relevantes.
- 📝 **Resumo inteligente** de artigos com IA.
- 😊 **Análise de sentimento** para entender o tom das notícias.
- 📋 **Geração de relatórios consolidados** e abrangentes.
- 🔗 **Integração com modelos Groq** para processamento de linguagem natural de alta performance.

## 🛠️ Instalação

Siga estes passos simples para configurar o projeto:

1. 📥 **Clone o repositório**:
   ```sh
   git clone <url-do-repositorio>
   cd NewsGrid
   ```

2. 📦 **Instale as dependências**:
   ```sh
   uv sync
   ```

3. ⚙️ **Configure as variáveis de ambiente**:
   - Copie `.env-sample` para `.env` e preencha as chaves necessárias (ex: API key do Groq e API Key do Brave).
   - 🔑 [Groq Console](https://console.groq.com/home)
   - 🌐 [Brave API](https://api-dashboard.search.brave.com/app/)

4. 🐰 **Execute a Imagem do RabbitMQ** (Obrigatório):
   ```sh
   docker compose up rabbitmq
   ```
   > Para utilizar todo o projeto dockerizado siga para docs Usando-Docker

## 🚀 Uso

1. ▶️ **Execute a API junto com os Workers no modo dev**:
   ```sh
   make dev
   ```

2. 👷 **Rode os workers separadamente da API**:
   - `make worker1` para pesquisa de notícias. 🔎
   - `make worker2` para análise e geração de relatórios. 📊

3. ▶️ **Execute a API separadamente dos workers**:
   ```sh
   make run
   ```

### 🔐 Autenticação

Para fazer login via `/api/v1/auth/login`. Para mais detalhes, consulte AUTH.MD.

## 🧪 Testes

O projeto inclui uma suíte de testes automatizados para garantir a qualidade e integridade do código. Execute os testes com:

```sh
uv run pytest
```
>Dependências instaladas via `uv sync --group dev` (para incluir ferramentas de teste como pytest).

Para mais detalhes sobre estrutura, execução e boas práticas, consulte TESTES.MD.

## 📁 Estrutura do Projeto

```
├── .env-sample                   # Exemplo de arquivo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── .python-version               # Versão do Python
├── alembic.ini                   # Configuração do Alembic para migrações de banco
├── compose.yml                   # Configuração do Docker Compose 🐳
├── Dockerfile                    # Dockerfile para containerização da aplicação
├── makefile                      # Comandos de automação 🔧
├── pyproject.toml                # Dependências do projeto 📦
├── README.md                     # Este arquivo
├── .github/
│   └── workflows/                # Workflows do GitHub Actions para CI/CD
├── alembic/                      # Migrações de banco de dados
│   ├── env.py
│   ├── README                    # Comandos do Alembic 
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── startup.py               # Inicialização da aplicação FastAPI 🚀
│   ├── api/
│   │   ├── report/
│   │   │   ├── controller.py    # Lógica de negócio da análise 🧠
│   │   │   ├── routes.py        # Rotas da API 🛤️
│   │   │   └── schemas.py       # Schemas de validação ✅
│   │   ├── auth/
│   │   │   ├── controller.py    # Controller de autenticação 🔐
│   │   │   ├── routes.py        # Rotas de auth
│   │   │   └── schemas.py       # Schemas de auth
│   │   ├── status/
│   │   │   ├── controller.py    # Controller de status de tarefas ⏳
│   │   │   ├── routes.py        # Rotas de status
│   │   │   └── schemas.py       # Schemas de status
│   │   └── user/
│   │       ├── controller.py    # Controller de usuários 👤
│   │       ├── routes.py        # Rotas de usuários
│   │       └── schemas.py       # Schemas de usuários
│   ├── core/                    # Configurações centrais (database, container DI)
│   │   ├── container.py         # Container de injeção de dependências 🏗️
│   │   └── database.py          # Sessão do ORM (SQLALCHEMY 2.0)
│   ├── domain/                  # Camada de domínio (DDD) 🎯
│   │   ├── auth/
│   │   │   ├── entities.py      # Entidades de domínio para auth
│   │   │   ├── repositories.py  # Interfaces de repositório para auth
│   │   │   └── use_cases.py     # Use cases para auth
│   │   ├── report/
│   │   │   ├── entities.py      # Entidades de domínio para relatórios
│   │   │   ├── repositories.py  # Interfaces de repositório para relatórios
│   │   │   └── use_cases.py     # Use cases para relatórios
│   │   ├── status/
│   │   │   ├── entities.py      # Entidades de domínio para status
│   │   │   ├── repositories.py  # Interfaces de repositório para status
│   │   │   └── use_cases.py     # Use cases para status
│   │   └── user/
│   │       ├── entities.py      # Entidades de domínio para usuários
│   │       ├── repositories.py  # Interfaces de repositório para usuários
│   │       └── use_cases.py     # Use cases para usuários
│   ├── infrastructure/          # Camada de infraestrutura (implementações) 🔧
│   │   ├── agents/
│   │   │   ├── base_agent.py    # Base para agentes 🧠
│   │   │   ├── agent_analyst.py # Implementação do agente analista
│   │   │   └── agent_research.py # Implementação do agente pesquisador
│   │   ├── repositories/
│   │   │   ├── redis/
│   │   │   │   ├── cache_repository.py    # Repositório Redis para cache
│   │   │   │   └── status_repository.py   # Repositório Redis para status
│   │   │   └── sql/
│   │   │       ├── auth_repository.py     # Repositório SQL para auth
│   │   │       ├── report_repository.py   # Repositório SQL para relatórios
│   │   │       └── user_repository.py     # Repositório SQL para usuários
│   │   └── workers/
│   │       ├── base_worker.py            # Base para workers 🔧
│   │       ├── worker_analyst.py         # Worker para análise e relatórios 📊
│   │       └── worker_researcher.py      # Worker para pesquisa de notícias 🔎
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── reports.py
│   │   └── user.py
├── docs/                         # Documentos do projeto 📦
├── scripts/                      # Diretório para scripts utilitários
├── tests/                        # Testes automatizados
├── utils/                        # Utilitários globais
│   ├── broker.py                 # Utilitários para conexão com RabbitMQ
│   ├── exceptions.py             # Exceções reutilizáveis
│   ├── llm.py                    # Configuração de agentes LLM 🤖
│   ├── logging.py                # Configuração de logging
│   ├── redis_client.py           # Cliente Redis
│   ├── reporting.py              # Utilitários para geração de relatórios
│   ├── security.py               # Utilitários de segurança (JWT)
│   ├── send_to_queue.py          # Envio de mensagens para RabbitMQ 📨
│   ├── settings.py               # Configurações globais ⚙️
│   └── tasks_controller.py       # Controle de tarefas no Redis
```

## 📚 Referências

- 🔑 [Groq](https://console.groq.com/)
- 🌐 [Brave](https://api-dashboard.search.brave.com/app/)
- 📖 [Agno](https://docs.agno.com/)
- 🛠️ [Tools](https://docs.agno.com/integrations/toolkits/search/bravesearch)
- 📨 [RabbitMQ com Python - Contexto Teórico e Protocolo AMQP](https://www.youtube.com/watch?v=V_DBYCuwQAk)
- 🔍 [RabbitMQ](https://www.rabbitmq.com/docs/use-rabbitmq)