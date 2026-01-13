# 🔐 Autenticação e Segurança - NewsGrid

Este documento descreve o funcionamento do sistema de autenticação via Sessões implementado no NewsGrid, utilizando Redis como fonte de verdade.

## 🧠 Arquitetura

O sistema utiliza uma estratégia de **Sessões com Cookies**. Após o login, uma sessão é criada e armazenada em um cookie seguro. As rotas protegidas verificam a validade da sessão automaticamente.

### Fluxo de Validação
1. **Cliente** faz login enviando o token via POST para `/api/v1/auth/login`.
2. **API (FastAPI)** valida o token, cria uma sessão no Redis e define um cookie `session_id`.
3. **Para rotas protegidas:** A API verifica o cookie `session_id` via dependência `verify_session`.
4. **Redis** é consultado na chave `session:{session_id}`.
5. **Se Válido:** O Redis retorna o `username` associado. A API permite o acesso e injeta o usuário no contexto.
6. **Se Inválido:** A API retorna `401 Unauthorized`.

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
1. **Login:** Envie uma requisição POST para `/api/v1/auth/login` com o token no body.
2. **Uso:** O navegador/cliente mantém o cookie automaticamente para requisições subsequentes.
3. **Logout:** Envie uma requisição POST para `/api/v1/auth/logout` para encerrar a sessão.

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

- **Expiração:** Sessões expiram automaticamente após 24 horas de inatividade para garantir segurança.
- **Relatórios:** Relatórios criados durante a sessão permanecem associados ao usuário no Redis e podem ser acessados após um novo login. Eles não são afetados pela expiração da sessão.
- **Renovação:** Não há extensão automática de sessões. Para renovar o acesso, o usuário deve fazer login novamente via `/api/v1/auth/login`. Isso cria uma nova sessão e define um novo cookie.

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

#### 3. Verificar Usuário Logado

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -b cookies.txt
```

#### 4. Logout

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
     -b cookies.txt \
     -c cookies.txt
```