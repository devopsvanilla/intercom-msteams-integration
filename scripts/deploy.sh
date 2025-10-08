#!/bin/bash

set -e

echo "🚀 Deploying Teams-Intercom Integration..."

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please copy .env.docker to .env and configure your credentials"
    echo "   cp .env.docker .env"
    echo "   # Edit .env with your Azure and Intercom credentials"
    exit 1
fi

# Verificar variáveis críticas
source .env
if [ -z "$AZURE_CLIENT_ID" ] || [ -z "$AZURE_CLIENT_SECRET" ] || [ -z "$INTERCOM_ACCESS_TOKEN" ]; then
    echo "❌ Critical environment variables missing!"
    echo "📝 Please configure Azure and Intercom credentials in .env"
    echo "   Required: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, INTERCOM_ACCESS_TOKEN"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Creating directories..."
mkdir -p data logs config nginx/ssl

# Build e start dos containers
echo "🐳 Building and starting containers..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Aguardar serviços ficarem saudáveis
echo "⏳ Waiting for services to be healthy..."
timeout 120 bash -c '
    while ! docker-compose ps | grep -q "healthy"; do
        echo "Waiting for services..."
        sleep 5
    done
'

# Verificar status
echo "📊 Checking services status..."
docker-compose ps

# Teste básico
echo "🧪 Running basic health checks..."
sleep 10

# Test backend
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend health check passed"
else
    echo "⚠️  Backend health check failed"
fi

# Test frontend
if curl -f http://localhost:3000/nginx-health >/dev/null 2>&1; then
    echo "✅ Frontend health check passed"
else
    echo "⚠️  Frontend health check failed"
fi

echo ""
echo "✅ Deployment completed!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "📊 Health Check: http://localhost:8000/health"
echo ""
echo "🔧 To view logs:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"
