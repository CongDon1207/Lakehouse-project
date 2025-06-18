FROM apache/airflow:2.9.2

# cài gói hệ thống nếu cần
USER root
RUN apt-get update && apt-get install -y vim nano && rm -rf /var/lib/apt/lists/*

# cài Python package dự án
#   - Dùng đúng constraints của Airflow 2.9.2 để bảo toàn dependency
ENV AIRFLOW_VERSION=2.9.2
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.12.txt"

COPY requirements.txt /requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt --constraint "${CONSTRAINT_URL}"

WORKDIR /opt/airflow
# ⬅️  KHÔNG ghi đè ENTRYPOINT – dùng mặc định của Apache Airflow
