.PHONY: install run workers

# Instalar dependências usando uv
install:
	uv sync

# Modo pacote
package:
	uv pip install -e .

# Executar a Api
run:
	set PYTHONPATH=. && uv run uvicorn app.startup:app --reload --host 0.0.0.0 --port 8000

# Executar a Aplicação completa com os workers
dev:
ifeq ($(OS),Windows_NT)
	start cmd /c "set PYTHONPATH=. && uv run worker-researcher"
	start cmd /c "set PYTHONPATH=. && uv run worker-analyst"
else
	set PYTHONPATH=. && uv run worker-researcher &
	set PYTHONPATH=. && uv run worker-analyst &
endif
	set PYTHONPATH=. && uv run uvicorn app.startup:app --reload --host 0.0.0.0 --port 8000
	

# iniciar o RabbitMQ
init_rabbitmq:
	@echo "Iniciando imagem do rabbitmq..."
	docker compose up -d rabbitmq
	@echo "Aguardando RabbitMQ iniciar..."
	ping -n 11 127.0.0.1 >nul

# iniciar os workers separadamente
worker1:
	set PYTHONPATH=. && uv run worker-researcher

worker2:
	set PYTHONPATH=. && uv run worker-analyst

# iniciar todos os workers
workers:
	set PYTHONPATH=. && uv run start-workers


# teste
test-curl:
	Invoke-WebRequest -Method POST -Uri "http://127.0.0.1:8000/api/v1/analyze?topic=Futuro%20do%20Javascript%20em%202025" -UseBasicParsing
