#!/bin/bash
set -e

echo "🛠️ Đổi tất cả services/*/entrypoint.sh sang UNIX line ending..."

for file in services/*/entrypoint.sh; do
    if [ -f "$file" ]; then
        dos2unix "$file"
        echo "  Đã fix: $file"
    fi
done

echo "🚀 Build lại Docker images..."
docker compose -f docker-compose.build.yml build

echo "✅ Đã fix format và build lại xong!"
