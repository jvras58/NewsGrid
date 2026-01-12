# 🔐 Autenticação e Segurança - NewsGrid

Este documento descreve o funcionamento do sistema de autenticação via Token implementado no NewsGrid, utilizando Redis como fonte de verdade.

## 🧠 Arquitetura

O sistema utiliza uma estratégia de **API Key no Header**. Não há sessões ou cookies; cada requisição deve ser autenticada individualmente.

### Fluxo de Validação
1.  **Cliente** envia uma requisição com o header `Authorization: Bearer <token>`.
2.  **API (FastAPI)** intercepta a requisição via dependência `verify_token`.
3.  **Redis** é consultado na chave `auth:token:{token_recebido}`.
4.  **Se Válido:** O Redis retorna o `username` associado. A API permite o acesso e injeta o usuário no contexto.
5.  **Se Inválido:** A API retorna `401 Unauthorized` ou `403 Forbidden`.

---

## 🚀 Como Usar

### 1. Credenciais Iniciais (Seed)
Ao iniciar a aplicação pela primeira vez, o sistema cria automaticamente um usuário administrador se ele não existir.

* **Usuário Padrão:** `admin`
* **Token Padrão:** `newsgrid-secret-123` (Configurável via código/env)

### 2. Cabeçalho Obrigatório
Todas as rotas protegidas exigem o seguinte cabeçalho HTTP:

```http
Authorization: Bearer <SEU_TOKEN_AQUI>
```

---

## 📡 Endpoints de Autenticação

### Criar Novo Usuário

**POST** `/api/v1/auth/create`
*Requer token de um usuário existente (ou do admin).*

**Body:**

```json
{
  "username": "parceiro11",
  "token": "token-personalizado-123" // Opcional (gera UUID se omitido)
}
```

### Listar Usuários

**GET** `/api/v1/auth/list`
*Retorna todos os usuários cadastrados no sistema.*

### Revogar Acesso

**DELETE** `/api/v1/auth/revoke/{username}`
*Remove imediatamente o acesso do usuário, invalidando o token.*

---

## 🛡️ Estrutura no Redis

Para manter a organização, utilizamos *Namespacing* nas chaves do Redis:

| Tipo | Padrão da Chave | Exemplo | Descrição |
| --- | --- | --- | --- |
| **Token** | `auth:token:{token}` | `auth:token:abc-123` | Guarda o `username` dono do token. |
| **Usuário** | `auth:user:{username}` | `auth:user:admin` | Guarda o `token` atual do usuário (lookup reverso). |
| **Lista** | `auth:users_list` | `auth:users_list` | Set contendo todos os usernames ativos. |
| **Relatórios** | `user:{username}:reports` | `user:admin:reports` | Set contendo IDs dos relatórios gerados pelo usuário. |

---

## 🔄 Fluxo de Processamento (Worker)

1. O usuário autenticado solicita uma análise.
2. A API anexa o `user_id` (username) no payload da mensagem e envia para o RabbitMQ.
3. O Worker processa a IA.
4. O Worker salva o relatório final e usa o `ReportService` para vincular esse relatório à lista do usuário (`user:{username}:reports`).

Isso garante que cada usuário tenha acesso apenas/historicamente aos seus próprios relatórios.

---

### 2. Como fazer a requisição agora (Exemplos Práticos)

Como agora a porta está trancada, você precisa passar a chave (`Authorization: Bearer <token>`) em toda chamada.

#### Usando cURL (Terminal)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/?topic=Inteligencia%20Artificial" \
     -H "accept: application/json" \
     -H "Authorization: Bearer newsgrid-secret-123" \
     -d ""
```