# Configuração Intercom - Guia Completo

Este guia detalha como configurar o Intercom para permitir que a aplicação Teams-Intercom Integration acesse conversas, crie/responda mensagens e receba eventos via webhooks.

## 📋 Pré-requisitos

- Conta Intercom com permissões de administrador
- Acesso ao [Intercom Developer Hub](https://developers.intercom.com/)
- Aplicação já configurada (seguir primeiro o [README-msteams-setup.md](README-msteams-setup.md))

---

## 🔧 Parte 1: Configuração no Developer Hub

### 1.1 Acessar Developer Hub

1. **Fazer login no Intercom**
   - Acesse: [https://app.intercom.com/](https://app.intercom.com/)
   - Faça login com sua conta

2. **Acessar Developer Hub**
   - Vá para: [https://developers.intercom.com/](https://developers.intercom.com/)
   - Ou clique em **Settings** > **Integrations** > **Developer Hub**

### 1.2 Criar Nova Aplicação

1. **Criar App**
   - No Developer Hub, clique em **"New app"**
   - Configurações:

     ```text
     App name: Teams-Intercom Integration
     Workspace: [Selecione seu workspace]
     App type: Internal integration
     ```

   - Clique em **"Create app"**

2. **Configurar Informações Básicas**
   - Na página da aplicação, preencha:

     ```text
     Description: Integração entre Microsoft Teams e Intercom para automação de atendimento
     Website: https://sua-empresa.com (opcional)
     Support email: seu-email@empresa.com
     ```

---

## 🔑 Parte 2: Configurar Access Token

### 2.1 Gerar Access Token

1. **Acessar Authentication**
   - Na aplicação criada, vá para **"Authentication"**
   - Clique em **"Access Token"**

2. **Configurar Permissões**
   - Selecione as permissões necessárias:

     ```text
     ✅ Read conversations
     ✅ Write conversations
     ✅ Read users
     ✅ Write users
     ✅ Read contacts
     ✅ Write contacts
     ✅ Read admins
     ✅ Read teams
     ```

3. **Gerar Token**
   - Clique em **"Create access token"**
   - **⚠️ IMPORTANTE**: Copie o token imediatamente (só aparece uma vez)

     ```text
     Token format: dG9rXzxxxxxxxxxxxxxxxxxxxxxxxxx
     ```

### 2.2 Configurar na Aplicação

1. **Adicionar ao .env**

   ```env
   INTERCOM_ACCESS_TOKEN=dG9rXzxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🔗 Parte 3: Configurar Webhooks

### 3.1 Criar Webhook Endpoint

1. **Acessar Webhooks**
   - Na aplicação, vá para **"Webhooks"**
   - Clique em **"Create webhook"**

2. **Configurar Endpoint**

   ```text
   Webhook URL: https://sua-aplicacao.com/webhooks/intercom

   # Para desenvolvimento local (use ngrok ou similar):
   Webhook URL: https://abc123.ngrok.io/webhooks/intercom
   ```

3. **Selecionar Eventos**
   - Marque os eventos necessários:

     ```text
     Conversation events:
     ✅ conversation.user.created
     ✅ conversation.user.replied
     ✅ conversation.admin.replied
     ✅ conversation.admin.closed
     ✅ conversation.admin.opened

     Contact events:
     ✅ contact.user.created (when a User contact is created)
     ✅ contact.lead.created (when a Lead contact is created)
     ✅ contact.lead.signed_up (when a Lead converts to User)
     ✅ visitor.signed_up (when a Visitor converts to User)
     ```

### 3.2 Configurar Webhook Secret

**⚠️ IMPORTANTE**: O webhook secret é essencial para validar que os webhooks recebidos realmente vêm do Intercom.

#### Opção 1: Secret na Página do Webhook Individual

1. **Após criar o webhook**
   - Depois de clicar em "Create webhook", você pode ser direcionado para a página de configuração
   - Procure por uma seção **"Secret"**, **"Webhook Secret"** ou **"Security"**

2. **Gerar Secret (se disponível)**
   - Clique em **"Generate secret"** ou **"Create secret"**
   - **⚠️ CRÍTICO**: Copie o secret imediatamente - só aparece uma vez!

#### Opção 2: Secret Automático ou Não Disponível

Se não encontrar a opção de gerar secret:

1. **Verificar se já existe um secret**
   - Alguns webhooks do Intercom podem vir com secret pré-gerado
   - Verifique se há um campo com valor similar a: `whsec_...`

2. **Secret pode estar oculto**
   - Em algumas versões da interface, o secret só aparece após salvar o webhook
   - Retorne à lista de webhooks e clique no webhook criado para editá-lo

#### Configuração no Projeto

1. **Adicionar ao .env**

   ```env
   # Se você obteve um secret:
   INTERCOM_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   # Se NÃO conseguiu obter um secret, deixe vazio por enquanto:
   INTERCOM_WEBHOOK_SECRET=
   ```

2. **Verificação de segurança**

   ```python
   # A aplicação pode funcionar sem secret, mas com menos segurança
   # Recomendamos sempre tentar obter o secret para validação adequada
   ```

#### 🔍 Troubleshooting do Webhook Secret

**Se não conseguir encontrar o secret:**

- ✅ **Teste sem secret primeiro**: A aplicação funcionará, mas sem validação de assinatura
- ✅ **Contate suporte Intercom**: Para contas enterprise, o secret pode estar em local diferente
- ✅ **Verifique documentação atualizada**: [Intercom Webhook Docs](https://developers.intercom.com/building-apps/docs/setting-up-webhooks)

**💡 Dica**: Você pode testar a integração sem o secret inicialmente e adicioná-lo depois quando encontrar na interface.

### 3.3 Finalizar Configuração do Webhook

1. **Salvar Webhook**
   - Clique em **"Create webhook"** ou **"Save webhook"**
   - O webhook será ativado automaticamente

2. **Verificar Status**
   - Após salvar, verifique se o status aparece como **"Active"** ou **"Enabled"**
   - Anote o **ID do webhook** (pode ser útil para troubleshooting)

3. **Testar Conectividade** (Opcional)
   - Algumas interfaces oferecem um botão **"Test webhook"** ou **"Send test event"**
   - Use essa opção para verificar se sua URL está acessível

**🎯 Checkpoint**: Neste ponto você deve ter:

- ✅ Webhook criado e ativo
- ✅ URL configurada corretamente
- ✅ Eventos selecionados
- ✅ Secret copiado (se disponível) ou configurado como vazio

---

## ⚙️ Parte 4: Configuração da Aplicação

### 4.1 Configurar Variáveis de Ambiente

1. **Editar arquivo .env**

   ```bash
   # Se ainda não existe
   cp .env.example .env
   ```

2. **Preencher credenciais Intercom**

   ```env
   # Intercom Configuration
   INTERCOM_ACCESS_TOKEN=dG9rXzxxxxxxxxxxxxxxxxxxxxxxxxx
   INTERCOM_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   INTERCOM_BASE_URL=https://api.intercom.io
   ```

### 4.2 Verificar Configuração

1. **Executar aplicação**

   ```bash
   uvicorn main:app --reload
   ```

2. **Testar API Intercom**

   ```bash
   curl http://localhost:8000/intercom/conversations
   # Deve retornar lista de conversas (pode estar vazia)
   ```

---

## 🏢 Parte 5: Configuração Avançada (Opcional)

### 5.1 Configurar Tags para Roteamento

1. **Criar Tags no Intercom**
   - Vá para **Settings** > **General** > **Tags**
   - Crie tags para diferentes equipes:

     ```text
     - teams-support
     - teams-sales
     - teams-billing
     - teams-technical
     ```

2. **Configurar Mapeamento**
   - Use a interface web da aplicação para mapear tags para channels específicos

### 5.2 Configurar Inbox Automático

1. **Criar Inbox Dedicado**
   - Vá para **Settings** > **Inbox settings**
   - Crie um inbox específico: "Teams Integration"

2. **Configurar Roteamento**
   - Configure regras para direcionar conversas para este inbox
   - Isso facilita o filtro na aplicação

---

## 🧪 Parte 6: Testes e Validação

### 6.1 Testes de API

1. **Teste Access Token**

   ```bash
   curl -H "Authorization: Bearer SEU-ACCESS-TOKEN" \
        https://api.intercom.io/me
   # Deve retornar informações da aplicação
   ```

2. **Teste Listar Conversas**

   ```bash
   curl http://localhost:8000/intercom/conversations
   # Deve retornar lista de conversas
   ```

### 6.2 Teste de Webhook

1. **Simular Evento**

   ```bash
     curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature: sha1=HASH-CALCULADO" \
     -d '{
       "topic": "conversation.user.created",
       "data": {
         "item": {
           "id": "12345",
           "source": {
             "author": {
               "name": "Cliente Teste",
               "email": "teste@empresa.com"
             },
             "body": "Olá, preciso de ajuda!"
           }
         }
       }
     }'

2. **Teste evento de criação de contato usuário:**

   ```bash
   curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature: sha1=HASH-CALCULADO" \
     -d '{
       "topic": "contact.user.created",
       "data": {
         "item": {
           "id": "contact123",
           "name": "João Silva",
           "email": "joao@empresa.com",
           "role": "user"
         }
       }
     }'
   ```

3. **Teste evento de criação de lead:**

   ```bash
   curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature: sha1=HASH-CALCULADO" \
     -d '{
       "topic": "contact.lead.created",
       "data": {
         "item": {
           "id": "lead456",
           "name": "Maria Santos",
           "email": "maria@exemplo.com",
           "role": "lead"
         }
       }
     }'
   ```

4. **Teste evento de conversão de lead:**

   ```bash
   curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature: sha1=HASH-CALCULADO" \
     -d '{
       "topic": "contact.lead.signed_up",
       "data": {
         "item": {
           "id": "contact789",
           "name": "Pedro Costa",
           "email": "pedro@exemplo.com",
           "role": "user"
         }
       }
     }'2. **Teste evento de criação de contato usuário:**
   }'

2. **Teste evento de criação de contato usuário:**

   ```bash
   curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature-256: sha256=HASH-CALCULADO" \
     -d '{
       "topic": "contact.user.created",
       "data": {
         "item": {
           "id": "contact123",
           "name": "João Silva",
           "email": "joao@empresa.com",
           "role": "user"
         }
       }
     }'
   ```

3. **Teste evento de criação de lead:**

   ```bash
   curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature-256: sha256=HASH-CALCULADO" \
     -d '{
       "topic": "contact.lead.created",
       "data": {
         "item": {
           "id": "lead456",
           "name": "Maria Santos",
           "email": "maria@exemplo.com",
           "role": "lead"
         }
       }
     }'
   ```

4. **Teste evento de conversão de lead:**

   ```bash
   curl -X POST https://seu-webhook-url.ngrok.io/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature-256: sha256=HASH-CALCULADO" \
     -d '{
       "topic": "contact.lead.signed_up",
       "data": {
         "item": {
           "id": "contact789",
           "name": "Pedro Costa",
           "email": "pedro@exemplo.com",
           "role": "user"
         }
       }
     }'
   ```

5. **Verificar Logs**

5. **Verificar Logs**

   Após enviar um webhook de teste, verifique os logs da aplicação:

   ```

2. **Verificar Logs**

   ```bash
   # Verificar se o webhook foi processado
   docker logs teams-intercom-backend | grep webhook
   ```

### 6.3 Teste de Integração Completa

1. **Criar Conversa no Intercom**
   - Acesse o Intercom inbox
   - Crie uma nova conversa
   - Verifique se aparece no Teams

2. **Responder do Teams**
   - Responda no canal configurado
   - Verifique se a resposta aparece no Intercom

---

## 🔒 Segurança e Boas Práticas

### Proteção do Access Token

- ✅ **Nunca** exponha o token em logs ou código
- ✅ Use variáveis de ambiente
- ✅ Rotacione o token periodicamente (recomendado: 90 dias)
- ✅ Monitore uso do token via Intercom logs

### Validação de Webhooks

- ✅ **Sempre** valide a assinatura HMAC
- ✅ Use HTTPS em produção
- ✅ Implemente retry logic para falhas temporárias
- ✅ Monitore webhooks perdidos

### Rate Limiting

```python
# A aplicação já implementa rate limiting automático
# Limits do Intercom API:
# - 1000 requests/minute por default
# - Monitore headers: X-RateLimit-*
```

---

## 🚨 Troubleshooting

### Problemas Comuns

1. **Token inválido (401)**

   ```
   Erro: Unauthorized
   Solução: Verificar INTERCOM_ACCESS_TOKEN no .env
   ```

2. **Webhook não recebido**

   ```
   Problema: URL não acessível
   Solução: Usar ngrok para desenvolvimento local
   ```

3. **Signature validation failed**

   ```
   Problema: Secret incorreto ou encoding
   Solução: Verificar INTERCOM_WEBHOOK_SECRET
   ```

### Comandos de Diagnóstico

```bash
# Verificar configuração
curl -H "Authorization: Bearer $INTERCOM_ACCESS_TOKEN" \
     https://api.intercom.io/me

# Testar webhook endpoint
curl -X POST http://localhost:8000/webhooks/intercom \
     -H "Content-Type: application/json" \
     -d '{"topic":"ping"}'

# Verificar logs
tail -f logs/app.log | grep intercom
```

---

## 📞 Suporte

### Links Úteis

- [Intercom API Documentation](https://developers.intercom.com/intercom-api-reference)
- [Webhook Events Reference](https://developers.intercom.com/intercom-api-reference/reference/webhook-models)
- [Authentication Guide](https://developers.intercom.com/building-apps/docs/authentication-types)

### Contato

Para problemas específicos da integração:

- **GitHub Issues**: Reporte bugs e solicite features
- **Email**: <suporte@devopsvanilla.com>
- **Documentação**: Consulte outros README*.md do projeto

---

## ✅ Checklist de Configuração

- [ ] Aplicação criada no Developer Hub
- [ ] Access Token gerado e copiado
- [ ] Permissões corretas selecionadas
- [ ] Webhook URL configurada corretamente
- [ ] Eventos necessários selecionados
- [ ] Webhook Secret gerado e copiado
- [ ] Arquivo .env configurado com tokens
- [ ] Teste de API passou (GET /me)
- [ ] Teste de webhook passou
- [ ] Integração completa funcionando
- [ ] Logs e monitoramento configurados

### 🔍 Verificação Final dos Tokens

No Developer Hub, verifique se:

- ✅ **Access Token** está ativo e com permissões corretas
- ✅ **Webhook** está recebendo eventos (check delivery logs)
- ✅ **Rate limits** não estão sendo excedidos
- ✅ **Workspace** correto está selecionado

**🎉 Sua integração Intercom-Teams está pronta para uso!**

---

**💡 Próximos Passos:**

1. Configure mapeamentos de tags/inboxes na interface web
2. Teste cenários reais de atendimento
3. Configure monitoramento e alertas
4. Documente processos para sua equipe
