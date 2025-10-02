# Teams-Intercom Integration

Uma aplicação Python completa para integrar Microsoft Teams com Intercom FIN AI usando Microsoft Graph API, proporcionando automação de atendimento ao cliente com comunicação bidirecional.

## 🚀 Funcionalidades

### Integração Microsoft Teams
- ✅ Autenticação OAuth 2.0 com Azure AD
- ✅ Gerenciamento de equipes e canais
- ✅ Envio e recebimento de mensagens
- ✅ Criação automática de canais

### Integração Intercom FIN AI
- ✅ Processamento de conversas
- ✅ Integração com webhooks
- ✅ Suporte ao FIN AI para respostas automatizadas
- ✅ Gerenciamento de usuários e tickets

### Recursos Avançados
- ✅ Processamento assíncrono de webhooks
- ✅ Retry logic para chamadas API
- ✅ Logging estruturado
- ✅ Validação de assinatura de webhooks
- ✅ Rate limiting e tratamento de erros

## 📋 Pré-requisitos

### Azure AD App Registration
1. Registre uma aplicação no Azure Portal
2. Configure as seguintes permissões da Microsoft Graph API:
   - `User.Read`
   - `Team.ReadWrite.All`
   - `Channel.ReadWrite.All`
   - `Chat.ReadWrite`
   - `ChannelMessage.Send`

### Intercom Setup
1. Obtenha um Access Token da API do Intercom
2. Configure webhooks no Intercom apontando para sua aplicação
3. Obtenha o webhook secret para validação de assinatura

### Python Requirements
- Python 3.8+
- Dependências listadas em `requirements.txt`

## 🛠️ Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/devopsvanilla/intercom-msteams-integration.git
cd intercom-msteams-integration
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

### 5. Configure o arquivo .env
```env
# Azure AD Configuration
AZURE_CLIENT_ID=your-azure-app-client-id
AZURE_CLIENT_SECRET=your-azure-app-client-secret
AZURE_TENANT_ID=your-azure-tenant-id

# Intercom Configuration
INTERCOM_ACCESS_TOKEN=your-intercom-access-token
INTERCOM_WEBHOOK_SECRET=your-intercom-webhook-secret

# Teams Integration Settings
DEFAULT_TEAM_ID=your-default-teams-team-id
DEFAULT_CHANNEL_NAME=Customer Support
```

## 🚀 Execução

### Desenvolvimento
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
python main.py
```

A aplicação estará disponível em `http://localhost:8000`

## 📡 Endpoints da API

### Health Check
- `GET /` - Status da aplicação
- `GET /health` - Health check detalhado

### Microsoft Teams
- `GET /teams` - Listar todas as equipes
- `GET /teams/{team_id}/channels` - Listar canais de uma equipe
- `POST /teams/{team_id}/channels` - Criar novo canal
- `POST /teams/{team_id}/channels/{channel_id}/messages` - Enviar mensagem
- `GET /teams/{team_id}/channels/{channel_id}/messages` - Obter mensagens

### Intercom
- `GET /intercom/conversations` - Listar conversas do Intercom
- `POST /sync/conversation-to-teams` - Sincronizar conversa para Teams
- `POST /teams/message-from-intercom` - Encaminhar mensagem do Teams para Intercom

### Webhooks
- `POST /webhooks/intercom` - Receber webhooks do Intercom

## 🔄 Fluxo de Integração

### 1. Intercom → Teams
1. Cliente envia mensagem no Intercom
2. Webhook é disparado para a aplicação
3. Aplicação processa o evento
4. FIN AI pode gerar resposta sugerida
5. Notificação é enviada para o canal Teams configurado

### 2. Teams → Intercom
1. Mensagem é enviada via API para endpoint específico
2. Aplicação cria/atualiza conversa no Intercom
3. Mensagem é associada ao usuário correto

## 📝 Eventos de Webhook Suportados

- `conversation.user.created` - Nova conversa criada
- `conversation.user.replied` - Cliente respondeu
- `conversation.admin.replied` - Admin respondeu
- `conversation.admin.assigned` - Conversa atribuída
- `conversation.admin.closed` - Conversa fechada

## 🏗️ Arquitetura

```
├── config.py              # Configuração e variáveis de ambiente
├── graph_client.py         # Cliente Microsoft Graph API
├── intercom_client.py      # Cliente Intercom API
├── webhook_handler.py      # Processador de webhooks
├── main.py                # Aplicação FastAPI principal
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de variáveis de ambiente
└── README.md             # Este arquivo
```

### Componentes Principais

#### GraphClient
- Gerencia autenticação com Azure AD
- Operações de Teams (canais, mensagens, equipes)
- Implementa retry logic e tratamento de erros

#### IntercomClient
- Cliente assíncrono para API do Intercom
- Suporte a conversas, usuários e FIN AI
- Context manager para gerenciamento de sessão

#### WebhookHandler
- Processa eventos do Intercom
- Verifica assinatura de webhooks
- Roteia eventos para handlers específicos

#### Main Application
- Servidor FastAPI com endpoints REST
- Processamento assíncrono de webhooks
- Logging estruturado e monitoramento

## 🔧 Configuração Avançada

### Logging
O sistema usa `structlog` para logging estruturado em JSON. Logs incluem:
- Timestamp ISO
- Nível de log
- Nome do logger
- Contexto estruturado

### Rate Limiting
- Implementado retry logic para APIs
- Tratamento de rate limits do Microsoft Graph
- Backoff exponencial em caso de falhas

### Segurança
- Validação de assinatura de webhooks
- Credenciais armazenadas em variáveis de ambiente
- Autenticação OAuth 2.0 com Azure AD

## 🧪 Testes

### Executar Testes
```bash
pytest
```

### Testes de Webhook
```bash
# Teste manual de webhook
curl -X POST http://localhost:8000/webhooks/intercom \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=your-signature" \
  -d '{"topic": "conversation.user.created", "data": {...}}'
```

## 🐛 Troubleshooting

### Erros Comuns

#### 1. Falha de Autenticação Azure AD
```
Erro: Authentication failed
Solução: Verifique AZURE_CLIENT_ID, AZURE_CLIENT_SECRET e AZURE_TENANT_ID
```

#### 2. Webhook Signature Invalid
```
Erro: Invalid webhook signature
Solução: Verifique INTERCOM_WEBHOOK_SECRET
```

#### 3. Teams Channel Not Found
```
Erro: Failed to get channels for team
Solução: Verifique se DEFAULT_TEAM_ID está correto e se o bot tem acesso
```

### Debug Mode
```bash
# Executar em modo debug
DEBUG=true python main.py
```

## 📊 Monitoramento

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs Estruturados
```json
{
  "timestamp": "2025-01-01T10:00:00.000Z",
  "level": "info",
  "logger": "webhook_handler",
  "event": "Processing webhook event: conversation.user.created",
  "conversation_id": "12345"
}
```

## 🔮 Próximos Passos

### Melhorias Planejadas
- [ ] Interface web para configuração
- [ ] Suporte a múltiplas equipes Teams
- [ ] Cache Redis para melhor performance
- [ ] Métricas e dashboards
- [ ] Suporte a anexos e imagens
- [ ] Integração com Azure Key Vault

### Contribuições
Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação oficial:
  - [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)
  - [Intercom API](https://developers.intercom.com/)
  - [FastAPI](https://fastapi.tiangolo.com/)

---

**Desenvolvido com ❤️ por DevOps Vanilla**
