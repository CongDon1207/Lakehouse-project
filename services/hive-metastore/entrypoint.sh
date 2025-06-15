#!/bin/bash
set -e

# 1. Xóa SLF4J duplicate (tuỳ chọn)
rm -f /opt/hive/lib/slf4j-reload4j-1.7.36.jar || true

# 2. Init schema MySQL (chỉ chạy 1 lần)
echo "Initializing Hive Metastore schema on MySQL..."
schematool -dbType mysql -initSchema --verbose || echo "Schema already exists or init failed."

# 3. Start Metastore
echo "Starting Hive Metastore service..."
exec hive --service metastore -p 9083
