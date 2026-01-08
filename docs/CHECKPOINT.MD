Checkpoint de Melhorias:

1. **Configuração do Docker Compose**: No arquivo compose.yml, o ambiente está configurado para usar variáveis do .env, mas ainda não implementado. É necessário atualizar para ler as credenciais do RabbitMQ do arquivo .env em vez de hardcodear.

2. **Refatoração de Funções nos Workers**: Nos arquivos worker_researcher.py e worker_analyst.py, funções como [`send_to_next_queue`](app/workers/worker_researcher.py) e [`save_report`](app/workers/worker_analyst.py) podem ser extraídas para módulos reutilizáveis, como em send_to_queue.py, para evitar duplicação e melhorar a manutenibilidade.

3. **Separação dos Agentes LLM**: Os agentes criados utilizando o llm.py (como `research_agent` e `analyst_agent`) estão definidos diretamente nos workers. Deve ser movido para módulos dedicado, como um novo arquivo em `utils/agents.py` ou `api/analyze/agents.py`, para centralizar e reutilizar a configuração dos agentes.