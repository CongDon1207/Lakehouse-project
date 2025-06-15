#!/bin/bash
set -e

# 1) Migrate DB (idempotent)
airflow db migrate

# 2) Tự động tạo Admin user nếu chưa tồn tại
if ! airflow users list | grep -qw "${ADMIN_USERNAME:-admin}"; then
  airflow users create \
    --username "${ADMIN_USERNAME:-admin}" \
    --password "${ADMIN_PASSWORD:-admin123}" \
    --firstname "${ADMIN_FIRSTNAME:-Admin}" \
    --lastname "${ADMIN_LASTNAME:-User}" \
    --role Admin \
    --email "${ADMIN_EMAIL:-admin@example.com}"
else
  echo "Admin user '${ADMIN_USERNAME:-admin}' already exists, skipping creation."
fi

# 3) Chạy lệnh chính (api-server hoặc scheduler)
exec airflow "$@"