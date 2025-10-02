# Teams-Intercom Integration DevContainer

Este diretório contém a configuração completa do DevContainer para o projeto Teams-Intercom Integration.

## 📁 Estrutura

```
.devcontainer/
├── devcontainer.json    # Configuração principal do container
├── post-create.sh       # Script executado após criação do container
├── post-start.sh        # Script executado a cada inicialização
├── dotfiles/           # Configurações personalizadas do shell
│   ├── .bashrc         # Configuração do Bash
│   └── .zshrc          # Configuração do ZSH
└── README.md           # Este arquivo
```

## 🚀 Funcionalidades Incluídas

### 🐍 **Desenvolvimento Python**
- Python 3.11 com pip, setuptools e wheel
- Virtual environment automático
- Extensões VS Code para Python, debugging e linting
- Ferramentas de formatação: Black, isort
- Linting: Flake8, Pylint, Ruff
- Type checking: MyPy
- Testing: pytest com coverage
- Security: Bandit, Safety

### 🔧 **Ferramentas de Desenvolvimento**
- **GitHub CLI** - Para integração completa com GitHub
- **Git** com configuração automática
- **Docker** - Para containerização
- **Pre-commit hooks** - Para qualidade de código
- **ZSH + Oh My Zsh** - Shell aprimorado

### 📊 **VS Code Extensões**
- **Python Development:** Python, Pylint, Black, isort, MyPy
- **Git & GitHub:** GitLens, GitHub Actions, Pull Requests
- **API Development:** Thunder Client, REST Client
- **Code Quality:** Ruff, YAML, TOML support
- **Documentation:** Markdown tools
- **Azure & Microsoft Graph:** Azure CLI, Azure Functions

### 🔨 **Automação**
- **Make commands** para tarefas comuns
- **Tasks.json** configurado para VS Code
- **Launch.json** para debugging
- **Aliases** úteis para desenvolvimento
- **Auto-ativação** do ambiente virtual

## 🎯 **Comandos Úteis**

### Make Commands
```bash
make help       # Mostrar todos os comandos
make install    # Instalar dependências
make dev        # Executar servidor de desenvolvimento
make test       # Executar testes
make lint       # Executar linting
make format     # Formatar código
make typecheck  # Verificação de tipos
make security   # Verificações de segurança
make clean      # Limpar arquivos de cache
```

### Aliases Personalizados
```bash
# Python
py              # python
pip             # python -m pip
pytest          # python -m pytest

# Git
gs              # git status
ga              # git add
gc              # git commit
gp              # git push
gl              # git pull
gd              # git diff

# Projeto
rundev          # uvicorn main:app --reload
runprod         # python main.py
test            # pytest -v
testcov         # pytest com coverage
lint            # flake8 + pylint
format          # black + isort
typecheck       # mypy
security        # bandit + safety
```

### Funções Especiais
```bash
project_status  # Mostrar status do projeto
reload          # Recarregar configurações do shell
```

## 🔧 **Configuração Automática**

### **Scripts de Inicialização**

#### `post-create.sh`
Executado uma vez após a criação do container:
- Instala dependências do sistema
- Configura Python e ferramentas de desenvolvimento
- Instala dependências do projeto
- Configura pre-commit hooks
- Cria configurações do VS Code
- Configura aliases e funções úteis

#### `post-start.sh`
Executado a cada inicialização do container:
- Ativa ambiente virtual
- Verifica configurações
- Mostra status do projeto
- Exibe comandos úteis

### **Portas Configuradas**
- **8000** - FastAPI Application (principal)
- **8080** - Servidor web alternativo
- **3000** - Desenvolvimento frontend
- **5000** - Flask/Debug server

### **Volumes e Mounts**
- Workspace completo montado
- Dotfiles personalizados
- Cache do Git e Python persistente

## 🛠️ **Configurações do VS Code**

### **Debugging**
- Configuração para FastAPI
- Debug de arquivo atual
- Debug de testes pytest

### **Tasks**
- Instalar dependências
- Executar testes
- Formatar código
- Linting e type checking
- Executar servidor de desenvolvimento

### **Settings**
- Formatação automática com Black
- Organizacão automática de imports
- Linting habilitado
- Type checking configurado
- Exclusões apropriadas de arquivos

## 🔐 **Segurança**

### **Pre-commit Hooks**
- Formatação de código
- Linting
- Verificação de segurança
- Validação de arquivos

### **Ferramentas de Segurança**
- **Bandit** - Análise de segurança Python
- **Safety** - Verificação de vulnerabilidades
- **Validação** de webhooks e assinaturas

## 📚 **Como Usar**

### **1. Abrir no DevContainer**
1. Abra o projeto no VS Code
2. Clique em "Reopen in Container" quando solicitado
3. Ou use `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

### **2. Configurar Ambiente**
1. Edite o arquivo `.env` com suas credenciais
2. Execute `make install` para instalar dependências
3. Execute `make dev` para iniciar o servidor

### **3. Desenvolvimento**
1. Use `make help` para ver comandos disponíveis
2. Use `project_status` para verificar o status
3. Aproveite as funcionalidades automáticas do VS Code

## 🎉 **Benefícios**

### **✅ Ambiente Consistente**
- Mesmo ambiente para toda a equipe
- Dependências versionadas
- Configurações padronizadas

### **✅ Produtividade**
- Aliases e comandos úteis
- Debugging configurado
- Formatação automática
- Linting em tempo real

### **✅ Qualidade de Código**
- Pre-commit hooks
- Testes automatizados
- Verificações de segurança
- Type checking

### **✅ Integração GitHub**
- GitHub CLI configurado
- Extensions para Pull Requests
- GitHub Actions support
- GitLens para análise de código

## 🔄 **Customização**

Para personalizar o ambiente:

1. **Adicionar extensões:** Edite `devcontainer.json`
2. **Modificar aliases:** Edite arquivos em `dotfiles/`
3. **Adicionar ferramentas:** Edite `post-create.sh`
4. **Configurar VS Code:** Edite seção `customizations`

## 📞 **Suporte**

Se você encontrar problemas:
1. Verifique os logs do container
2. Execute `project_status` para diagnóstico
3. Reconstrua o container se necessário
4. Consulte a documentação do DevContainers

---

**Desenvolvido com ❤️ para máxima produtividade em Python!** 🚀