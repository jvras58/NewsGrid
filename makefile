.PHONY: install run workers

# Instalar dependências usando uv
install:
	uv sync

# Executar a Aplicação
run:
	uv run uvicorn api:app --reload

# iniciar os workers
workers:
	@echo "Iniciando imagem do rabbitmq..."
	docker compose up -d rabbitmq
	@echo "Aguardando RabbitMQ iniciar..."
	ping -n 11 127.0.0.1 >nul
	@echo "Iniciando workers..."
	uv run worker_researcher.py &
	uv run worker_analyst.py &
