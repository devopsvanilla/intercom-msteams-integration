# 🔒 Segurança e .gitignore - Teams-Intercom Integration

## 📋 Resumo

Este projeto utiliza um `.gitignore` abrangente e seguro baseado nos padrões oficiais do GitHub e melhores práticas de segurança para:

- **Python/FastAPI** (backend)
- **Node.js/React/Vite** (frontend)
- **Docker/Dev Containers** (desenvolvimento)
- **Azure/Microsoft Graph** (cloud APIs)
- **VS Code** (IDE)

## 🛡️ Arquivos Sensíveis Protegidos

### Credenciais e Configurações

- `.env*` - Variáveis de ambiente com tokens e secrets
- `config.json` - Arquivos de configuração com dados sensíveis
- `secrets.json` - Arquivos de secrets
- `*.key`, `*.pem`, `*.crt` - Chaves e certificados
- `.azure/` - Configurações da Azure CLI

### Específicos do Projeto

- `config/teams_channels_config.json` - Configurações de equipes
- `intercom_secret.txt` - Segredos do webhook Intercom
- `manifest.json` - Manifesto da aplicação Teams

## 🔧 Tecnologias e Padrões Utilizados

### 🐍 Python/FastAPI

Baseado no [template oficial Python do GitHub](https://github.com/github/gitignore/blob/main/Python.gitignore):

- `__pycache__/`, `*.pyc` - Arquivos compilados
- `.venv/`, `venv/` - Ambientes virtuais
- `.pytest_cache/`, `.coverage` - Arquivos de teste
- `.mypy_cache/` - Cache do type checker
- `dist/`, `build/` - Arquivos de distribuição

### ⚛️ Node.js/React/Vite

Baseado no [template oficial Node.js do GitHub](https://github.com/github/gitignore/blob/main/Node.gitignore):

- `node_modules/` - Dependências
- `dist/`, `.cache` - Arquivos de build
- `*.log` - Logs
- `.env.local` - Variáveis locais

### 🐳 Docker

- `docker-compose.override.yml` - Overrides locais
- `Dockerfile.local` - Dockerfiles de desenvolvimento

### 💻 VS Code/IDEs

- `.vscode/` - Configurações pessoais do VS Code
- `.idea/` - Configurações do IntelliJ/PyCharm
- `*.swp`, `*.swo` - Arquivos temporários do Vim

## 📁 Estrutura de Arquivos Ignorados

```text
/
├── .env                          # ❌ Credenciais (IGNORADO)
├── .env.example                  # ✅ Template (VERSIONADO)
├── .venv/                        # ❌ Ambiente virtual (IGNORADO)
├── __pycache__/                  # ❌ Cache Python (IGNORADO)
├── node_modules/                 # ❌ Dependências JS (IGNORADO)
├── dist/                         # ❌ Build frontend (IGNORADO)
├── .vscode/                      # ❌ Configurações pessoais (IGNORADO)
├── config/
│   ├── teams_channels_config.json # ❌ Config com IDs (IGNORADO)
│   └── config.example.json       # ✅ Template (VERSIONADO)
├── logs/                         # ❌ Logs (IGNORADO)
└── temp/                         # ❌ Temporários (IGNORADO)
```

## 🚨 Arquivos Críticos para Proteger

### ⚠️ **NUNCA** versionar

1. **`.env`** - Contém:

   - `AZURE_CLIENT_SECRET`
   - `INTERCOM_ACCESS_TOKEN`
   - `INTERCOM_WEBHOOK_SECRET`

1. **Configurações com IDs reais**:

   - `config/teams_channels_config.json`
   - Qualquer arquivo com Team IDs ou Channel IDs reais

1. **Logs de produção**:

   - Podem conter dados de usuários
   - Tokens em plain text
   - Informações de debugging

### ✅ **Sempre** versionar

1. **Templates**:

   - `.env.example`
   - `config.example.json`

1. **Configurações de desenvolvimento**:

   - `.gitignore`
   - `requirements.txt`
   - `package.json`

## 🔍 Verificação de Segurança

### Comandos para verificar vazamentos

```bash
# Verificar se .env está sendo ignorado
git status --ignored

# Procurar por possíveis secrets em commits
git log --all --grep="password\|secret\|token\|key"

# Verificar arquivos não rastreados
git ls-files --others --ignored --exclude-standard

# Procurar por padrões sensíveis
grep -r "password\|secret\|token" . --exclude-dir=.git --exclude-dir=.venv
```

### Ferramentas recomendadas

- **git-secrets** - Previne commits de secrets
- **truffleHog** - Encontra secrets em repositórios
- **bandit** - Scanner de segurança Python (já incluído)

## 🛠️ Como usar

### 1. Verificar se o .gitignore está funcionando

```bash
# Criar arquivo de teste sensível
echo "AZURE_CLIENT_SECRET=test" > .env.test

# Verificar se está sendo ignorado
git status

# Limpar
rm .env.test
```

### 2. Adicionar novos padrões

```bash
# Editar .gitignore
echo "# Novos arquivos específicos do projeto" >> .gitignore
echo "custom_secrets/" >> .gitignore
```

### 3. Verificar arquivos já rastreados

```bash
# Se um arquivo sensível já foi commitado anteriormente
git rm --cached .env
git commit -m "Remove .env from tracking"
```

## 📚 Referências

- [GitHub .gitignore Templates](https://github.com/github/gitignore)
- [Python .gitignore Official](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Node.js .gitignore Official](https://github.com/github/gitignore/blob/main/Node.gitignore)
- [OWASP Secret Management](https://owasp.org/www-community/controls/SecretManagement)
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)

## ✅ Validação

Este `.gitignore` foi criado seguindo:

- ✅ Padrões oficiais do GitHub
- ✅ Melhores práticas de segurança OWASP
- ✅ Específico para as tecnologias do projeto
- ✅ Proteção contra vazamento de credenciais
- ✅ Compatível com ferramentas de CI/CD
