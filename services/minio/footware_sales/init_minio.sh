#!/bin/bash
set -e

# Tạo alias
mc alias set local http://minio:9000 minio minio123

# Tạo 1 bucket duy nhất cho domain
mc mb -p local/footware || true

echo "✅ Bucket 'footware' đã tạo. Các tầng sẽ dùng prefix:"
echo "   - footware/bronze/"
echo "   - footware/silver/"
echo "   - footware/gold/"
