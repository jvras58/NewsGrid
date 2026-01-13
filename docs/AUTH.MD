# 🔐 Autenticação e Segurança - NewsGrid

Este documento descreve o funcionamento do sistema de autenticação **híbrida** implementado no NewsGrid, utilizando Redis como fonte de verdade.

## 🧠 Arquitetura

O sistema utiliza uma estratégia de **Autenticação Híbrida** que suporta dois métodos simultâneos:
- **Navegadores:** Autenticação via Cookies de sessão (`session_id`)
- **APIs/Scripts:** Autenticação via Bearer Tokens no header `Authorization: Bearer <token>`

Isso permite que tanto aplicações web (navegadores) quanto scripts/APIs utilizem o mesmo sistema de forma natural.

### Fluxo de Validação Híbrida

A função `get_current_user()` verifica a autenticação com a seguinte prioridade:

```
Requisição da API
        ↓
┌─────────────────────────────────┐
│  get_current_user()             │
└─────────────────────────────────┘
        ↓
    ┌───────────────────────┐
    │ Tenta Cookie?         │
    └───────────────────────┘
    /                       \
  SIM                       NÃO
  ↓                         ↓
Valida via              ┌───────────────────────┐
AuthService            │ Tenta Bearer Token?   │
.get_user_by_session() └───────────────────────┘
  ✓ Retorna             /                       \
                      SIM                       NÃO
                      ↓                         ↓
                  Valida via               ❌ HTTPException
              AuthService                 (401 Unauthorized)
              .authenticate_by_token()
                ✓ Retorna
```

**Detalhes do fluxo:**
1. **Cliente** faz login enviando o token via POST para `/api/v1/auth/login`.
2. **API (FastAPI)** valida o token e:
   - Cria uma sessão no Redis e define um cookie `session_id` (para navegadores)
   - Retorna o token autenticado (para APIs)
3. **Para rotas protegidas:** A API verifica automaticamente via `get_current_user()` em ordem:
   1. Primeiro tenta validar o cookie `session_id` via Redis
   2. Se não encontrado, tenta validar o Bearer token
   3. Se nenhum método funcionar, retorna `401 Unauthorized`

---

## 🚀 Como Usar

### 1. Credenciais Iniciais (Seed)
Para inicializar o sistema com um usuário administrador, execute o script de seed:

```bash
make seed
# ou
uv run python -m scripts.seed_initial
```

Isso cria o usuário padrão no Redis se ele não existir.

* **Usuário Padrão:** `admin`
* **Token Padrão:** `12345678-1234-5678-9012-123456789012` (Configurável via `settings.default_token` pelo `.env`)

### 2. Processo de Autenticação

#### Via Navegador (Cookie)
1. **Login:** Envie uma requisição POST para `/api/v1/auth/login` com o token no body.
2. **Uso:** O navegador mantém o cookie `session_id` automaticamente para requisições subsequentes.
3. **Logout:** Envie uma requisição POST para `/api/v1/auth/logout` para encerrar a sessão.

#### Via API/Script (Bearer Token)
1. **Obtenha o token:** Faça login em `/api/v1/auth/login` com seu token de autenticação.
2. **Uso:** Inclua o token no header `Authorization: Bearer <seu_token>` em todas as requisições.
3. **Sem logout:** Tokens não precisam de logout; expiram naturalmente com a sessão do usuário.

---

## 📡 Endpoints de Autenticação

### Login

**POST** `/api/v1/auth/login`

**Body:**

```json
{
  "token": "12345678-1234-5678-9012-123456789012"
}
```

**Resposta de Sucesso:**

```json
{
  "message": "Login realizado",
  "user": "admin"
}
```

Define um cookie `session_id` que expira em 24 horas.

### Logout

**POST** `/api/v1/auth/logout`

Remove o cookie `session_id` e invalida a sessão no Redis.

### Renovação e Expiração de Sessões

- **Expiração de Sessão:** Sessões (cookies) expiram automaticamente após 24 horas de inatividade para garantir segurança.
- **Expiração de Token:** Tokens Bearer expiram com a sessão associada ao usuário.
- **Relatórios:** Relatórios criados durante a sessão permanecem associados ao usuário no Redis e podem ser acessados após um novo login. Eles não são afetados pela expiração da sessão.
- **Renovação:** Não há extensão automática de sessões. Para renovar o acesso, o usuário deve fazer login novamente via `/api/v1/auth/login`. Isso cria uma nova sessão e define um novo cookie/token.

### Verificar Usuário Atual

**GET** `/api/v1/auth/me`

Retorna o usuário autenticado atual.

### Criar Novo Usuário

**POST** `/api/v1/users/`
*Requer sessão ativa (usuário logado).*

**Body:**

```json
{
  "username": "parceiro11",
  "token": "123e4567-e89b-12d3-a456-426614174000" // Opcional; se informado, deve ser UUID válido (36 caracteres). Se omitido, será gerado automaticamente.
}
```

### Listar Usuários

**GET** `/api/v1/users/`
*Requer sessão ativa.*

Retorna todos os usuários cadastrados no sistema.

### Revogar Acesso

**DELETE** `/api/v1/users/{username}`
*Requer sessão ativa.*

Remove imediatamente o acesso do usuário, invalidando o token e sessões ativas.

---

## 🛡️ Estrutura no Redis

Para manter a organização, utilizamos *Namespacing* nas chaves do Redis:

| Tipo | Padrão da Chave | Exemplo | Descrição |
| --- | --- | --- | --- |
| **Token** | `auth:token:{token}` | `auth:token:abc-123` | Guarda o `username` dono do token. |
| **Usuário** | `auth:user:{username}` | `auth:user:admin` | Guarda o `token` atual do usuário (lookup reverso). |
| **Lista** | `auth:users_list` | `auth:users_list` | Set contendo todos os usernames ativos. |
| **Sessão** | `session:{session_id}` | `session:uuid-123` | Guarda o `username` associado à sessão (expira em 24h). |
| **Relatórios** | `user:{username}:reports` | `user:admin:reports` | Set contendo IDs dos relatórios gerados pelo usuário. |

---

## 🔄 Fluxo de Processamento (Worker)

1. O usuário autenticado solicita uma análise.
2. A API anexa o `user_id` (username) no payload da mensagem e envia para o RabbitMQ.
3. O Worker processa a IA.
4. O Worker salva o relatório final e usa o `ReportService` para vincular esse relatório à lista do usuário (`user:{username}:reports`).

Isso garante que cada usuário tenha acesso apenas/historicamente aos seus próprios relatórios.

---

## 📋 Exemplos Práticos

### Usando cURL (Terminal)

#### 1. Fazer Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"token": "12345678-1234-5678-9012-123456789012"}' \
     -c cookies.txt
```

Isso salva o cookie em `cookies.txt`.

#### 2. Fazer uma Requisição Protegida (usando o cookie)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/?topic=Inteligencia%20Artificial" \
     -H "accept: application/json" \
     -b cookies.txt \
     -d ""
```

#### 2b. Fazer uma Requisição Protegida (usando Bearer Token)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/?topic=Inteligencia%20Artificial" \
     -H "accept: application/json" \
     -H "Authorization: Bearer 12345678-1234-5678-9012-123456789012" \
     -d ""
```

#### 3. Verificar Usuário Logado (com cookie)

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -b cookies.txt
```

#### 3b. Verificar Usuário Logado (com Bearer Token)

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer 12345678-1234-5678-9012-123456789012"
```

#### 4. Logout (com cookie)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
     -b cookies.txt \
     -c cookies.txt
```

**Nota:** Com Bearer Tokens, não há necessidade de fazer logout explícito. O token expira naturalmente.

---

## 🔄 Casos de Uso

### Navegador Web
**Fluxo:**
1. Usuário faz login via browser
2. Browser recebe cookie `session_id`
3. Todas as requisições subsequentes incluem automaticamente o cookie
4. Usuário faz logout (limpa cookie)

**Vantagem:** Experiência de usuário contínua; cookies gerenciados automaticamente pelo navegador.

### API/Script Externo
**Fluxo:**
1. Script faz login com token em `/api/v1/auth/login`
2. Script inclui Bearer token no header em todas as requisições
3. Sem necessidade de logout; token expira naturalmente

**Vantagem:** Simples para integrações; ideal para automações e bots.

### Integração Híbrida
O mesmo endpoint pode ser acessado tanto por navegadores (cookies) quanto por scripts (Bearer tokens) simultaneamente, sem conflitos.