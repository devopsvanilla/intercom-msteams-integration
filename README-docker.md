# 🐳 Docker Deployment Guide

Este guia detalha como implantar a aplicação Teams-Intercom Integration usando Docker e Docker Compose.

## 📋 Pré-requisitos

- **Docker**: 20.10+ (recomendado 24.0+)
- **Docker Compose**: 2.0+ (incluído no Docker Desktop)
- **Credenciais configuradas**: Azure AD e Intercom

## 🚀 Deploy Rápido

### 1. Configurar Environment

```bash
# Copiar template de configuração
cp .env.docker .env

# Editar com suas credenciais
nano .env  # ou seu editor preferido
```

### 2. Deploy Automático

```bash
# Executar script de deploy
./scripts/deploy.sh
```

## ⚙️ Configuração Manual

### 1. Estrutura de Arquivos

```
├── Dockerfile              # Backend FastAPI
├── docker-compose.yml      # Orquestração
├── frontend/
│   ├── Dockerfile          # Frontend React
│   └── nginx.conf          # Configuração Nginx
├── nginx/
│   ├── nginx.conf          # Reverse proxy
│   └── conf.d/default.conf # Virtual hosts
├── scripts/
│   ├── deploy.sh          # Deploy automatizado
│   ├── backup.sh          # Backup de dados
│   ├── cleanup.sh         # Limpeza
│   └── status.sh          # Status dos serviços
└── .env.docker            # Template de configuração
```

### 2. Serviços Incluídos

- **Backend** (FastAPI): porta 8000
- **Frontend** (React + Nginx): porta 3000
- **Redis** (cache): porta 6379 (interna)
- **Nginx** (reverse proxy): portas 80/443

### 3. Variáveis de Ambiente Necessárias

```env
# Azure AD
AZURE_CLIENT_ID=seu-client-id
AZURE_CLIENT_SECRET=seu-client-secret
AZURE_TENANT_ID=seu-tenant-id

# Intercom
INTERCOM_ACCESS_TOKEN=seu-access-token
INTERCOM_WEBHOOK_SECRET=seu-webhook-secret

# Teams
DEFAULT_TEAM_ID=seu-team-id
DEFAULT_CHANNEL_NAME=Customer Support

# Security
REDIS_PASSWORD=senha-segura-redis
CORS_ORIGINS=http://localhost:3000
```

## 🔧 Comandos Úteis

### Deploy e Gestão

```bash
# Deploy completo
./scripts/deploy.sh

# Verificar status
./scripts/status.sh

# Backup
./scripts/backup.sh

# Limpeza completa
./scripts/cleanup.sh
```

### Docker Compose Manual

```bash
# Build e start
docker-compose up -d --build

# Verificar status
docker-compose ps

# Logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Parar
docker-compose down

# Rebuild específico
docker-compose build backend
docker-compose up -d backend
```

### Debugging

```bash
# Acessar container backend
docker exec -it teams-intercom-backend bash

# Acessar container frontend
docker exec -it teams-intercom-frontend sh

# Verificar logs específicos
docker logs teams-intercom-backend
docker logs teams-intercom-frontend

# Monitorar recursos
docker stats
```

## 🔒 Configurações de Segurança

### Containers

- ✅ **Usuários não-root** em todos os containers
- ✅ **Capabilities limitadas** (CAP_DROP ALL)
- ✅ **Security options** habilitadas
- ✅ **Resource limits** definidos
- ✅ **Health checks** configurados

### Rede

- ✅ **Rede isolada** entre containers
- ✅ **Rate limiting** no Nginx
- ✅ **CORS** configurado adequadamente
- ✅ **Headers de segurança** aplicados

### Dados

- ✅ **Volumes persistentes** para dados importantes
- ✅ **Backup automatizado** disponível
- ✅ **Configurações externalizadas** via .env

## 📊 Monitoramento

### Endpoints de Health

- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:3000/nginx-health`
- API Docs: `http://localhost:8000/docs`

### Logs Estruturados

```bash
# Ver logs em tempo real
docker-compose logs -f

# Filtrar por serviço
docker-compose logs backend | grep ERROR

# Logs do sistema
docker-compose logs nginx
```

### Métricas de Performance

```bash
# Uso de recursos
docker stats --no-stream

# Status detalhado
./scripts/status.sh
```

## 🔄 Backup e Restore

### Backup Automático

```bash
./scripts/backup.sh
# Cria backup em: ./backups/YYYYMMDD_HHMMSS/
```

### Restore Manual

```bash
# Parar serviços
docker-compose down

# Restaurar dados
cp -r backups/20241008_120000/config ./
cp -r backups/20241008_120000/data ./

# Restart
docker-compose up -d
```

## 🚀 Deploy em Produção

### 1. Configurações Adicionais

```env
# Produção
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=INFO

# SSL/TLS
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/private.key

# Monitoring
SENTRY_DSN=https://...
ENABLE_METRICS=true
```

### 2. Certificados SSL

```bash
# Criar diretório para certificados
mkdir -p nginx/ssl

# Copiar certificados
cp your-cert.pem nginx/ssl/cert.pem
cp your-key.pem nginx/ssl/private.key

# Ajustar permissões
chmod 600 nginx/ssl/*
```

### 3. Reverse Proxy Externo

Se usar nginx/traefik externo, ajustar portas:

```yaml
# docker-compose.yml
services:
  backend:
    ports:
      - "127.0.0.1:8000:8000"  # Só localhost
  frontend:
    ports:
      - "127.0.0.1:3000:80"   # Só localhost
```

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Containers não iniciam**
   ```bash
   # Verificar logs
   docker-compose logs

   # Verificar recursos
   docker system df
   docker system prune
   ```

2. **Frontend não conecta no backend**
   ```bash
   # Verificar variável VITE_API_BASE
   echo $VITE_API_BASE

   # Verificar rede
   docker network ls
   docker network inspect teams-intercom-integration_teams-intercom-network
   ```

3. **Banco Redis não conecta**
   ```bash
   # Testar conexão
   docker exec teams-intercom-redis redis-cli ping

   # Verificar senha
   docker exec teams-intercom-redis redis-cli -a $REDIS_PASSWORD ping
   ```

4. **Permissões de volume**
   ```bash
   # Ajustar permissões
   sudo chown -R 1000:1000 data logs config
   ```

### Logs Detalhados

```bash
# Habilitar debug
export DEBUG=true
docker-compose up -d

# Ver logs detalhados
docker-compose logs --tail=100 backend
```

## 📈 Otimizações

### Performance

- **Multi-stage builds** para imagens menores
- **Resource limits** para evitar overconsumption
- **Health checks** para auto-healing
- **Cache layers** otimizados

### Segurança

- **Non-root users** em todos os containers
- **Minimal base images** (alpine/slim)
- **Security headers** no Nginx
- **Rate limiting** ativado

### Escalabilidade

```yaml
# Escalar backend
docker-compose up -d --scale backend=3

# Load balancer automático via nginx upstream
```

## 🆘 Suporte

### Comandos de Diagnóstico

```bash
# Status completo
./scripts/status.sh

# Verificar configuração
docker-compose config

# Verificar imagens
docker images | grep teams-intercom

# Verificar volumes
docker volume ls | grep teams-intercom
```

### Reset Completo

```bash
# CUIDADO: Remove tudo!
./scripts/cleanup.sh
rm -rf data logs config
./scripts/deploy.sh
```

---

## ✅ Checklist de Deploy

- [ ] Docker e Docker Compose instalados
- [ ] Arquivo .env configurado com credenciais reais
- [ ] Diretórios data/, logs/, config/ criados
- [ ] Scripts executáveis (`chmod +x scripts/*.sh`)
- [ ] Deploy executado (`./scripts/deploy.sh`)
- [ ] Health checks passando
- [ ] Frontend acessível (http://localhost:3000)
- [ ] Backend API funcionando (http://localhost:8000/docs)
- [ ] Backup configurado

**🎉 Sua aplicação está pronta para uso em containers!**
