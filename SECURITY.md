# 🔒 Política de Segurança - Teams-Intercom Integration

## 📋 Visão Geral

Este documento descreve as medidas de segurança implementadas no projeto Teams-Intercom Integration, abrangendo desde o desenvolvimento até a implantação em produção. O projeto segue as melhores práticas de segurança para aplicações que integram serviços em nuvem.

## 🛡️ Medidas de Segurança Implementadas

### 🔐 Proteção de Credenciais e Secrets

#### Gerenciamento de Arquivos Sensíveis (.gitignore)

**Arquivos NUNCA versionados:**

- `.env*` - Variáveis de ambiente com tokens e secrets
- `config.json`, `secrets.json` - Configurações com dados sensíveis
- `*.key`, `*.pem`, `*.crt` - Chaves e certificados privados
- `.azure/` - Configurações da Azure CLI
- `config/teams_channels_config.json` - Configurações com IDs reais
- `intercom_secret.txt` - Segredos do webhook Intercom
- `logs/` - Logs que podem conter dados sensíveis

**Templates sempre versionados:**

- `.env.example`, `.env.docker` - Templates de configuração
- `config.example.json` - Exemplos de configuração
- `README*.md` - Documentação

#### Externalização de Configurações

```env
# Exemplo de configuração segura
AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}     # Não hardcoded
INTERCOM_ACCESS_TOKEN=${INTERCOM_ACCESS_TOKEN} # Via environment
REDIS_PASSWORD=${REDIS_PASSWORD:-secure-default}
```

### 🐳 Segurança em Containers Docker

#### Containers Hardening

**Medidas implementadas:**

- ✅ **Usuários não-root**: Todos os containers executam com usuários dedicados
- ✅ **Capabilities limitadas**: `CAP_DROP ALL` + apenas capabilities necessárias
- ✅ **Security options**: `no-new-privileges:true`
- ✅ **Resource limits**: CPU e memória limitados
- ✅ **Multi-stage builds**: Imagens finais mínimas

```dockerfile
# Exemplo de segurança no Dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser  # Nunca root

# No docker-compose.yml
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
cap_add:
  - CHOWN  # Apenas o necessário
```

#### Rede e Comunicação

- ✅ **Rede isolada**: Bridge network dedicada (`teams-intercom-network`)
- ✅ **Rate limiting**: Proteção contra DDoS/spam
- ✅ **Headers de segurança**: X-Frame-Options, X-XSS-Protection, etc.
- ✅ **CORS configurado**: Origens permitidas controladas

```nginx
# Headers de segurança no Nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

#### Volumes e Persistência

- ✅ **Volumes externos**: Dados persistentes fora dos containers
- ✅ **Backup automatizado**: Script de backup incluído
- ✅ **Permissões controladas**: Ownership correto nos volumes

### 🌐 Segurança da API e Webhooks

#### Autenticação e Autorização

**Microsoft Graph API:**

- ✅ **Client Credentials Flow**: Autenticação segura para aplicações
- ✅ **Permissions mínimas**: Apenas permissões necessárias
- ✅ **Token rotation**: Renovação automática de tokens
- ✅ **Tenant isolation**: Isolamento por tenant Azure

**Intercom Webhooks:**

- ✅ **Signature validation**: HMAC SHA-256 verification
- ✅ **Secret rotation**: Suporte para rotação de secrets
- ✅ **Request validation**: Validação rigorosa de payload

```python
# Validação de webhook segura
def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

#### Rate Limiting e Proteção DDoS

```nginx
# Rate limiting no Nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=webhook:10m rate=5r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
}
```

### 🔍 Logging e Monitoramento

#### Logs Estruturados

- ✅ **Structured logging**: JSON format para análise
- ✅ **Correlation IDs**: Rastreamento de requests
- ✅ **Sanitização**: Remoção de dados sensíveis dos logs
- ✅ **Retention policy**: Rotação automática de logs

```python
# Logging seguro
logger.info("User authenticated", extra={
    "user_id": "masked_id",  # ID mascarado
    "tenant": tenant_id,
    "action": "auth_success"
    # Nunca logar tokens/passwords
})
```

#### Health Checks e Alertas

- ✅ **Health endpoints**: Monitoramento contínuo
- ✅ **Dependency checks**: Verificação de serviços externos
- ✅ **Graceful degradation**: Falhas controladas

### 🚀 Segurança na Implantação

#### Ambiente de Produção

**Checklist de segurança:**

- ✅ HTTPS obrigatório com certificados válidos
- ✅ Firewall configurado (apenas portas necessárias)
- ✅ Secrets via Azure Key Vault ou equivalent
- ✅ Network policies restritivas
- ✅ Backup e disaster recovery

#### CI/CD Pipeline

```yaml
# Exemplo de verificações no pipeline
security-scan:
  - bandit: Python security linting
  - safety: Vulnerability scanning
  - docker-scout: Container image scanning
  - secrets-scan: Secret detection
```

## 🔒 Configuração Segura

### Variáveis de Ambiente Obrigatórias

```env
# Azure AD (obrigatório)
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=secure-secret-here  # Pelo menos 32 chars
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Intercom (obrigatório)
INTERCOM_ACCESS_TOKEN=secure-token-here
INTERCOM_WEBHOOK_SECRET=secure-webhook-secret  # Pelo menos 32 chars

# Security settings
CORS_ORIGINS=https://yourdomain.com  # Nunca usar *
REDIS_PASSWORD=strong-redis-password  # Pelo menos 16 chars
DEBUG=false  # SEMPRE false em produção
```

### Princípio do Menor Privilégio

**Permissões Microsoft Graph (mínimas necessárias):**

```text
✅ User.Read.All          # Leitura básica de usuários
✅ Team.ReadBasic.All     # Leitura básica de teams
✅ Channel.ReadBasic.All  # Leitura básica de canais
✅ ChannelMessage.Send    # Envio de mensagens apenas
❌ *.ReadWrite.All       # Evitar permissões amplas
❌ Directory.ReadWrite   # Desnecessário
```

## 🚨 Relatando Problemas de Segurança

### GitHub Security Advisories

Para relatar vulnerabilidades de segurança, use o sistema oficial do GitHub:

#### 1. **Private Vulnerability Reporting**

1. **Acesse a aba Security**:
   - Vá para: `github.com/devopsvanilla/intercom-msteams-integration`
   - Clique em **"Security"** no menu superior

2. **Report a vulnerability**:
   - Clique em **"Report a vulnerability"**
   - Ou acesse: `/security/advisories/new`

3. **Preencha o formulário**:

   ```text
   Title: [CVE] Descrição concisa da vulnerabilidade

   Description:
   - Tipo de vulnerabilidade (SQL Injection, XSS, etc.)
   - Componente afetado
   - Versão(s) afetada(s)
   - Impacto potencial
   - Passos para reproduzir
   - Evidências (screenshots, logs)

   Severity: Critical/High/Medium/Low

   CVSS Score: Se disponível
   ```

#### 2. **Security Policy Compliance**

**O que reportar:**

- ✅ Vulnerabilidades de código
- ✅ Dependências vulneráveis
- ✅ Configurações inseguras
- ✅ Vazamentos de dados
- ✅ Problemas de autenticação/autorização

**O que NÃO reportar como segurança:**

- ❌ Bugs funcionais normais
- ❌ Requests de features
- ❌ Problemas de performance
- ❌ Questões de usabilidade

#### 3. **Timeline Esperado**

- **Reconhecimento**: 2 dias úteis
- **Avaliação inicial**: 5 dias úteis
- **Fix desenvolvido**: Conforme criticidade
  - Critical: 7 dias
  - High: 14 dias
  - Medium: 30 dias
  - Low: 90 dias
- **Divulgação pública**: Após fix aplicado

#### 4. **Contato Alternativo**

Se o GitHub Security não estiver disponível:

```text
Email: security@devopsvanilla.com
Subject: [SECURITY] Teams-Intercom Integration - [CRITICIDADE]

Incluir:
- Descrição detalhada
- Evidências
- Sugestões de mitigação
- Sua informação de contato para follow-up
```

### Responsible Disclosure

**Compromisso do projeto:**

- ✅ Resposta rápida e transparente
- ✅ Créditos ao reporter (se desejado)
- ✅ Coordenação para divulgação responsável
- ✅ Patches prioritários para questões críticas

**Pedimos aos pesquisadores:**

- 🤝 Reporte privadamente primeiro
- 🤝 Aguarde nossa resposta antes da divulgação pública
- 🤝 Forneça detalhes suficientes para reprodução
- 🤝 Evite acessar dados de produção

## 🔧 Ferramentas de Segurança e Pre-commit

### 🛠️ Pre-commit Hooks Implementados

O projeto utiliza um conjunto abrangente de verificações automáticas de qualidade e segurança executadas antes de cada commit:

#### **Verificações de Qualidade de Código**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace      # Remove espaços em branco
      - id: end-of-file-fixer       # Linha em branco no final
      - id: check-yaml              # Valida sintaxe YAML
      - id: check-json              # Valida sintaxe JSON
      - id: check-added-large-files # Bloqueia arquivos grandes
      - id: debug-statements        # Detecta debug prints
      - id: check-merge-conflict    # Detecta conflitos merge
```

#### **Formatação e Linting**

```yaml
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black                   # Formatação Python
        language_version: python3.12

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort                   # Organização de imports
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8                  # Linting Python
        args: [--max-line-length=88, --extend-ignore=E203]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.280
    hooks:
      - id: ruff                    # Linter moderno Python
        args: [--fix, --exit-non-zero-on-fix]
```

#### **Análise de Segurança Automática**

```yaml
  - repo: local
    hooks:
      - id: bandit                  # Análise de segurança Python
        name: bandit
        entry: bandit
        language: system
        args: ['-r', '.']
        types: [python]
```

### 🚀 Como Usar os Pre-commit Hooks

```bash
# 1. Instalar pre-commit (já incluído no dev container)
pip install pre-commit

# 2. Instalar hooks no repositório
pre-commit install

# 3. Executar todos os hooks manualmente
pre-commit run --all-files

# 4. Executar hook específico
pre-commit run bandit --all-files
pre-commit run black --all-files
pre-commit run flake8 --all-files

# 5. Bypass temporário (emergências apenas)
git commit --no-verify -m "hotfix: emergency commit"

# 6. Atualizar hooks para versões mais recentes
pre-commit autoupdate
```

### 📊 Benefícios dos Pre-commit Tests

#### **Qualidade Garantida**

- ✅ **Formatação consistente**: Black formata automaticamente
- ✅ **Imports organizados**: isort mantém ordem padrão
- ✅ **Código limpo**: Flake8 + Ruff detectam problemas
- ✅ **Sintaxe válida**: Verificação de YAML/JSON/TOML
- ✅ **Sem debug prints**: Detecta `print()` esquecidos

#### **Segurança Proativa**

- ✅ **Vulnerabilidades detectadas**: Bandit análise estática
- ✅ **Secrets protegidos**: Evita commit de credenciais
- ✅ **Arquivos grandes bloqueados**: Previne commit acidental
- ✅ **Conflitos detectados**: Evita commits com conflitos

#### **Produtividade**

- ✅ **Feedback imediato**: Erros detectados localmente
- ✅ **Correção automática**: Muitos problemas corrigidos automaticamente
- ✅ **CI/CD mais rápido**: Menos falhas no pipeline
- ✅ **Code review focado**: Revisão em lógica, não estilo

### 🔍 Relatórios de Segurança

#### **Exemplo de Execução Bandit**

```bash
$ pre-commit run bandit --all-files

bandit...................................................................Passed

# Relatório detalhado
$ bandit -r . -f json -o security-report.json
```

#### **Métricas de Qualidade**

```bash
# Relatório completo de qualidade
$ pre-commit run --all-files

trailing-whitespace..........................................Passed
end-of-file-fixer................................................Passed
check-yaml.......................................................Passed
check-json.......................................................Passed
check-added-large-files..........................................Passed
debug-statements.................................................Passed
check-merge-conflict.............................................Passed
black................................................................Passed
isort................................................................Passed
flake8...............................................................Passed
ruff.................................................................Passed
bandit...............................................................Passed

✅ Todos os 12 hooks passaram com sucesso!
```

### 🛡️ Configuração de Segurança do Bandit

O projeto utiliza configuração customizada do Bandit para análise de segurança:

```ini
# .bandit
[bandit]
exclude_dirs = venv,tests,__pycache__,.git
skips = B101,B104,B105
```

**Verificações Bandit Ativas:**

- ✅ **B102**: `exec` usage detection
- ✅ **B103**: File permissions (chmod)
- ✅ **B106**: Hardcoded passwords
- ✅ **B107**: Hardcoded sensitive URLs
- ✅ **B108**: Temp file usage
- ✅ **B201-B606**: SQL injection, XSS, crypto issues
- ✅ **B701-B902**: Framework-specific vulnerabilities

**Verificações Desabilitadas (Contexto Específico):**

- ❌ **B101**: assert_used (usado em testes)
- ❌ **B104**: hardcoded_bind_all_interfaces (config desenvolvimento)
- ❌ **B105**: hardcoded_password_string (exemplos documentação)

### 📈 Análise Estática Adicional

```bash
# Security linting Python (integrado no pre-commit)
bandit -r . -f json -o security-report.json

# Vulnerability scanning dependencies
safety check --json

# Dependency audit
pip-audit --format=json

# Type checking
mypy .

# Code complexity
radon cc . --average

# Documentation coverage
interrogate . --ignore-init-method

### Análise de Containers

```bash
# Docker image scanning
docker scout cves teams-intercom-backend:latest

# Runtime security
docker run --security-opt=no-new-privileges teams-intercom-backend
```

### Monitoring Contínuo

```bash
# Health checks
curl -f http://localhost:8000/health

# Log analysis
docker logs teams-intercom-backend | grep -i error

# Security events
journalctl -u docker | grep -i security
```

## 📚 Referências e Compliance

### Standards e Frameworks

- **OWASP Top 10** - Web application security
- **NIST Cybersecurity Framework** - Overall security posture
- **Azure Security Baseline** - Cloud security
- **Container Security Best Practices** - Docker/K8s security

### Links Úteis

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)

### ✅ Security Checklist

### Desenvolvimento

- [ ] Secrets não hardcoded
- [ ] .gitignore configurado corretamente
- [ ] **Pre-commit hooks instalados**: `pre-commit install`
- [ ] **Todos os hooks passando**: `pre-commit run --all-files`
- [ ] **Bandit scan limpo**: Sem vulnerabilidades detectadas
- [ ] **Formatação consistente**: Black + isort aplicados
- [ ] Input validation implementada
- [ ] Error handling seguro (sem vazamento de informações)
- [ ] Logging sanitizado

### Pre-commit Validation

- [ ] **Trailing whitespace removido**: Arquivos limpos
- [ ] **End-of-file fixer aplicado**: Linha em branco no final
- [ ] **YAML/JSON válidos**: Sintaxe correta
- [ ] **Sem arquivos grandes**: < 500KB por arquivo
- [ ] **Sem debug statements**: `print()`, `pdb.set_trace()` removidos
- [ ] **Conflitos resolvidos**: Sem markers de merge
- [ ] **Imports organizados**: isort profile black
- [ ] **Linting passando**: flake8 + ruff sem erros
- [ ] **Segurança validada**: bandit sem vulnerabilidades

### Deploy

- [ ] HTTPS configurado
- [ ] Containers não-root
- [ ] Network policies aplicadas
- [ ] Secrets externalizados
- [ ] **CI/CD hooks configurados**: Pre-commit em pipeline
- [ ] Backup configurado
- [ ] Monitoring ativo

### Produção

- [ ] Certificados válidos
- [ ] Rate limiting ativo
- [ ] Health checks funcionando
- [ ] Logs sendo coletados
- [ ] **Vulnerability scanning regular**: Bandit + safety
- [ ] **Dependency updates**: Renovate/Dependabot ativo
- [ ] Incident response plan definido

---

## 🆘 Emergências de Segurança

**Em caso de incidente crítico:**

1. **Isolamento**: Parar serviços afetados
2. **Avaliação**: Determinar escopo do impacto
3. **Contenção**: Implementar mitigações imediatas
4. **Comunicação**: Notificar stakeholders
5. **Recuperação**: Restaurar serviços seguros
6. **Lições aprendidas**: Documentar e melhorar

**Contatos de emergência:**

- GitHub Security: Use o formulário de reporte
- Email: <security@devopsvanilla.com>
- Status page: [status.devopsvanilla.com]
