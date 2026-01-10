Checkpoint de Melhorias:

1. **Automatizar execução dos workers**: Atualmente, precisamos rodar os workers manualmente com comandos como 'uv run'. Isso não é uma prática ideal; devemos integrar o disparo automático dos workers ao receber uma requisição POST na API, utilizando filas assíncronas (RabbitMQ já em uso) ou tarefas em background para processamento sem intervenção manual.

2. **Melhorar configuração e deploy**: Adicionar suporte completo ao Docker para containerização da aplicação inteira, incluindo workers, e configurar CI/CD básico com GitHub Actions para automação de builds e deploys.