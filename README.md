# Teams-Intercom Integration

Aplicação que integra Microsoft Teams com Intercom FIN AI usando FastAPI (backend) e React (frontend) para automação de atendimento, com interface web de configuração e suporte a múltiplas equipes e canais.

## 🚀 Novidades deste release
- Interface Web de Configuração (React) com suporte a múltiplos Teams/Channels
- API de Configuração (FastAPI) com persistência em arquivo/JSON e validações
- Sincronização bidirecional Intercom ↔ Teams
- Melhorias de logging, tratamento de erros e testes

## 🖥️ Interface Web de Configuração
A UI (frontend/) permite gerenciar:
- Múltiplas equipes do Microsoft Teams e seus canais
- Mapeamentos Intercom → Team/Channel
- Tokens/segredos (somente leitura, edição via .env)
- Testes rápidos de conectividade e webhooks

URLs padrão (dev):
- Frontend: http://localhost:5173 (Vite) ou http://localhost:3000
- Backend: http://localhost:8000

Principais telas:
- Dashboard: visão geral de status (Graph, Intercom, Webhooks)
- Teams & Channels: listar/adicionar/remover e definir mapeamentos
- Webhooks: validar assinatura e simular eventos
- Settings: variáveis de ambiente e caminhos de persistência

## 📦 Estrutura do Projeto
```
├── api/                  # Endpoints FastAPI (config, teams, intercom, webhooks)
├── frontend/             # UI React (Vite)
│   └── src/              # App.jsx, componentes e serviços
├── main.py               # App FastAPI, montagem de routers e CORS
├── graph_client.py       # Cliente Microsoft Graph API
├── intercom_client.py    # Cliente Intercom API
├── webhook_handler.py    # Handlers e verificação de assinatura
├── config.py             # Carregamento .env e camada de persistência
├── .env.example          # Variáveis de ambiente
└── tests/                # Testes de API e integração
```

## 📋 Pré-requisitos
- Python 3.10+ (recomendado)
- Node.js 18+ e npm/yarn/pnpm
- Conta Azure AD com permissões para app registration
- Token de API do Intercom e webhook secret

Permissões Microsoft Graph (delegadas ou application, conforme cenário):
- User.Read
- Team.ReadWrite.All
- Channel.ReadWrite.All
- Chat.ReadWrite
- ChannelMessage.Send

## 🛠️ Instalação
### 1) Clonar repositório
```bash
git clone https://github.com/devopsvanilla/intercom-msteams-integration.git
cd intercom-msteams-integration
```

### 2) Backend (FastAPI)
Crie virtualenv e instale dependências:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Copie e edite variáveis:
```bash
cp .env.example .env
# Edite .env com credenciais Azure/Intercom e opções de CORS
```
Execute em dev com autoreload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3) Frontend (React + Vite)
Instale e rode:
```bash
cd frontend
npm install
# Configure variável VITE_API_BASE se necessário (padrão: http://localhost:8000)
npm run dev  # inicia em http://localhost:5173
```

## ▶️ Demonstração de Uso
1) Abra o frontend e verifique o status do backend (badge “Healthy”).
2) Em “Teams & Channels”, clique em “Sincronizar” para listar equipes e canais via Microsoft Graph.
3) Configure mapeamentos: Intercom Inbox/Tag → Team/Channel.
4) Em “Webhooks”, use “Simular evento” para enviar conversation.user.created ao backend.
5) Envie uma mensagem do Intercom e confirme o espelhamento no canal do Teams configurado.

## 📡 Principais Endpoints
- GET /health — Status da aplicação
- GET /teams — Lista equipes
- GET /teams/{team_id}/channels — Lista canais
- POST /teams/{team_id}/channels — Cria canal
- POST /teams/{team_id}/channels/{channel_id}/messages — Envia mensagem
- GET /intercom/conversations — Lista conversas Intercom
- POST /sync/conversation-to-teams — Espelha conversa para Teams
- POST /webhooks/intercom — Recebe webhooks do Intercom
- GET/POST /config — Lê/grava configurações (multi-teams/channels)

## 🔐 Variáveis de Ambiente (.env)
Azure AD:
- AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID

Intercom:
- INTERCOM_ACCESS_TOKEN, INTERCOM_WEBHOOK_SECRET

App/Integração:
- DEFAULT_TEAM_ID, DEFAULT_CHANNEL_NAME
- CORS_ORIGINS=http://localhost:5173,http://localhost:3000
- CONFIG_STORE_PATH=./config_store.json

Frontend (opcional):
- frontend/.env: VITE_API_BASE=http://localhost:8000

## 🐛 Troubleshooting
1) Permissões/Consent no Azure AD
- Erro: 403/insufficient privileges
- Ação: conceda admin consent às permissões Graph e reautentique.

2) CORS ao acessar API do frontend
- Erro: “CORS policy blocked request”
- Ação: defina CORS_ORIGINS no .env do backend incluindo a URL do frontend, reinicie.

3) Persistência de configuração não salva
- Ação: verifique CONFIG_STORE_PATH (permissões de escrita, caminho relativo/absoluto). Confirme se POST /config retorna 200 e o arquivo é atualizado.

4) Webhook signature inválida
- Ação: confirme INTERCOM_WEBHOOK_SECRET e o cabeçalho X-Hub-Signature-256. Verifique relógio/UTF-8 ao calcular HMAC.

5) Autoreload não funciona
- Backend: use `uvicorn main:app --reload`; verifique se está rodando no ambiente virtual correto.
- Frontend: `npm run dev`; se a porta conflitar, export VITE_PORT=5173 ou use `--port`.

6) Falhas ao listar canais/teams
- Ação: garanta que o app/bot esteja no tenant e com acesso às equipes; valide DEFAULT_TEAM_ID.

7) Erros 429/limite de taxa
- Ação: aguarde backoff exponencial interno; reduza paralelismo e reintente.

Logs estruturados: habilite nível DEBUG para diagnósticos detalhados.

## 🧪 Testes
```bash
pytest
# Exemplo webhook manual
curl -X POST http://localhost:8000/webhooks/intercom \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{"topic":"conversation.user.created","data":{}}'
```

## 🤝 Contribuição
- Abra issues/PRs. Siga Conventional Commits quando possível.
- Execute linters/tests antes do PR.

## 📄 Licença
MIT. Veja LICENSE.
