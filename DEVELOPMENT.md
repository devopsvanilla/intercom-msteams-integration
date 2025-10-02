# 🛠️ Guia de Desenvolvimento - Teams-Intercom Integration

Este documento contém todas as informações essenciais para desenvolver com eficiência no projeto Teams-Intercom Integration.

## 🚀 Início Rápido

### 1. **Configuração Inicial**
```bash
# 1. Copiar arquivo de ambiente
cp .env.example .env

# 2. Editar credenciais (OBRIGATÓRIO)
code .env

# 3. Instalar dependências
make install

# 4. Executar servidor de desenvolvimento
make dev
```

### 2. **Verificar Status**
```bash
# Verificar status do projeto
project_status

# Verificar se tudo está funcionando
make test
```

## 🎯 Comandos Essenciais

### **Make Commands (Principais)**
```bash
make help       # 📚 Mostrar todos os comandos disponíveis
make install    # 📦 Instalar todas as dependências
make dev        # 🚀 Executar servidor de desenvolvimento (porta 8000)
make test       # 🧪 Executar todos os testes
make testcov    # 📊 Executar testes com coverage HTML
make lint       # 🔍 Executar linting (flake8 + pylint)
make format     # ✨ Formatar código (black + isort)
make typecheck  # 🔤 Verificação de tipos (mypy)
make security   # 🔒 Análise de segurança (bandit + safety)
make clean      # 🧹 Limpar arquivos de cache
```

### **Aliases Úteis**

#### **Python Development**
```bash
py              # python
pip             # python -m pip
pytest          # python -m pytest
black           # python -m black
isort           # python -m isort
flake8          # python -m flake8
mypy            # python -m mypy
```

#### **Git Workflow**
```bash
gs              # git status
ga              # git add
gc              # git commit
gp              # git push
gl              # git pull
gd              # git diff
gb              # git branch
gco             # git checkout
glog            # git log --oneline --graph --decorate --all
```

#### **Projeto Específico**
```bash
rundev          # uvicorn main:app --reload --host 0.0.0.0 --port 8000
runprod         # python main.py
test            # pytest -v
testcov         # pytest -v --cov=. --cov-report=html
lint            # flake8 . && pylint *.py
format          # black . && isort .
typecheck       # mypy .
security        # bandit -r . && safety check
```

#### **Docker & Utilities**
```bash
d               # docker
dc              # docker-compose
dps             # docker ps
di              # docker images
dex             # docker exec -it

reload          # source ~/.bashrc ou ~/.zshrc
h               # history
c               # clear
path            # echo -e ${PATH//:/\\n}
ports           # netstat -tuln
json            # python -m json.tool
```

## 🔧 Ferramentas de Desenvolvimento

### **VS Code - Extensões Instaladas**
```
🐍 Python Development:
- ms-python.python              # Python support
- ms-python.flake8              # Linting
- ms-python.pylint              # Linting avançado
- ms-python.black-formatter     # Formatação
- ms-python.isort               # Organização imports
- ms-python.mypy-type-checker   # Type checking
- charliermarsh.ruff            # Linter rápido

🧪 Testing & Debugging:
- ms-toolsai.jupyter            # Jupyter notebooks
- ms-vscode.live-server         # Live server

🔗 Git & GitHub:
- eamodio.gitlens               # Git enhanced
- github.vscode-pull-request-github
- github.copilot                # AI assistant
- github.copilot-chat           # AI chat

🌐 API Development:
- humao.rest-client             # REST testing
- rangav.vscode-thunder-client  # API client

☁️ Azure & Cloud:
- ms-vscode.azurecli            # Azure CLI
- ms-azuretools.vscode-azureresourcegroups
```

### **Debugging Configurado**
```json
// Configurações disponíveis no VS Code
{
    "Python: FastAPI",          // Debug da aplicação principal
    "Python: Current File",     // Debug do arquivo atual
    "Python: Pytest"           // Debug dos testes
}
```

### **Tasks Configuradas**
```
- Install Dependencies    # pip install -r requirements.txt
- Run Tests              # pytest -v
- Format Code            # black .
- Sort Imports           # isort .
- Lint Code              # flake8 .
- Type Check             # mypy .
- Run FastAPI Dev        # uvicorn main:app --reload
```

## 📂 Estrutura do Projeto

### **Arquivos Principais**
```
📁 intercom-msteams-integration/
├── 🔧 config.py              # Configurações e env vars
├── 📊 graph_client.py        # Cliente Microsoft Graph
├── 💬 intercom_client.py     # Cliente Intercom API
├── 🎣 webhook_handler.py     # Processador webhooks
├── 🚀 main.py               # Aplicação FastAPI
├── 🧪 test_integration.py   # Testes unitários
├── 📋 requirements.txt      # Dependências Python
├── 🔐 .env.example         # Exemplo variáveis ambiente
└── 📚 README.md            # Documentação principal
```

### **DevContainer**
```
📁 .devcontainer/
├── 🐳 devcontainer.json     # Configuração container
├── 🔧 post-create.sh        # Setup inicial
├── ⚡ post-start.sh         # Inicialização
├── 📚 README.md            # Docs devcontainer
└── 📁 dotfiles/
    ├── .bashrc             # Config Bash
    └── .zshrc              # Config ZSH
```

## 🔄 Workflow de Desenvolvimento

### **1. Preparação**
```bash
# Ativar ambiente (automático no devcontainer)
source .venv/bin/activate

# Verificar status
project_status

# Instalar/atualizar dependências
make install
```

### **2. Desenvolvimento**
```bash
# Executar servidor de desenvolvimento
make dev

# Em outro terminal: executar testes
make test

# Formatar código antes de commit
make format

# Verificar qualidade
make lint
make typecheck
make security
```

### **3. Commit**
```bash
# Pre-commit hooks executam automaticamente
git add .
git commit -m "feat: nova funcionalidade"
git push
```

### **4. Debugging**

#### **Via VS Code**
1. Abrir arquivo Python
2. Colocar breakpoints
3. F5 ou Debug → Start Debugging
4. Escolher configuração:
   - **Python: FastAPI** - Para debug da aplicação
   - **Python: Current File** - Para debug do arquivo atual
   - **Python: Pytest** - Para debug de testes

#### **Via Terminal**
```bash
# Debug com pdb
python -m pdb main.py

# Debug de testes específicos
pytest -v -s test_integration.py::TestGraphClient::test_authentication_success
```

## 🧪 Testes

### **Executar Testes**
```bash
# Todos os testes
make test

# Testes com coverage
make testcov

# Testes específicos
pytest test_integration.py -v

# Teste de uma classe específica
pytest test_integration.py::TestGraphClient -v

# Teste de um método específico
pytest test_integration.py::TestGraphClient::test_authentication_success -v

# Testes em modo watch (reexecuta ao salvar)
pytest-watch
```

### **Coverage Report**
```bash
# Gerar relatório HTML
make testcov

# Abrir relatório
open htmlcov/index.html
```

## 🔍 Qualidade de Código

### **Linting**
```bash
# Executar todos os linters
make lint

# Linters individuais
flake8 .                    # Style guide
pylint *.py                 # Code analysis
ruff check .                # Fast linter
bandit -r .                 # Security
```

### **Formatação**
```bash
# Formatar tudo
make format

# Formatadores individuais
black .                     # Code formatter
isort .                     # Import organizer
```

### **Type Checking**
```bash
# Verificação de tipos
make typecheck

# MyPy com mais detalhes
mypy . --show-error-codes
```

### **Segurança**
```bash
# Análise de segurança
make security

# Ferramentas individuais
bandit -r .                 # Security linter
safety check                # Vulnerability check
```

## 🌐 APIs e Endpoints

### **Endpoints Principais**
```bash
# Health Check
curl http://localhost:8000/

# Status detalhado
curl http://localhost:8000/health

# Listar Teams
curl http://localhost:8000/teams

# Webhooks Intercom
curl -X POST http://localhost:8000/webhooks/intercom \
  -H "Content-Type: application/json" \
  -d '{"topic": "conversation.user.created", "data": {...}}'
```

### **Testing APIs**

#### **Thunder Client (VS Code)**
1. Abrir Thunder Client
2. Criar nova requisição
3. Usar http://localhost:8000

#### **REST Client (VS Code)**
Criar arquivo `.http`:
```http
### Health Check
GET http://localhost:8000/

### Get Teams
GET http://localhost:8000/teams

### Send Message
POST http://localhost:8000/teams/{{team_id}}/channels/{{channel_id}}/messages
Content-Type: application/json

{
    "message": "Hello from API!",
    "type": "html"
}
```

## 🔐 Configuração de Ambiente

### **Variáveis Obrigatórias (.env)**
```bash
# Azure AD Configuration
AZURE_CLIENT_ID=your-azure-app-client-id
AZURE_CLIENT_SECRET=your-azure-app-client-secret
AZURE_TENANT_ID=your-azure-tenant-id

# Intercom Configuration
INTERCOM_ACCESS_TOKEN=your-intercom-access-token
INTERCOM_WEBHOOK_SECRET=your-intercom-webhook-secret

# Teams Integration
DEFAULT_TEAM_ID=your-default-teams-team-id
DEFAULT_CHANNEL_NAME=Customer Support
```

### **Variáveis Opcionais**
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Webhook Configuration
WEBHOOK_PATH=/webhooks/intercom

# Azure Redirect
AZURE_REDIRECT_URI=http://localhost:8000/auth/callback
```

## 🚨 Troubleshooting

### **Problemas Comuns**

#### **1. Erro de Autenticação Azure**
```bash
# Verificar variáveis
grep AZURE .env

# Testar credenciais
python -c "from config import config; print(config.azure.client_id)"
```

#### **2. Dependências Não Instaladas**
```bash
# Reinstalar tudo
make clean
make install

# Verificar virtual environment
which python
echo $VIRTUAL_ENV
```

#### **3. Servidor Não Inicia**
```bash
# Verificar porta em uso
ports

# Matar processos
pkill -f uvicorn

# Executar em porta diferente
uvicorn main:app --port 8001
```

#### **4. Testes Falhando**
```bash
# Verificar environment de teste
cat .env.test

# Executar teste específico com mais detalhes
pytest test_integration.py::test_name -v -s
```

### **Logs e Debug**
```bash
# Logs da aplicação
tail -f logs/app.log

# Debug mode
DEBUG=true make dev

# Verbose logging
PYTHONPATH=. python main.py --log-level debug
```

## 📚 Recursos Úteis

### **Documentação**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)
- [Intercom API](https://developers.intercom.com/)
- [Pytest Documentation](https://docs.pytest.org/)

### **Comandos de Referência Rápida**
```bash
# Status geral
project_status

# Ajuda
make help

# Desenvolvimento rápido
make format && make test && make dev

# Deploy checklist
make lint && make typecheck && make security && make test
```

### **Função Útil: project_status**
```bash
# Mostra status completo do projeto
project_status

# Output exemplo:
🚀 Teams-Intercom Integration Status:
✅ Virtual environment: .venv
✅ Environment file: Found
✅ Dependencies: Installed
✅ Git repository: main
✅ Working directory: Clean
```

## 🎯 Dicas de Produtividade

### **1. Atalhos do VS Code**
- `Ctrl+Shift+P` - Command Palette
- `F5` - Start Debugging
- `Ctrl+`` ` - Toggle Terminal
- `Ctrl+Shift+E` - Explorer
- `Ctrl+Shift+G` - Git

### **2. Git Workflow**
```bash
# Branch feature
git checkout -b feature/nova-funcionalidade

# Commit com convenção
git commit -m "feat: adicionar nova funcionalidade"
git commit -m "fix: corrigir bug authentication"
git commit -m "docs: atualizar documentation"
```

### **3. Desenvolvimento Eficiente**
```bash
# Terminal multiplex
make dev &          # Servidor em background
make test           # Testes em foreground

# Watch mode para testes
pytest-watch

# Hot reload sempre ativo
uvicorn main:app --reload
```

### **4. Debugging Avançado**
```python
# Breakpoint no código
import pdb; pdb.set_trace()

# Logging estruturado
import structlog
logger = structlog.get_logger(__name__)
logger.info("Debug info", extra_data=data)
```

---

**💡 Dica:** Use `make help` sempre que precisar lembrar dos comandos disponíveis!

**🚀 Happy Coding!** Desenvolvido com ❤️ por DevOps Vanilla