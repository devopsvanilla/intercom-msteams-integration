#!/bin/bash
# Script para registrar um aplicativo Azure AD, criar segredo e configurar permissões para Microsoft Graph
# Uso: bash ./scripts/register-azure-app.sh <app-name> <tenant-id> <redirect-uri>

set -e

APP_NAME=${1:-intercom-msteams}
TENANT_ID=${2}
REDIRECT_URI=${3:-http://localhost:8000/auth/callback}

# Detectar tenantId do usuário logado
CURRENT_TENANT_ID=$(az account show --query tenantId -o tsv)
echo "Tenant ID detectado pelo Azure CLI: $CURRENT_TENANT_ID"

if [ -z "$TENANT_ID" ]; then
  echo "Uso: bash $0 <app-name> <tenant-id> <redirect-uri>"
  echo "Exemplo: bash $0 intercom-msteams $CURRENT_TENANT_ID http://localhost:8000/auth/callback"
  read -p "Deseja usar o tenant detectado ($CURRENT_TENANT_ID)? [s/N]: " USE_TENANT
  if [[ "$USE_TENANT" =~ ^[sS]$ ]]; then
    TENANT_ID="$CURRENT_TENANT_ID"
  else
    echo "Informe o tenantId como segundo argumento."
    exit 1
  fi
else
  if [ "$TENANT_ID" != "$CURRENT_TENANT_ID" ]; then
    echo "ATENÇÃO: O tenant informado ($TENANT_ID) é diferente do detectado pelo Azure CLI ($CURRENT_TENANT_ID)."
    read -p "Deseja continuar mesmo assim? [s/N]: " CONTINUE_ANYWAY
    if [[ ! "$CONTINUE_ANYWAY" =~ ^[sS]$ ]]; then
      echo "Abortado pelo usuário."
      exit 1
    fi
  fi
fi

# 1. Registrar o aplicativo (ou usar existente)
echo "Verificando se o aplicativo '$APP_NAME' já existe..."
EXISTING_APP=$(az ad app list --display-name "$APP_NAME" --query "[0].{appId:appId}" -o json 2>/dev/null || echo "{}")
EXISTING_APP_ID=$(echo "$EXISTING_APP" | jq -r .appId 2>/dev/null || echo "null")

if [ "$EXISTING_APP_ID" != "null" ] && [ "$EXISTING_APP_ID" != "" ]; then
  echo "Aplicativo existente encontrado com ID: $EXISTING_APP_ID"
  APP_ID="$EXISTING_APP_ID"
  echo "Atualizando configurações do aplicativo existente..."
  az ad app update \
    --id "$APP_ID" \
    --web-redirect-uris "$REDIRECT_URI" \
    --sign-in-audience AzureADMyOrg
else
  echo "Criando novo aplicativo..."
  APP_INFO=$(az ad app create \
    --display-name "$APP_NAME" \
    --sign-in-audience AzureADMyOrg \
    --web-redirect-uris "$REDIRECT_URI" \
    --query "{appId:appId}" -o json)
  APP_ID=$(echo "$APP_INFO" | jq -r .appId)
fi

# 2. Criar segredo do cliente
SECRET_INFO=$(az ad app credential reset \
  --id "$APP_ID" \
  --append \
  --display-name "Intercom Integration Secret" \
  --years 2 \
  --query "{secret:password}" -o json)
CLIENT_SECRET=$(echo "$SECRET_INFO" | jq -r .secret)

# 3. Adicionar permissões Microsoft Graph (exemplo: Channel.ReadWrite.All, Team.ReadWrite.All)
# Using permission IDs for Microsoft Graph API
# Channel.ReadWrite.All: cc83893a-e232-4723-b5af-bd0b01bcfe65
# Team.ReadWrite.All: 0121dc95-1b9f-4aed-8892-78e9b83f1b80
# User.Read: e1fe6dd8-ba31-4d61-89e7-88639da4683d

az ad app permission add \
  --id "$APP_ID" \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions cc83893a-e232-4723-b5af-bd0b01bcfe65=Role

az ad app permission add \
  --id "$APP_ID" \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions 0121dc95-1b9f-4aed-8892-78e9b83f1b80=Role

az ad app permission add \
  --id "$APP_ID" \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope

# 4. Conceder permissões (admin consent)
echo "Solicitando consentimento do administrador para as permissões..."
az ad app permission admin-consent --id "$APP_ID" || echo "Aviso: Falha ao conceder consentimento automaticamente. Você pode precisar conceder manualmente no portal do Azure."

# 5. Exibir dados para .env
cat <<EOF

# Adicione ao seu .env:
AZURE_CLIENT_ID=$APP_ID
AZURE_CLIENT_SECRET=$CLIENT_SECRET
AZURE_TENANT_ID=$TENANT_ID
AZURE_REDIRECT_URI=$REDIRECT_URI
EOF

echo "Aplicativo registrado e configurado com sucesso!"
