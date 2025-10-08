#!/bin/bash

set -e

echo "🧹 Cleaning up Teams-Intercom Integration..."

# Parar containers
echo "🛑 Stopping containers..."
docker-compose down --remove-orphans

# Remover imagens
echo "🗑️  Removing images..."
docker rmi teams-intercom-integration_backend:latest 2>/dev/null || echo "Backend image not found"
docker rmi teams-intercom-integration_frontend:latest 2>/dev/null || echo "Frontend image not found"

# Remover volumes (CUIDADO!)
read -p "⚠️  Remove volumes (will delete all data)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing volumes..."
    docker volume rm teams-intercom-integration_redis-data 2>/dev/null || echo "Redis volume not found"
fi

# Limpar imagens órfãs
echo "🧽 Cleaning up orphaned images..."
docker image prune -f

# Limpar containers parados
echo "🧽 Cleaning up stopped containers..."
docker container prune -f

# Limpar redes órfãs
echo "🧽 Cleaning up orphaned networks..."
docker network prune -f

echo "✅ Cleanup completed!"
echo "🔄 To redeploy, run: ./scripts/deploy.sh"
