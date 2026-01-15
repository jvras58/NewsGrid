# 🔐 Autenticação e Segurança - NewsGrid

Este documento descreve o funcionamento do sistema de autenticação via **JWT Bearer Token** implementado no NewsGrid.

## 🧠 Arquitetura

O sistema utiliza o padrão **OAuth2 com JWT Bearer Token**, seguindo as melhores práticas do FastAPI. Após o login, um token JWT é gerado e deve ser enviado no header `Authorization` de todas as requisições protegidas.

### Fluxo de Validação
1. **Cliente** faz login enviando `username` e `password` via POST para `/api/v1/auth/login`.
2. **API (FastAPI)** valida as credenciais no PostgreSQL, verificando o hash da senha, e gera um JWT.
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

Isso cria o usuário padrão no PostgreSQL se ele não existir.

* **Usuário Padrão:** `admin`
* **Senha Padrão:** `admin123` (Configurável via `settings.default_user_password` pelo `.env`)

### 2. Processo de Autenticação
1. **Login:** Envie uma requisição POST para `/api/v1/auth/login` com `username` e `password`.
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
| `password` | Senha do usuário |

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
  "email": "parceiro11@example.com",
  "password": "senha_segura"
}
```

> Todos os campos são obrigatórios. A senha será hasheada antes de ser armazenada no PostgreSQL.

### Listar Usuários

**GET** `/api/v1/users/`

*Requer JWT válido.*

Retorna todos os usuários cadastrados no sistema.

---

## 🛡️ Estrutura de Dados

### PostgreSQL (Usuários)
Os usuários são armazenados no PostgreSQL com as seguintes informações:
- `id`: ID único do usuário
- `username`: Nome de usuário único
- `email`: Email único
- `hashed_password`: Senha hasheada com bcrypt
- `created_at`: Data de criação

### Redis (Relatórios e Tasks)
Para manter a organização, utilizamos *Namespacing* nas chaves do Redis para relatórios e status de tasks:

| Tipo | Padrão da Chave | Exemplo | Descrição |
| --- | --- | --- | --- |
| **Relatórios** | `user:{username}:reports` | `user:admin:reports` | Set contendo IDs dos relatórios gerados pelo usuário. |
| **Task Status** | `task:{task_id}` | `task:12345` | Status da task (RESEARCHING, ANALYZING, COMPLETED, FAILED). |

> **Nota:** Com JWT, a validação de autenticação é stateless e não requer armazenamento de sessões no Redis.

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
     -d "username=admin&password=admin123"
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
   - **password:** sua senha (ex: `admin123`)
4. Clique em **Authorize**
5. Todas as requisições subsequentes incluirão automaticamente o JWT

### Usando Python (requests)

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]

# Requisição autenticada
headers = {"Authorization": f"Bearer {token}"}
me = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
print(me.json())
```