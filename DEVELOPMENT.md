# 🛠️ Guia de Desenvolvimento - Teams-Intercom Integration

Este guia descreve padrões, arquitetura e fluxo de desenvolvimento do projeto.

## Arquitetura
- Backend: FastAPI (main.py) com routers em api/
- Frontend: React + Vite (frontend/src)
- Integrations: Microsoft Graph (graph_client.py), Intercom (intercom_client.py)
- Webhooks: webhook_handler.py com verificação HMAC (X-Hub-Signature-256)
- Config: config.py carrega .env e persiste configurações em CONFIG_STORE_PATH (JSON)

## Convenções de Código
- Python: black, isort, flake8, mypy (tipagem gradual)
- Commits: Conventional Commits (feat, fix, docs, refactor, test, chore)
- Estrutura de módulos: api/<domínio>.py expondo router = APIRouter()

## Desenvolvimento Local
### Backend
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
CORS é habilitado lendo CORS_ORIGINS do .env.

### Frontend
```bash
cd frontend
npm i
npm run dev  # http://localhost:5173
```
Defina VITE_API_BASE se o backend não estiver em http://localhost:8000.

## Persistência de Configuração
- Leitura/Escrita via endpoints GET/POST /config no backend
- Armazenamento em JSON (CONFIG_STORE_PATH), com validações de schema
- Campos sigilosos (tokens) não são retornados pelo GET

## Testes
- pytest para API e integração (tests/)
- Exemplos de testes para Teams/Channels e webhooks
```bash
pytest -q
```
Mock de clientes externos via monkeypatch/fixtures.

## Execução de Webhooks de Teste
```bash
curl -X POST http://localhost:8000/webhooks/intercom \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{"topic":"conversation.user.created","data":{}}'
```

## Guia de Colaboração
1. Crie branch a partir de main: feature/<escopo>, fix/<escopo>
2. Rode lint, testes e verificação de tipos antes do PR
3. Atualize docs (README/DEVELOPMENT) quando adicionar endpoints ou telas
4. Abra PR com descrição clara, checklist e evidências (prints/gifs)

## Roadmap Técnico
- Cache (Redis) para chamadas Graph
- Métricas/Tracing (OpenTelemetry)
- Uploads e anexos
- Integração com Azure Key Vault

## Dicas de Debug
- Ative DEBUG e log estruturado
- Inspecione requests/responses do Graph e Intercom com IDs de correlação
- Para CORS, confirme o Origin, Access-Control-Allow-Origin e OPTIONS preflight

## Publicação
- Containerizar backend e frontend (Dockerfile + docker-compose)
- Variáveis via .env e secrets do ambiente
