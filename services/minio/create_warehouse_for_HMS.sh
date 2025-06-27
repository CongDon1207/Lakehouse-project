#!/bin/bash

set -e

# Thiết lập alias minio (bỏ qua nếu đã tồn tại)
mc alias set minio http://minio:9000 minio minio123 2>/dev/null || true

# Kiểm tra bucket warehouse đã tồn tại chưa
if mc ls minio | grep -qw warehouse; then
    echo "Bucket 'warehouse' đã tồn tại."
else
    echo "Bucket 'warehouse' chưa có, tiến hành tạo..."
    mc mb minio/warehouse
    echo "Đã tạo bucket 'warehouse'."
fi
