# 🚀 NewsGrid - Pipeline de Inteligência de Mercado

Um sistema automatizado e inteligente para análise de inteligência de mercado, utilizando IA avançada para pesquisar, resumir e analisar notícias sobre temas específicos. 📊🤖

## 🎯 Objetivo

O usuário solicita uma análise sobre um tema (ex: "Impacto da IA no mercado de ações em 2026"). O sistema pesquisa notícias recentes, resume cada uma, analisa o sentimento geral e gera um relatório consolidado, fornecendo insights valiosos para tomada de decisões. 💡

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
   docker compose up
   ```

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


## 📁 Estrutura do Projeto

```
├── .env-sample                   # Exemplo de arquivo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── .python-version               # Versão do Python
├── compose.yml                   # Configuração do Docker Compose 🐳
├── makefile                      # Comandos de automação 🔧
├── pyproject.toml                # Dependências do projeto 📦
├── README.md                     # Este arquivo
├── app/
│   ├── startup.py               # Inicialização da aplicação FastAPI 🚀
│   ├── agents/
│   │   ├── agent_analyst.py     # Agente analista de mercado 📈
│   │   ├── agent_research.py    # Agente pesquisador 🔍
│   ├── api/
│   │   └── analyze/
│   │       ├── controller.py      # Lógica de negócio da análise 🧠
│   │       ├── routes.py          # Rotas da API 🛤️
│   │       ├── schemas.py8        # Schemas de validação ✅
│   └── workers/
│       ├── worker_analyst.py     # Worker para análise e relatórios 📊
│       ├── worker_researcher.py  # Worker para pesquisa de notícias 🔎
├── docs/
│   └── CHECKPOINT.MD             # Documento de checkpoints de melhorias
├── logs/                         # Diretório para logs
├── scripts/                      # Diretório para scripts
└── utils/
    ├── base_agent.py             # base para agentes 🧠
    ├── base_worker.py            # base para workers 🔧
    ├── broker.py                 # Utilitários para conexão com RabbitMQ
    ├── llm.py                    # Configuração de agentes LLM 🤖
    ├── logging.py                # Configuração de logging
    ├── reporting.py              # Utilitários para geração de relatórios
    ├── send_to_queue.py          # Envio de mensagens para RabbitMQ 📨
    ├── settings.py               # Configurações globais ⚙️
```

## 📚 Referências

- 🔑 [Groq](https://console.groq.com/)
- 🌐 [Brave](https://api-dashboard.search.brave.com/app/)
- 📖 [Agno](https://docs.agno.com/)
- 🛠️ [Tools](https://docs.agno.com/integrations/toolkits/search/bravesearch)
- 📨 [RabbitMQ com Python - Contexto Teórico e Protocolo AMQP](https://www.youtube.com/watch?v=V_DBYCuwQAk)
- 🔍 [RabbitMQ](https://www.rabbitmq.com/docs/use-rabbitmq)