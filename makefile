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
	start cmd /c "set PYTHONPATH=. && uv run python -m app.workers.worker_researcher"
	start cmd /c "set PYTHONPATH=. && uv run python -m app.workers.worker_analyst"
else
	set PYTHONPATH=. && uv run python -m app.workers.worker_researcher &
	set PYTHONPATH=. && uv run python -m app.workers.worker_analyst &
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
	set PYTHONPATH=. && uv run python -m app.workers.worker_researcher

worker2:
	set PYTHONPATH=. && uv run python -m app.workers.worker_analyst

# iniciar todos os workers
workers:
	set PYTHONPATH=. && uv run python -m scripts.start_workers


# teste
test-curl:
	powershell -Command "$createResponse = Invoke-WebRequest -Method POST -Uri 'http://localhost:8000/api/v1/auth/create' -Body '{\"username\": \"testuser\"}' -ContentType 'application/json' -UseBasicParsing | ConvertFrom-Json; $token = $createResponse.token; Invoke-WebRequest -Method POST -Uri 'http://localhost:8000/api/v1/analyze/?topic=Bitcoin' -Headers @{'Authorization'='Bearer ' + $token} -UseBasicParsing"

# cobertura de teste
test-coverage:
	set PYTHONPATH=. && uv run pytest --cov=app --cov-report=html
