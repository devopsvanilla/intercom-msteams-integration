# Configuração de Autenticação - Microsoft Graph

Este documento explica como configurar a autenticação correta para o Microsoft Graph API.

## Problema Resolvido

O erro `/me request is only valid with delegated authentication flow` ocorreu porque:

1. O código original usava **Client Credentials Flow** (autenticação de aplicativo)
2. Mas tentava acessar o endpoint `/me` que requer **Delegated Authentication Flow** (autenticação de usuário)

## Solução Implementada

### 1. Duplo Fluxo de Autenticação

O código agora suporta dois tipos de autenticação baseado na variável de ambiente `USE_DEVICE_CODE_AUTH`:

#### Para Desenvolvimento (Device Code Flow)
```env
USE_DEVICE_CODE_AUTH=true
```

- **Vantagens**: Pode acessar `/me` e outros endpoints delegados
- **Desvantagens**: Requer interação do usuário (login)
- **Uso**: Desenvolvimento local

#### Para Produção (Client Credentials Flow)
```env
USE_DEVICE_CODE_AUTH=false
```

- **Vantagens**: Execução automática, sem interação do usuário
- **Desvantagens**: Não pode acessar endpoints delegados como `/me`
- **Uso**: Produção, CI/CD, servidores

### 2. Endpoints Compatíveis

#### Device Code Flow (Delegated)
- `GET /me` ✅
- `GET /me/joinedTeams` ✅
- Requer permissões delegadas no Azure AD

#### Client Credentials Flow (Application)
- `GET /groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')` ✅
- `GET /applications` ✅
- Requer permissões de aplicativo no Azure AD

## Configuração no Azure AD

### 1. Permissões Delegadas (Device Code Flow)
No Azure Portal → App Registration → API Permissions, adicione:

```
Microsoft Graph:
- Team.ReadBasic.All (Delegated)
- Channel.ReadBasic.All (Delegated)
- ChannelMessage.Send (Delegated)
- Channel.Create (Delegated)
- User.Read (Delegated)
```

### 2. Permissões de Aplicativo (Client Credentials Flow)
No Azure Portal → App Registration → API Permissions, adicione:

```
Microsoft Graph:
- Team.ReadBasic.All (Application)
- Channel.ReadBasic.All (Application)
- ChannelMessage.Send (Application)
- Channel.Create (Application)
- Group.Read.All (Application)
```

### 3. Configurações Adicionais

#### Para Device Code Flow:
- Vá em **Authentication** → **Advanced settings**
- Marque "Allow public client flows" = **Yes**

#### Para ambos os fluxos:
- Vá em **Certificates & secrets**
- Crie um novo **Client secret**
- Copie o valor para `AZURE_CLIENT_SECRET`

## Como Usar

### 1. Desenvolvimento Local

```bash
# Configure no .env
USE_DEVICE_CODE_AUTH=true

# Execute a aplicação
uvicorn main:app --reload --port 8000
```

No primeiro acesso, aparecerá um código para autenticação:
```
To sign in, use a web browser to open the page https://microsoft.com/devicelogin
and enter the code XXXXXXXXX to authenticate.
```

### 2. Produção

```bash
# Configure no .env
USE_DEVICE_CODE_AUTH=false

# Execute a aplicação
uvicorn main:app --port 8000
```

## Monitoramento

O código inclui logs para identificar qual fluxo está sendo usado:

```python
# Device Code Flow
logger.info("Using Device Code authentication flow...")
logger.info(f"Authenticated as user: {user.display_name}")

# Client Credentials Flow
logger.info("Using Client Credentials authentication flow...")
logger.info("Successfully authenticated with application permissions")
```

## Resolução de Problemas

### Erro: "AADSTS65001: The user or administrator has not consented"
- Vá no Azure Portal → App Registration → API Permissions
- Clique em "Grant admin consent for [tenant]"

### Erro: "Authentication failed"
- Verifique se `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` e `AZURE_TENANT_ID` estão corretos
- Confirme se as permissões foram concedidas no Azure AD

### Device Code não aparece
- Verifique se `USE_DEVICE_CODE_AUTH=true` no arquivo .env
- Confirme se "Allow public client flows" está habilitado

## Links Úteis

- [Microsoft Graph Authentication Concepts](https://learn.microsoft.com/en-us/graph/auth/auth-concepts)
- [Device Code Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)
- [Client Credentials Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)
