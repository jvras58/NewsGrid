## Visão Geral

O projeto NewsGrid demonstra uma **boa aderência à Clean Architecture** com separação clara entre camadas (domain, infrastructure, api) e uso de interfaces abstratas (ABCs) para repositórios. No entanto, existem **violações pontuais da regra de dependência** e **inconsistências** que comprometem a pureza arquitetural, especialmente na camada de domínio e nos controllers. A estrutura está bem organizada para uma POC, mas precisa de refinamentos para produção.

---

## 1. Problemas Encontrados

### 1.1 Camadas e Responsabilidades

| Problema | Localização | Severidade |
|----------|-------------|------------|
| **Controllers com lógica de negócio** | app/api/report/controller.py | 🔴 Alta |
| **Services legados ainda existem** | app/services/ (fora da estrutura DDD) | 🟡 Média |

**Exemplo do problema em controller.py:**

```python
def request_analysis_logic(topic: str, user_id: int):
    # ❌ Lógica de negócio direta no controller
    cache_key = make_cache_key(topic)
    cached_report = get_cached_report(cache_key)
    if cached_report:
        return {"status": "cached", "report": cached_report}

    task_id = str(uuid.uuid4())
    task_status_service.set_researching(task_id)  # ❌ Chamada direta a service

    payload = {"task_id": task_id, "topic": topic, "user_id": str(user_id)}
    send_to_queue("queue_research", payload)  # ❌ Infraestrutura no controller
```

**vs. o correto em controller.py:**

```python
def request_analysis_logic(request: AnalyzeRequest, user_id: int) -> AnalyzeResponse:
    use_case = container.request_analysis_use_case()  # ✅ Usa Use Case
    result = use_case.execute(request.topic, user_id)
    return AnalyzeResponse(**result)
```

---

### 1.2 Regra de Dependência

| Violação | Arquivo | Descrição |
|----------|---------|-----------|
| **Use Case depende de função de infraestrutura** | use_cases.py | `send_to_queue` importado diretamente |
| **Entidade com import de exception utilitária** | - | Deveria ter exceções próprias do domínio |

**Exemplo crítico:**

```python
from utils.send_to_queue import send_to_queue  # ❌ VIOLAÇÃO: domínio importa infraestrutura

class RequestAnalysisUseCase:
    def execute(self, topic: str, user_id: int) -> dict[str, Any]:
        # ...
        try:
            send_to_queue("queue_research", payload)  # ❌ Chamada direta
```

---

### 1.3 Domínio e Casos de Uso

| Problema | Impacto |
|----------|---------|
| **Entidades usam `dataclass` simples** | Falta validação rica no domínio |
| **Exceções genéricas** (`BadRequestError`) | Mistura erros HTTP com domínio |
| **Use Cases retornam `dict`** | Perda de tipagem forte |

**Exemplo de entidade anêmica:**

```python
@dataclass
class ReportEntity:
    id: int | None
    task_id: str
    owner_id: int
    topic: str
    content: str | None
    created_at: datetime

    def validate(self):  # ⚠️ Validação básica, sem comportamento de negócio
        if not self.task_id:
            raise ValueError("Task ID é obrigatório")
```

---

### 1.4 Interface Adapters e Infraestrutura

| Problema | Arquivo |
|----------|---------|
| **Schema com método `from_entity`** | Acoplamento correto ✅ |
| **Controller instancia Container diretamente** | Deveria receber via DI |
| **Duas pastas `api/analyze` e `api/report` fazem a mesma coisa** | Duplicação |

---

### 1.5 Injeção de Dependências

```python
container = Container()  # ❌ Instância global no módulo

def request_analysis_logic(request: AnalyzeRequest, user_id: int):
    use_case = container.request_analysis_use_case()  # ❌ Resolve dentro da função
```

**Problema:** O container é criado como variável de módulo, não injetado via FastAPI `Depends`.

---

### 1.6 Testabilidade

| Aspecto | Status |
|---------|--------|
| **Use Cases testáveis isoladamente** | ✅ Sim (recebem interfaces) |
| **Workers acoplados a pika** | ❌ Difícil mockar |
| **`send_to_queue` hardcoded em Use Case** | ❌ Impede testes puros |

---

## 2. Plano de Ação (Ordem de Prioridade)

### Fase 1: Correções Críticas (1 semana)

#### 1.1 Extrair `send_to_queue` para interface no domínio

```python
from abc import ABC, abstractmethod
from typing import Any

class IMessageBroker(ABC):
    """Interface para envio de mensagens."""
    
    @abstractmethod
    def publish(self, queue: str, payload: dict[str, Any]) -> None:
        pass
```

```python
from app.domain.messaging.repositories import IMessageBroker
from utils.send_to_queue import send_to_queue

class RabbitMQBroker(IMessageBroker):
    def publish(self, queue: str, payload: dict[str, Any]) -> None:
        send_to_queue(queue, payload)
```

```python
# ANTES:
from utils.send_to_queue import send_to_queue

# DEPOIS:
from app.domain.messaging.repositories import IMessageBroker

class RequestAnalysisUseCase:
    def __init__(
        self,
        cache_repo: ICacheRepository,
        task_status_repo: ITaskStatusRepository,
        message_broker: IMessageBroker,  # ✅ Injetado
    ):
        self.message_broker = message_broker
    
    def execute(self, topic: str, user_id: int) -> dict[str, Any]:
        # ...
        self.message_broker.publish("queue_research", payload)  # ✅ Usa interface
```

#### 1.2 Remover pasta duplicada `api/analyze`

Consolidar em `api/report` que já usa Use Cases corretamente.

---

### Fase 2: Melhoria de Domínio (2 semanas)

#### 2.1 Criar exceções de domínio

```python
class DomainException(Exception):
    """Base para exceções de domínio."""
    pass

class ReportNotFoundError(DomainException):
    def __init__(self, task_id: str):
        super().__init__(f"Relatório não encontrado: {task_id}")

class UnauthorizedAccessError(DomainException):
    def __init__(self, resource: str):
        super().__init__(f"Acesso negado a: {resource}")

class RateLimitExceededError(DomainException):
    def __init__(self, reset_in: int):
        super().__init__(f"Limite excedido. Reset em {reset_in}s")
```

#### 2.2 Use Cases retornarem entidades ou DTOs tipados

```python
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    status: str
    task_id: str | None = None
    report: ReportEntity | None = None

class RequestAnalysisUseCase:
    def execute(self, topic: str, user_id: int) -> AnalysisResult:  # ✅ Tipo forte
        # ...
        return AnalysisResult(status="processing", task_id=task_id)
```

---

### Fase 3: Injeção de Dependências via FastAPI (1 semana)

#### 3.1 Criar providers no dependencies.py

```python
from app.core.container import Container

_container = Container()

def get_request_analysis_use_case():
    return _container.request_analysis_use_case()

def get_report_use_case():
    return _container.get_report_use_case()
```

#### 3.2 Usar `Depends` nas rotas

```python
from app.api.dependencies import get_request_analysis_use_case
from app.domain.report.use_cases import RequestAnalysisUseCase

@router.post("/", response_model=AnalyzeResponse)
async def request_analysis(
    request: AnalyzeRequest,
    current_user: get_current_user_dep,
    use_case: RequestAnalysisUseCase = Depends(get_request_analysis_use_case),  # ✅
):
    result = use_case.execute(request.topic, current_user.id)
    return AnalyzeResponse.from_result(result)
```

---

### Fase 4: Limpeza de Legados (1 semana)

1. **Remover** app/services/ - migrar funcionalidades restantes para Use Cases
2. **Mover** send_to_queue.py para `app/infrastructure/messaging/`
3. **Consolidar** exceções em `app/domain/exceptions.py`

---

## 3. Resumo Visual da Arquitetura Atual vs. Ideal

### Atual (com problemas)

```
┌─────────────────────────────────────────────────────────┐
│  API Layer (FastAPI)                                    │
│  ┌─────────────┐    ┌─────────────┐                     │
│  │ routes.py   │───▶│ controller  │──┐                  │
│  └─────────────┘    └─────────────┘  │                  │
└──────────────────────────────────────│──────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────┐
│  Domain Layer                                           │
│  ┌─────────────┐                                        │
│  │ use_cases   │───▶ send_to_queue() ❌ VIOLA REGRA    │
│  └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

### Ideal (corrigido)

```
┌─────────────────────────────────────────────────────────┐
│  API Layer (FastAPI)                                    │
│  ┌─────────────┐    ┌─────────────┐                     │
│  │ routes.py   │───▶│ Depends(UC) │                     │
│  └─────────────┘    └─────────────┘                     │
└──────────────────────────────────────│──────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────┐
│  Domain Layer                                           │
│  ┌─────────────┐    ┌─────────────────┐                 │
│  │ use_cases   │───▶│ IMessageBroker  │ (interface)     │
│  └─────────────┘    └─────────────────┘                 │
└─────────────────────────────────────────────────────────┘
                                       ▲
                                       │
┌─────────────────────────────────────────────────────────┐
│  Infrastructure Layer                                   │
│  ┌─────────────────────┐                                │
│  │ RabbitMQBroker      │ (implementa IMessageBroker)    │
│  └─────────────────────┘                                │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Checklist de Conformidade

| Critério | Status | Ação |
|----------|--------|------|
| Entidades sem dependências externas | ⚠️ | Remover `BadRequestError` |
| Use Cases usam apenas interfaces | ❌ | Criar `IMessageBroker` |
| Controllers delegam para Use Cases | ⚠️ | Remover controller.py legado |
| Injeção via `Depends` | ❌ | Implementar providers |
| Exceções de domínio próprias | ❌ | Criar módulo `domain/exceptions.py` |
| Testabilidade dos Use Cases | ⚠️ | Após criar interfaces |

---

**Conclusão:** A arquitetura está 70% aderente à Clean Architecture. As principais melhorias são: (1) abstrair `send_to_queue` via interface, (2) remover duplicação `analyze`/`report`, e (3) usar `Depends` para injeção nos controllers.