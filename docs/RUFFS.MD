# Ruff - Linter e Formatador para Python

## O que é Ruff?

Ruff é um linter e formatador de código extremamente rápido para Python, escrito em Rust. Ele oferece compatibilidade ampla com ferramentas existentes e suporta mais de 800 regras de linting. Ruff é projetado para ser uma alternativa rápida ao Flake8, Black e outras ferramentas, com configuração zero necessária, embora possa ser personalizado.

Principais recursos:
- **Linter**: Detecta erros de código, estilo e complexidade.
- **Formatador**: Formata código de forma compatível com Black.
- **Velocidade**: Muito rápido devido ao Rust.
- **Integração**: Pode ser usado via CLI, pre-commit hooks, GitHub Actions, ou como servidor de linguagem para IDEs.

## Instalação

Ruff está incluído como dependência de desenvolvimento no projeto. Para instalar todas as dependências, execute:

```bash
uv sync
```

Isso instalará o Ruff junto com outras dependências dev.

Para instalar manualmente (se necessário):

```bash
pip install ruff
```

Ou via uv:

```bash
uv add --dev ruff
```

## Configuração no Projeto

A configuração do Ruff está definida no arquivo `pyproject.toml`. Aqui está um resumo das configurações atuais:

### Configurações Gerais
```toml
[tool.ruff]
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "logs",
    ".pytest_cache",
    "alembic",
]
line-length = 88
indent-width = 4
target-version = "py312"
```

- **exclude**: Diretórios e arquivos ignorados pelo Ruff.
- **line-length**: Comprimento máximo da linha (compatível com Black).
- **indent-width**: Largura da indentação.
- **target-version**: Versão alvo do Python (3.12).

### Configurações de Linting
```toml
[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP", "SIM"]
ignore = ["E501"]
fixable = ["ALL"]
unfixable = ["B"]
```

- **select**: Regras habilitadas:
  - `E4`, `E7`, `E9`: Regras do pycodestyle (PEP 8).
  - `F`: Pyflakes (erros de sintaxe).
  - `B`: flake8-bugbear (bugs comuns).
  - `I`: isort (organização de imports).
  - `UP`: pyupgrade (atualização de sintaxe).
  - `SIM`: flake8-simplify (simplificações).
- **ignore**: Regras ignoradas (ex.: `E501` para comprimento de linha).
- **fixable**: Permite correção automática para todas as regras.
- **unfixable**: Regras que não podem ser corrigidas automaticamente (ex.: algumas de bugbear).

### Configurações de Formatação
```toml
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
docstring-code-format = true
```

- **quote-style**: Usar aspas duplas (compatível com Black).
- **indent-style**: Indentar com espaços.
- **line-ending**: Detectar automaticamente finais de linha.
- **docstring-code-format**: Formatar código em docstrings.

## Como Usar o Ruff

### Verificar o Código (Linting)
Para verificar problemas de linting em todo o projeto:

```bash
uv run ruff check .
```

Para verificar arquivos específicos:

```bash
uv run ruff check path/to/file.py
```

### Corrigir Automaticamente
Para corrigir problemas fixáveis automaticamente:

```bash
uv run ruff check --fix .
```

Isso organizará imports, removerá imports não utilizados, etc.

### Formatar o Código
Para formatar o código de acordo com as regras:

```bash
uv run ruff format .
```

### Outros Comandos Úteis
- **Ver diferenças**: `uv run ruff check --diff .`
- **Estatísticas**: `uv run ruff check --statistics .`
- **Saídas específicas**: `uv run ruff check --output-format json .`
- **Modo watch**: `uv run ruff check --watch .` (re-executa ao detectar mudanças).

## Integração com Editores

### VS Code
Instale a extensão "Ruff" do marketplace. Ela fornece:
- Diagnósticos em tempo real.
- Correção automática ao salvar.
- Formatação integrada.

Certifique-se de que o Ruff esteja instalado no ambiente virtual.

### Outros Editores
Ruff pode ser integrado via pre-commit hooks ou servidores de linguagem. Consulte a documentação oficial para mais detalhes.

## Pre-commit Hooks
Para integrar Ruff em pre-commit hooks, adicione ao `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.x.x
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Boas Práticas
- Execute `ruff check --fix .` e `ruff format .` antes de commits.
- Use `ruff check --statistics .` para monitorar a qualidade do código.
- Personalize as regras em `pyproject.toml` conforme necessário para o projeto.
- Ignore arquivos gerados ou de terceiros na configuração `exclude`.

Para mais informações, consulte a documentação oficial: https://docs.astral.sh/ruff/