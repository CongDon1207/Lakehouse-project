#!/bin/bash
set -e

# Thiết lập alias cho MinIO server
mc alias set local http://minio:9000 minio minio123

# Tạo các bucket nếu chưa tồn tại
mc mb -p local/bronze   || true
mc mb -p local/silver   || true
mc mb -p local/gold     || true

echo "✅ Bucket MinIO đã khởi tạo xong!"
