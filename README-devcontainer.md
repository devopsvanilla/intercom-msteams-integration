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

Se você encontrar este erro ao fazer commit:

```bash
# Executar o script de configuração do Git (recomendado)
./.devcontainer/git-config.sh

# O script irá solicitar:
# - Seu nome completo
# - Seu email (com validação automática)
# - Confirmação das informações

# Ou configurar manualmente:
export GIT_AUTHOR_NAME="Seu Nome"
export GIT_AUTHOR_EMAIL="seu@email.com"
export GIT_COMMITTER_NAME="Seu Nome"
export GIT_COMMITTER_EMAIL="seu@email.com"
git config user.name "Seu Nome"
git config user.email "seu@email.com"
```

**Causa:** Variáveis de ambiente Git vazias no VS Code sobrescrevem as configurações locais.

**Solução permanente:** Execute `./.devcontainer/git-config.sh` após abrir o container.

**Recursos do script:**

- ✅ Validação automática de email
- ✅ Verificação de configuração existente
- ✅ Confirmação antes de aplicar
- ✅ Configuração de todas as variáveis necessárias

### Reconstruir completamente

```bash
# Remover volumes e reconstruir
Ctrl+Shift+P → "Dev Containers: Rebuild Container Without Cache"
```

---

## 🎉 Próximos passos

Após o setup:

1. **✅ Verificar instalação:** `make test`
2. **🔧 Configurar credenciais:** Editar `.env`
3. **🚀 Iniciar desenvolvimento:** `make dev`
4. **📚 Ler documentação:** Consultar outros READMEs do projeto
5. **🤝 Configurar Git:** `git config --global user.name "Seu Nome"`

---

**🚀 Seu ambiente está pronto! Happy coding!**

> **Dica:** Marque este README como favorito e compartilhe com a equipe. O Dev Container garante que todos terão exatamente o mesmo ambiente de desenvolvimento.
