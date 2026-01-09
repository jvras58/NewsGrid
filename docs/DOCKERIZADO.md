# 🚀 Executando o Projeto NewsGrid com Docker

Este guia explica como executar todo o projeto NewsGrid usando Docker e Docker Compose, garantindo isolamento, facilidade de implantação e comunicação perfeita entre os serviços. 🐳📦

## 📋 Pré-requisitos

- 🐳 **Docker** instalado e em execução.
- 📦 **Docker Compose** instalado.
- ⚙️ Arquivo `.env` configurado com as variáveis necessárias (ex: chaves de API do Groq e Brave, credenciais do RabbitMQ).

## 🏗️ Estrutura dos Serviços

O `compose.yml` define quatro serviços principais que trabalham juntos:

- **API** 🚀: Servidor FastAPI que expõe endpoints para análise de mercado. Disponível em `http://localhost:8000`.
- **Researcher** 🔍: Worker que pesquisa notícias relevantes usando ferramentas de busca e IA.
- **Analyst** 📊: Worker que analisa sentimentos, resume artigos e gera relatórios consolidados.
- **RabbitMQ** 🐰: Message broker que coordena a comunicação assíncrona entre os workers e a API.

Todos os serviços compartilham a mesma rede Docker, permitindo comunicação interna via nomes de serviço.

## ⚠️ Configuração Importante

Antes de iniciar, certifique-se de que no arquivo `.env`, a variável `RABBITMQ_HOST` esteja definida como `rabbitmq` (o nome do serviço no `compose.yml`), **não como `localhost`**. Isso permite que os serviços `researcher` e `analyst` se comuniquem com o RabbitMQ via rede interna do Docker. 🌐

Exemplo no `.env`:
```
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=seu_usuario
RABBITMQ_PASSWORD=sua_senha
```

## ▶️ Passos para Executar

1. **📂 Navegue até o diretório raiz do projeto**:
   ```sh
   cd NewsGrid
   ```

2. **🔨 Construa e inicie todos os serviços**:
   ```sh
   docker compose up --build
   ```
   - Isso criará e iniciará os containers para `api`, `researcher`, `analyst` e `rabbitmq`. ⏳
   - A API estará disponível em `http://localhost:8000`. 🌐
   - O painel de gerenciamento do RabbitMQ estará em `http://localhost:15672` (use as credenciais do `.env`). 🖥️

3. **📜 Verifique os logs** (opcional, em outro terminal):
   ```sh
   docker compose logs -f
   ```

## 🛑 Parando os Serviços

Para parar e remover os containers:
```sh
docker compose down
```

Para remover também os volumes (dados persistentes):
```sh
docker compose down -v
```

## 💡 Notas

- 🔗 Os serviços `researcher` e `analyst` dependem do `rabbitmq` e iniciarão após ele.
- 🐛 Se houver erros, verifique os logs com `docker compose logs <nome_do_serviço>`.
- 🛠️ Para desenvolvimento, você pode executar serviços individuais com `docker compose up <nome_do_serviço>`.