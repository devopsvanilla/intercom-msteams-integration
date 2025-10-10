# Teams-Intercom Integration - Guia Dev Container

## 🎯 Por que usar Dev Containers?

Este guia permite configurar um ambiente de desenvolvimento **completo, consistente e isolado** em segundos, garantindo que todos os desenvolvedores trabalhem com exatamente as mesmas versões de ferramentas, dependências e configurações.

### ✅ Vantagens

- **Ambiente idêntico** para toda a equipe
- **Setup automático** em minutos, não horas
- **Isolamento completo** - não afeta seu sistema local
- **Produtividade máxima** com ferramentas pré-configuradas
- **Zero conflitos** de dependências
- **Debugging** já configurado

---

## 🛠️ O que será instalado e configurado

### 🐍 Python & Dependências

- **Python 3.11** com pip, setuptools, wheel
- **Ambiente virtual** automático (.venv)
- **Todas as dependências** do projeto (FastAPI, Azure SDK, Microsoft Graph, etc.)

### 🔧 Ferramentas de Desenvolvimento

- **Formatação:** Black, isort
- **Linting:** Flake8, Pylint, Ruff, MyPy
- **Testes:** pytest, pytest-asyncio, coverage
- **Segurança:** Bandit, Safety
- **Pre-commit hooks** automáticos

### 📊 VS Code - Extensões e Configurações

- **Python Development:** Debugging, IntelliSense, formatação automática
- **Git & GitHub:** GitLens, GitHub Actions, Pull Requests, Copilot
- **API Development:** Thunder Client, REST Client
- **Azure & Microsoft Graph:** Azure CLI, extensões específicas
- **Code Quality:** Linting em tempo real, type checking
- **Documentation:** Markdown tools avançados

### 🌟 Ferramentas do Sistema

- **GitHub CLI (gh)** - Integração completa com GitHub
- **Docker-in-Docker** - Para desenvolvimento de containers
- **Git** versão mais recente
- **ZSH + Oh My Zsh** - Shell otimizado
- **Utilitários:** curl, wget, jq, tree, htop

### ⚙️ Configurações Automáticas

- **Tasks VS Code** para comandos comuns
- **Launch configurations** para debugging
- **Aliases úteis** para desenvolvimento
- **Makefile** com comandos padronizados
- **Port forwarding** automático (8000, 3000, 5000, 8080)

---

## 🚀 Como configurar o ambiente

### Pré-requisitos

- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/devopsvanilla/intercom-msteams-integration.git
cd intercom-msteams-integration
```

### Passo 2: Abrir no VS Code

```bash
code .
```

### Passo 3: Abrir no Dev Container

Quando o VS Code abrir, você verá uma notificação:
**"Reopen in Container"** - clique nela

**OU** use o comando:

- `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
- Digite: `Dev Containers: Reopen in Container`
- Pressione Enter

### Passo 4: Aguardar a configuração

O container será construído automaticamente (5-10 minutos na primeira vez).

### Passo 5: Instalar dependências

Após o container estar pronto, execute:

```bash
# Opção 1: Script conveniente
./install_deps.sh

# Opção 2: Comando make
make install

# Opção 3: Manual
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Passo 6: Configurar ambiente

```bash
# Copiar arquivo de ambiente
cp .env.example .env

# Editar com suas credenciais
code .env
```

### Passo 7: Iniciar desenvolvimento

```bash
# Servidor de desenvolvimento
make dev

# Ou manualmente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📋 Comandos úteis

### Make Commands

```bash
make help          # Mostrar todos os comandos
make install       # Instalar dependências
make dev           # Servidor de desenvolvimento
make test          # Executar testes
make lint          # Linting do código
make format        # Formatar código
make typecheck     # Verificação de tipos
make security      # Verificações de segurança
make clean         # Limpar cache
```

### Aliases Pré-configurados

```bash
# Python
py                 # python
pip                # python -m pip
pytest             # python -m pytest

# Git
gs                 # git status
ga                 # git add
gc                 # git commit
gp                 # git push
gl                 # git pull

# Projeto
rundev             # uvicorn main:app --reload
test               # pytest -v
lint               # flake8 + pylint
format             # black + isort
```

---

## 🔧 Solução de problemas

### Container não inicia

```bash
# Reconstruir o container
Ctrl+Shift+P → "Dev Containers: Rebuild Container"
```

### Problemas de dependências

```bash
# Limpar e reinstalar
make clean
make reinstall

# Ou manual
pip cache purge
pip install -r requirements.txt
```

### Problemas de permissão

```bash
# Corrigir proprietário
sudo chown -R vscode:vscode /workspaces/intercom-msteams-integration
```

### Virtual environment

```bash
# Recriar ambiente virtual
rm -rf .venv
./setup_venv.sh
```

---

## 🌍 Variáveis de ambiente

Configure no arquivo `.env`:

```env
AZURE_CLIENT_ID=seu-client-id
AZURE_CLIENT_SECRET=seu-client-secret
AZURE_TENANT_ID=seu-tenant-id
INTERCOM_ACCESS_TOKEN=seu-access-token
INTERCOM_WEBHOOK_SECRET=seu-webhook-secret
DEFAULT_TEAM_ID=seu-team-id
DEBUG=true
```

---

## 📞 Suporte

### Problemas comuns

1. **Container lento:** Primeira execução demora mais
2. **Portas ocupadas:** Verifique se outras aplicações estão usando as portas
3. **Memória insuficiente:** Aumente a memória do Docker (8GB recomendado)

### Logs úteis

```bash
# Status do projeto
project_status

# Logs do container
docker logs <container_id>
```

### Problemas de autenticação Git

Se você tiver problemas de permissão ao fazer push (erro 403), mesmo estando autenticado no GitHub CLI:

```bash
# Verificar conta ativa
gh auth status

# Mudar conta se necessário
gh auth switch

# Configurar Git para usar GitHub CLI
gh auth setup-git

# Limpar credenciais antigas em cache
echo "url=https://github.com" | git credential reject

# Se persistir, usar token diretamente (temporário)
gh auth token  # copiar o token
git credential approve <<< "protocol=https
host=github.com
username=seu-usuario-github
password=seu-token-copiado"
```

**Causa:** O Git pode manter credenciais antigas em cache, mesmo após mudança de conta no GitHub CLI.

**Prevenção:** Sempre execute `gh auth setup-git` após mudar de conta.

### Erro "fatal: empty ident name (for <>) not allowed"

Este é um problema comum em Dev Containers onde as variáveis de ambiente do Git estão vazias.

**🎯 Solução Recomendada:**

```bash
# 1. Executar o script interativo de configuração
source .devcontainer/git-config.sh
```

O script irá:

- ✅ **Detectar configuração existente** e perguntar se deseja mantê-la
- ✅ **Solicitar informações** se necessário (nome e email)
- ✅ **Validar formato do email** automaticamente
- ✅ **Configurar todas as variáveis** necessárias (autor e committer)
- ✅ **Aplicar configurações** locais e de ambiente

**🔧 Solução Rápida (se já souber suas informações):**

```bash
# Configurar diretamente as variáveis de ambiente
export GIT_AUTHOR_NAME="Seu Nome Completo"
export GIT_AUTHOR_EMAIL="seu@email.com"
export GIT_COMMITTER_NAME="Seu Nome Completo"
export GIT_COMMITTER_EMAIL="seu@email.com"

# Configurar Git localmente também
git config user.name "Seu Nome Completo"
git config user.email "seu@email.com"
```

**📋 Para verificar se está configurado:**

```bash
# Verificar configuração Git
git config --get user.name
git config --get user.email

# Verificar variáveis de ambiente
echo "Autor: $GIT_AUTHOR_NAME <$GIT_AUTHOR_EMAIL>"
echo "Committer: $GIT_COMMITTER_NAME <$GIT_COMMITTER_EMAIL>"
```

**🚀 Configuração Automática (recomendado para uso frequente):**

Adicione ao seu `~/.bashrc` ou `~/.zshrc` dentro do container:

```bash
# Executar script de configuração Git automaticamente
if [ -f "/workspaces/intercom-msteams-integration/.devcontainer/git-config.sh" ]; then
    source /workspaces/intercom-msteams-integration/.devcontainer/git-config.sh
fi
```

**❓ Por que acontece:**

- Dev Containers podem ter variáveis de ambiente Git vazias
- VS Code/Git prioriza variáveis de ambiente sobre configuração local
- O script resolve isso configurando ambos os métodos

**✨ Recursos do script `.devcontainer/git-config.sh`:**

- 🔍 Detecção automática de configuração existente
- ✉️ Validação de formato de email
- 🛡️ Confirmação antes de aplicar mudanças
- 🔧 Configuração completa (config local + variáveis de ambiente)
- 💾 Persistência para a sessão atual do container

### Reconstruir completamente

```bash
# Remover volumes e reconstruir
Ctrl+Shift+P → "Dev Containers: Rebuild Container Without Cache"
```

---

## 🎉 Próximos passos

Após o setup do Dev Container:

1. **🔧 Configurar Git:** `source .devcontainer/git-config.sh` (essencial para commits)
2. **✅ Verificar instalação:** `make test`
3. **� Configurar credenciais:** Editar arquivo `.env`
4. **🚀 Iniciar desenvolvimento:** `make dev`
5. **📚 Ler documentação:** Consultar outros READMEs do projeto

---

**🚀 Seu ambiente está pronto! Happy coding!**

> **💡 Dica importante:** Execute sempre `source .devcontainer/git-config.sh` ao abrir o Dev Container para evitar problemas de commit. O script é interativo e preserva configurações existentes.
