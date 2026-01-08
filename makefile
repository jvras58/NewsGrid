.PHONY: install run workers

# Instalar dependências usando uv
install:
	uv sync

# Executar a Aplicação
run:
	$env:PYTHONPATH = "."; uv run uvicorn app.startup:app --reload --host 0.0.0.0 --port 8000
	

# iniciar o RabbitMQ
init_rabbitmq:
	@echo "Iniciando imagem do rabbitmq..."
	docker compose up -d rabbitmq
	@echo "Aguardando RabbitMQ iniciar..."
	ping -n 11 127.0.0.1 >nul

# iniciar os workers
worker1:
	$env:PYTHONPATH = "."; uv run app/workers/worker_researcher.py

worker2:
	$env:PYTHONPATH = "."; uv run app/workers/worker_analyst.py


# teste
test-curl:
	Invoke-WebRequest -Method POST -Uri "http://127.0.0.1:8000/api/v1/analyze?topic=Futuro%20do%20Javascript%20em%202025" -UseBasicParsing
