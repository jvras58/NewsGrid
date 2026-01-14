# 🔐 Autenticação e Segurança - NewsGrid

Este documento descreve o funcionamento do sistema de autenticação via **JWT Bearer Token** implementado no NewsGrid.

## 🧠 Arquitetura

O sistema utiliza o padrão **OAuth2 com JWT Bearer Token**, seguindo as melhores práticas do FastAPI. Após o login, um token JWT é gerado e deve ser enviado no header `Authorization` de todas as requisições protegidas.

### Fluxo de Validação
1. **Cliente** faz login enviando `username` e `password` (token de acesso) via POST para `/api/v1/auth/login`.
2. **API (FastAPI)** valida o token de acesso no Redis, verifica se pertence ao usuário e gera um JWT.
3. **Para rotas protegidas:** A API valida o JWT via dependência `get_current_user` usando `OAuth2PasswordBearer`.
4. **Se Válido:** O JWT é decodificado e o `username` é extraído do payload. A API permite o acesso.
5. **Se Inválido:** A API retorna `401 Unauthorized` com header `WWW-Authenticate: Bearer`.

### Vantagens do JWT
- **Stateless:** Não requer consulta ao Redis para validar sessões.
- **Padrão de Mercado:** Compatível com qualquer cliente HTTP e frameworks frontend.
- **Swagger UI:** Integração nativa com o botão "Authorize" em `/docs`.

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
* **Token de Acesso Padrão:** `12345678-1234-5678-9012-123456789012` (Configurável via `settings.default_token` pelo `.env`)

### 2. Processo de Autenticação
1. **Login:** Envie uma requisição POST para `/api/v1/auth/login` com `username` e `password` (seu token de acesso).
2. **Receba o JWT:** A resposta contém `access_token` e `token_type`.
3. **Use o JWT:** Inclua o header `Authorization: Bearer <access_token>` em todas as requisições protegidas.

---

## 📡 Endpoints de Autenticação

### Login

**POST** `/api/v1/auth/login`

**Content-Type:** `application/x-www-form-urlencoded` (padrão OAuth2)

**Form Data:**

| Campo | Descrição |
|-------|-----------|
| `username` | Nome do usuário |
| `password` | Token de acesso do usuário |

**Resposta de Sucesso:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Expiração do Token

- **Expiração:** O JWT expira após 30 minutos (configurável via `jwt_access_token_expire_minutes`).
- **Relatórios:** Relatórios criados permanecem associados ao usuário no Redis e podem ser acessados após novo login.
- **Renovação:** Para renovar o acesso, o usuário deve fazer login novamente via `/api/v1/auth/login`.

### Verificar Usuário Atual

**GET** `/api/v1/auth/me`

**Header:** `Authorization: Bearer <access_token>`

**Resposta:**

```json
{
  "username": "admin",
  "status": "authenticated via JWT"
}
```

### Criar Novo Usuário

**POST** `/api/v1/users/`

*Requer JWT válido no header Authorization.*

**Body:**

```json
{
  "username": "parceiro11",
  "token": "123e4567-e89b-12d3-a456-426614174000"
}
```

> O campo `token` é opcional. Se omitido, será gerado automaticamente um UUID.

### Listar Usuários

**GET** `/api/v1/users/`

*Requer JWT válido.*

Retorna todos os usuários cadastrados no sistema.

### Revogar Acesso

**DELETE** `/api/v1/users/{username}`

*Requer JWT válido.*

Remove imediatamente o acesso do usuário, invalidando o token de acesso.

---

## 🛡️ Estrutura no Redis

Para manter a organização, utilizamos *Namespacing* nas chaves do Redis:

| Tipo | Padrão da Chave | Exemplo | Descrição |
| --- | --- | --- | --- |
| **Token** | `auth:token:{token}` | `auth:token:abc-123` | Guarda o `username` dono do token de acesso. |
| **Usuário** | `auth:user:{username}` | `auth:user:admin` | Guarda o `token` atual do usuário (lookup reverso). |
| **Lista** | `auth:users_list` | `auth:users_list` | Set contendo todos os usernames ativos. |
| **Relatórios** | `user:{username}:reports` | `user:admin:reports` | Set contendo IDs dos relatórios gerados pelo usuário. |

> **Nota:** Com JWT, não há mais chaves `session:{session_id}` no Redis. A validação é feita via assinatura do token.

---

## ⚙️ Configuração JWT

As seguintes variáveis de ambiente controlam o comportamento do JWT (definidas em `utils/settings.py`):

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `JWT_SECRET_KEY` | `sua-chave-secreta-super-segura` | Chave secreta para assinar os tokens |
| `JWT_ALGORITHM` | `HS256` | Algoritmo de assinatura |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Tempo de expiração do token em minutos |

> ⚠️ **Importante:** Em produção, defina `JWT_SECRET_KEY` com uma chave forte e única no arquivo `.env`.

---

## 🔄 Fluxo de Processamento (Worker)

1. O usuário autenticado solicita uma análise (com JWT no header).
2. A API extrai o `username` do JWT e anexa ao payload da mensagem enviada ao RabbitMQ.
3. O Worker processa a IA.
4. O Worker salva o relatório final e usa o `ReportService` para vincular esse relatório à lista do usuário (`user:{username}:reports`).

Isso garante que cada usuário tenha acesso apenas aos seus próprios relatórios.

---

## 📋 Exemplos Práticos

### Usando cURL (Terminal)

#### 1. Fazer Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=12345678-1234-5678-9012-123456789012"
```

**Resposta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 2. Fazer uma Requisição Protegida (usando o JWT)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/?topic=Inteligencia%20Artificial" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 3. Verificar Usuário Logado

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Usando Swagger UI

1. Acesse `http://localhost:8000/docs`
2. Clique no botão **Authorize** 🔓 no canto superior direito
3. Preencha:
   - **username:** seu nome de usuário (ex: `admin`)
   - **password:** seu token de acesso (ex: `12345678-1234-5678-9012-123456789012`)
4. Clique em **Authorize**
5. Todas as requisições subsequentes incluirão automaticamente o JWT

### Usando Python (requests)

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "admin", "password": "12345678-1234-5678-9012-123456789012"}
)
token = response.json()["access_token"]

# Requisição autenticada
headers = {"Authorization": f"Bearer {token}"}
me = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
print(me.json())
```