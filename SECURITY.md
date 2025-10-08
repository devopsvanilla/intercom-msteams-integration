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

## 🔧 Ferramentas de Segurança

### Análise Estática

```bash
# Security linting Python
bandit -r . -f json -o security-report.json

# Vulnerability scanning
safety check --json

# Dependency check
pip-audit --format=json
```

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

## ✅ Security Checklist

### Desenvolvimento

- [ ] Secrets não hardcoded
- [ ] .gitignore configurado corretamente
- [ ] Input validation implementada
- [ ] Error handling seguro (sem vazamento de informações)
- [ ] Logging sanitizado

### Deploy

- [ ] HTTPS configurado
- [ ] Containers não-root
- [ ] Network policies aplicadas
- [ ] Secrets externalizados
- [ ] Backup configurado
- [ ] Monitoring ativo

### Produção

- [ ] Certificados válidos
- [ ] Rate limiting ativo
- [ ] Health checks funcionando
- [ ] Logs sendo coletados
- [ ] Vulnerability scanning regular
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
