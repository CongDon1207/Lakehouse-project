FROM apache/airflow:2.9.2

# Cài đặt các gói hệ thống
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        vim \
        nano \
        procps \
        curl \
        gnupg \
    # Cài đặt Docker CLI
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    # Dọn dẹp
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tạo group docker và thêm user airflow vào group đó
RUN groupadd docker || true \
    && usermod -aG docker airflow

# cài Python package dự án
ENV AIRFLOW_VERSION=2.9.2
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.12.txt"

COPY requirements.txt /requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt --constraint "${CONSTRAINT_URL}"

WORKDIR /opt/airflow