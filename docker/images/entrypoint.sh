#!/bin/bash
set -e

# 1. Khởi tạo/migrate DB (idempotent)
superset db upgrade

# 2. Tạo admin user nếu chưa có
superset fab create-admin \
  --username "${ADMIN_USERNAME:-admin}" \
  --firstname "${ADMIN_FIRSTNAME:-admin}" \
  --lastname "${ADMIN_LASTNAME:-admin}" \
  --email "${ADMIN_EMAIL:-admin@localhost}" \
  --password "${ADMIN_PASSWORD:-admin123}" || true

# 3. Init các metadata default (roles, permissions…)
superset init

# 4. Khởi động Superset webserver
exec superset run -h 0.0.0.0 -p 8088
