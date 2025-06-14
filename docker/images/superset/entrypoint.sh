#!/bin/bash
set -e

# 1. Khởi tạo DB, tạo user, init metadata
superset db upgrade

superset fab create-admin \
  --username "${ADMIN_USERNAME:-admin}" \
  --firstname "${ADMIN_FIRSTNAME:-admin}" \
  --lastname "${ADMIN_LASTNAME:-admin}" \
  --email "${ADMIN_EMAIL:-admin@localhost}" \
  --password "${ADMIN_PASSWORD:-admin123}" || true

superset init

# 2. Thêm kết nối Trino (dùng đúng command & flag)
superset set-database-uri \
  --database-name trino_conn \
  --uri "trino://trino@trino:8080/hive/default"

# 3. Start webserver
exec superset run -h 0.0.0.0 -p 8088
