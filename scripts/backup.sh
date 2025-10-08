#!/bin/bash

set -e

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup in $BACKUP_DIR..."

# Backup configurações
if [ -d "config" ]; then
    cp -r config "$BACKUP_DIR/"
    echo "✅ Config backed up"
fi

if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/.env.backup"
    echo "✅ Environment file backed up"
fi

# Backup data volume se existir
if docker volume ls | grep -q "teams-intercom-integration_redis-data"; then
    docker run --rm \
        -v teams-intercom-integration_redis-data:/data \
        -v "$PWD/$BACKUP_DIR":/backup \
        alpine tar czf /backup/redis-data.tar.gz -C /data . 2>/dev/null || echo "⚠️  Redis data backup failed"
    echo "✅ Redis data backed up"
fi

# Backup logs se existir
if [ -d "logs" ]; then
    cp -r logs "$BACKUP_DIR/"
    echo "✅ Logs backed up"
fi

# Backup docker images (opcional)
echo "💿 Backing up Docker images..."
docker save -o "$BACKUP_DIR/backend-image.tar" teams-intercom-integration_backend:latest 2>/dev/null || echo "⚠️  Backend image backup failed"
docker save -o "$BACKUP_DIR/frontend-image.tar" teams-intercom-integration_frontend:latest 2>/dev/null || echo "⚠️  Frontend image backup failed"

echo "✅ Backup completed: $BACKUP_DIR"
echo "📝 Backup contents:"
ls -la "$BACKUP_DIR"
