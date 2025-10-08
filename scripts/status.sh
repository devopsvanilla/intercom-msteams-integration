#!/bin/bash

echo "🔍 Teams-Intercom Integration Status"
echo "=================================="

# Docker Compose Status
echo "📊 Services Status:"
docker-compose ps 2>/dev/null || echo "❌ Docker Compose not running"

echo ""
echo "🏥 Health Checks:"

# Backend Health
if curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend: healthy"
    curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Backend responding"
else
    echo "❌ Backend: unhealthy"
fi

# Frontend Health
if curl -f -s http://localhost:3000/nginx-health >/dev/null 2>&1; then
    echo "✅ Frontend: healthy"
else
    echo "❌ Frontend: unhealthy"
fi

# Redis Health (se estiver rodando)
if docker ps | grep -q "teams-intercom-redis"; then
    if docker exec teams-intercom-redis redis-cli ping >/dev/null 2>&1; then
        echo "✅ Redis: healthy"
    else
        echo "❌ Redis: unhealthy"
    fi
fi

echo ""
echo "💾 Volumes:"
docker volume ls | grep teams-intercom || echo "No persistent volumes found"

echo ""
echo "🌐 Endpoints:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  Health:      http://localhost:8000/health"

echo ""
echo "📊 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Cannot get stats"

echo ""
echo "🪵 Recent Logs (last 10 lines):"
echo "--- Backend ---"
docker-compose logs --tail=5 backend 2>/dev/null || echo "No backend logs"
echo "--- Frontend ---"
docker-compose logs --tail=5 frontend 2>/dev/null || echo "No frontend logs"
