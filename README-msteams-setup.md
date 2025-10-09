# Configuração Microsoft Teams - Guia Completo

Este guia detalha como configurar a integração entre Microsoft Teams e Intercom para permitir que a aplicação acesse e envie mensagens nos canais do Teams.

## 📋 Pré-requisitos

- **Conta Microsoft 365**: Acesso a uma organização com Microsoft Teams
- **Permissões administrativas**: Capacidade de registrar aplicações no Azure AD
- **Microsoft Teams**: Equipes e canais onde deseja integrar
- **Acesso ao Azure Portal**: Para configurar o registro da aplicação

## 🔧 Parte 1: Configuração no Azure Portal

### 1.1 Registrar Nova Aplicação

1. **Acesse o Azure Portal**
   - Navegue para [portal.azure.com](https://portal.azure.com)
   - Faça login com credenciais administrativas
   - No menu superior ou no campo de busca, digite "Azure Active Directory" e clique no resultado
   - Ou clique no ícone do Azure AD no painel lateral (se visível)

   **💡 Nota**: Você deve ver uma página similar à sua imagem, com "Windows Azure Active Directory" e opções como "Visão geral", "Plano de implantação", etc.

2. **Criar App Registration**
   - No Azure Portal, você já está no **Azure Active Directory** na **Visão Geral**
   - Clique no botão **"+ Adicionar"** no topo da página
   - No menu suspenso, selecione **"Registro de aplicativo"**
   - Isso abrirá a página de criação de novo registro

   **💡 Método alternativo**: Você também pode navegar pelo menu lateral: **Gerenciar** > **App registrations** > **New registration**
   - Preencha as informações:

     ```text
     Name: Teams-Intercom Integration
     Supported account types: Accounts in this organizational directory only
     Redirect URI:
       - Platform: Web
       - URI: http://localhost:8000/auth/callback
     ```

   - Clique em **Register**

3. **Anote as Informações Importantes**
   Após o registro, anote na página **Overview**:

   ```text
   Application (client) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   Directory (tenant) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

### 1.2 Configurar Client Secret

1. **Criar Client Secret**
   - Na aplicação registrada, vá para **Certificates & secrets**
   - Clique em **New client secret**
   - Configurações:

     ```text
     Description: Teams-Intercom Integration Secret
     Expires: 24 months (recomendado)
     ```

   - Clique em **Add**
   - **⚠️ IMPORTANTE**: Copie o **Value** imediatamente (só aparece uma vez)

### 1.3 Configurar Permissões da API

1. **Adicionar Permissões Microsoft Graph**
   - Vá para **API permissions**
   - Clique em **Add a permission**
   - Selecione **Microsoft Graph**
   - Escolha **Delegated permissions**

   **Permissões Necessárias para a Integração:**

   ```text
   ✅ ChannelMessage.Send (enviar mensagens em canais)
   ✅ ChannelMessage.Read.All (ler mensagens dos canais)
   ✅ Team.ReadBasic.All (listar teams disponíveis)
   ✅ Channel.ReadBasic.All (listar canais dos teams)
   ✅ User.Read (perfil do usuário autenticado)
   ```

   **Como adicionar cada permissão:**
   - Clique em **Add a permission** > **Microsoft Graph** > **Delegated permissions**
   - Use a busca para encontrar cada permissão da lista
   - Marque a permissão e clique **Add permissions**
   - Repita para todas as permissões necessárias

2. **Grant Admin Consent**
   - Após adicionar todas as permissões, clique em **Grant admin consent for [sua organização]**
   - Confirme clicando em **Yes**
   - **Verifique o status**: Todas as permissões devem mostrar **Status: Sim**

3. **Verificação Final**
   - Na lista de permissões, confirme que todas aparecem com **Status: Sim**
   - Especialmente importante: `ChannelMessage.Send` deve estar presente e ativa

### 1.4 Configurar Authentication (Opcional)

Se precisar de autenticação interativa:

1. **Configurar Redirect URIs**
   - Vá para **Authentication**
   - Em **Platform configurations**, adicione:

     ```text
     Web Redirect URIs:
     - http://localhost:8000/auth/callback
     - https://sua-aplicacao.azurewebsites.net/auth/callback (para produção)
     ```

2. **Configurações Avançadas**
   - **Allow public client flows**: No (recomendado)
   - **Supported account types**: Single tenant (recomendado)

## ⚙️ Parte 2: Configuração da Aplicação

### 2.1 Configurar Variáveis de Ambiente

1. **Editar arquivo .env**

   ```bash
   # Copie o arquivo de exemplo se ainda não existe
   cp .env.example .env
   ```

2. **Preencher credenciais Azure**

   ```env
   # Azure AD Configuration
   AZURE_CLIENT_ID=seu-application-client-id-aqui
   AZURE_CLIENT_SECRET=seu-client-secret-aqui
   AZURE_TENANT_ID=seu-tenant-id-aqui
   AZURE_REDIRECT_URI=http://localhost:8000/auth/callback

   # Teams Integration Settings
   DEFAULT_TEAM_ID=seu-team-id-preferido (opcional)
   DEFAULT_CHANNEL_NAME=Customer Support
   ```

3. **Obter Team ID (Opcional)**
   - Execute a aplicação e acesse: `GET /teams`
   - Ou use Microsoft Graph Explorer: [graph.microsoft.com](https://developer.microsoft.com/en-us/graph/graph-explorer)
   - Query: `GET https://graph.microsoft.com/v1.0/me/joinedTeams`

### 2.2 Verificar Configuração

1. **Testar Autenticação**

   ```bash
   # Inicie a aplicação
   uvicorn main:app --reload

   # Teste o endpoint de health
   curl http://localhost:8000/health
   ```

2. **Verificar Microsoft Graph**

   ```bash
   # Listar teams disponíveis
   curl http://localhost:8000/teams

   # Listar canais de uma equipe
   curl http://localhost:8000/teams/{TEAM_ID}/channels
   ```

## 🏢 Parte 3: Configuração no Microsoft Teams

### 3.1 Adicionar Bot/Aplicação ao Teams

### Método 1: Via Teams Admin Center (Recomendado)

1. **Acesse Teams Admin Center**
   - Vá para [admin.teams.microsoft.com](https://admin.teams.microsoft.com)
   - Login como administrador

2. **Upload Custom App**
   - **Teams apps** > **Manage apps**
   - Clique em **Upload new app**
   - Crie um app manifest (veja seção 3.2)

### Método 2: Convite Direto

1. **Adicionar via Graph API**

   ```bash
   # A aplicação pode auto-adicionar-se aos teams
   # usando as permissões configuradas
   POST /teams/{team-id}/members
   ```

### 3.2 Manifest da Aplicação Teams (Opcional)

Se quiser instalar como app nativo do Teams, crie `manifest.json`:

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.16/MicrosoftTeams.schema.json",
  "manifestVersion": "1.16",
  "version": "1.0.0",
  "id": "SEU-AZURE-CLIENT-ID",
  "packageName": "com.empresa.teams-intercom-integration",
  "developer": {
    "name": "Sua Empresa",
    "websiteUrl": "https://sua-empresa.com",
    "privacyUrl": "https://sua-empresa.com/privacy",
    "termsOfUseUrl": "https://sua-empresa.com/terms"
  },
  "icons": {
    "color": "color.png",
    "outline": "outline.png"
  },
  "name": {
    "short": "Intercom Integration",
    "full": "Teams-Intercom Integration Bot"
  },
  "description": {
    "short": "Integração entre Teams e Intercom",
    "full": "Bot que conecta Microsoft Teams com Intercom para suporte ao cliente"
  },
  "accentColor": "#FFFFFF",
  "bots": [
    {
      "botId": "SEU-AZURE-CLIENT-ID",
      "scopes": ["team", "personal"],
      "commandLists": [
        {
          "scopes": ["team"],
          "commands": [
            {
              "title": "help",
              "description": "Mostra comandos disponíveis"
            }
          ]
        }
      ]
    }
  ],
  "permissions": [
    "identity",
    "messageTeamMembers"
  ],
  "validDomains": [
    "sua-aplicacao.azurewebsites.net",
    "localhost"
  ]
}
```

### 3.3 Configurar Webhook do Teams (Opcional)

Para receber mensagens do Teams:

1. **Configurar Webhook Endpoint**

   ```env
   TEAMS_WEBHOOK_PATH=/webhooks/teams
   ```

2. **Registrar Webhook no Teams**
   - Use Graph API ou Teams Admin para configurar webhook
   - Endpoint: `https://sua-app.com/webhooks/teams`

## 🧪 Parte 4: Testes e Validação

### 4.1 Testes de Conectividade

1. **Teste Health Check**

   ```bash
   curl http://localhost:8000/health
   # Resposta esperada:
   {
     "status": "healthy",
     "services": {
       "graph_api": true,
       "webhook_handler": true
     }
   }
   ```

2. **Teste Listar Teams**

   ```bash
   curl http://localhost:8000/teams
   # Deve retornar lista de teams acessíveis
   ```

3. **Teste Enviar Mensagem**

   ```bash
   curl -X POST http://localhost:8000/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages \
     -H "Content-Type: application/json" \
     -d '{
       "message": "🤖 Teste de integração Teams-Intercom funcionando!",
       "type": "html"
     }'
   ```

### 4.2 Teste de Integração Completa

1. **Simular Webhook Intercom**

   ```bash
   curl -X POST http://localhost:8000/webhooks/intercom \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature-256: sha256=..." \
     -d '{
       "topic": "conversation.user.created",
       "data": {
         "item": {
           "id": "12345",
           "source": {
             "author": {
               "name": "Cliente Teste",
               "email": "teste@empresa.com"
             }
           }
         }
       }
     }'
   ```

2. **Verificar no Teams**
   - Acesse o canal configurado no Teams
   - Verifique se a mensagem apareceu

## 🔒 Segurança e Boas Práticas

### Segurança das Credenciais

1. **Proteger Client Secret**

   ```bash
   # Nunca commite o .env
   echo ".env" >> .gitignore

   # Use Azure Key Vault em produção
   # Use variáveis de ambiente do container/sistema
   ```

2. **Rotação de Secrets**
   - Configure expiração do client secret (máximo 24 meses)
   - Monitore expiração e renove antes do vencimento
   - Teste com nova credencial antes de remover a antiga

### Princípio do Menor Privilégio

1. **Permissões Mínimas**
   - Use apenas as permissões Graph necessárias
   - Prefira delegated permissions quando possível
   - Evite `*.All` permissions desnecessárias

2. **Escopo de Teams**
   - Configure `DEFAULT_TEAM_ID` para limitar acesso
   - Use service accounts específicos
   - Monitore logs de acesso

### Monitoramento

1. **Logs de Auditoria**
   - Azure AD > Sign-in logs
   - Azure AD > Audit logs
   - Teams Admin Center > Usage reports

2. **Health Monitoring**

   ```bash
   # Configure alertas para:
   # - Falhas de autenticação
   # - Rate limits Graph API
   # - Webhook failures
   ```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro 401 - Unauthorized**

   ```
   Causas:
   - Client ID/Secret incorretos
   - Tenant ID errado
   - Credenciais de autenticação inválidas

   Solução:
   - Verificar credenciais no .env
   - Confirmar Client ID e Tenant ID corretos
   - Regenerar Client Secret se necessário
   ```

2. **Erro 403 - Forbidden ao enviar mensagem**

   ```
   Causas:
   - Permissões não concedidas pelo administrador
   - App não autorizado no team/canal
   - Usuário sem permissões suficientes

   Solução:
   - Verificar que admin consent foi concedido
   - Confirmar que app está autorizado nos teams
   - Verificar permissões do usuário autenticado
   ```

3. **Erro 429 - Rate Limited**

   ```
   Causas:
   - Muitas requests para Microsoft Graph API
   - Throttling da Microsoft

   Solução:
   - Implementar backoff exponencial
   - Reduzir frequência de calls
   - Usar batch requests quando possível
   ```

4. **Teams não listados**

   ```
   Causas:
   - App não tem acesso aos teams
   - Usuário não é membro dos teams
   - Permissões insuficientes

   Solução:
   - Verificar permissões Team.ReadBasic.All
   - Confirmar que usuário é membro dos teams
   - Adicionar app aos teams necessários
   ```

5. **Permissões não aparecem no portal**

   ```
   Causas:
   - Procurando na seção errada do portal
   - Cache do navegador

   Solução:
   - Verificar seção "API permissions" do app registration
   - Atualizar página do navegador
   - Usar navegador em modo incógnito
   ```

### Logs e Debug

1. **Habilitar Debug Logs**

   ```env
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```

2. **Verificar Logs Estruturados**

   ```bash
   # Logs da aplicação mostrarão:
   # - Tentativas de autenticação
   # - Calls Graph API
   # - Responses e errors
   tail -f logs/app.log | jq .
   ```

3. **Graph Explorer Testing**
   - Use [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
   - Teste queries com as mesmas credenciais
   - Valide permissions e responses

## 📞 Suporte

Para problemas específicos:

1. **Azure AD/Graph API**: [Microsoft Q&A](https://docs.microsoft.com/en-us/answers/)
2. **Teams Development**: [Teams Developer Community](https://docs.microsoft.com/en-us/microsoftteams/platform/)
3. **Documentação oficial**: [Microsoft Graph Teams API](https://docs.microsoft.com/en-us/graph/api/resources/teams-api-overview)

---

## ✅ Checklist de Configuração

- [ ] App registrado no Azure AD
- [ ] Client Secret criado e copiado
- [ ] Permissões Graph configuradas como **Delegated permissions**
- [ ] **ChannelMessage.Send** adicionada e ativa
- [ ] Admin consent concedido (**Status: Sim** em todas as permissões)
- [ ] Arquivo .env configurado com todas as credenciais
- [ ] Teste de health passou
- [ ] Lista de teams funcionando
- [ ] Mensagem de teste enviada com sucesso
- [ ] Webhook Intercom funcionando
- [ ] Logs e monitoramento configurados

### 🔍 Verificação Final das Permissões

Antes de prosseguir, confirme na tela de **API permissions** do Azure Portal:

```text
ChannelMessage.Send | Delegated | Send channel messages | Sim ✅
ChannelMessage.Read.All | Delegated | Read user channel messages | Sim ✅
Team.ReadBasic.All | Delegated | Read the names and descriptions of teams | Sim ✅
Channel.ReadBasic.All | Delegated | Read the names and descriptions of channels | Sim ✅
User.Read | Delegated | Sign in and read user profile | Sim ✅
```

**Se alguma permissão mostrar Status "Não":**

1. Clique em "Grant admin consent for [Tenant]"
2. Aguarde alguns minutos para propagação
3. Recarregue a página do Azure Portal
4. Verifique que todas mudaram para "Sim"

**🎉 Sua integração Teams-Intercom está pronta para uso!**
