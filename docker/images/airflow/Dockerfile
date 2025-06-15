FROM apache/airflow:3.0.1

USER root

# Cài package hệ thống nếu cần (tuỳ chọn)
RUN apt-get update && apt-get install -y vim nano && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt để cài thêm Python package (nếu có)
COPY requirements.txt /requirements.txt
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
WORKDIR /opt/airflow
