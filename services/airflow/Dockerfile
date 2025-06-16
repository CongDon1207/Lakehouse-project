FROM apache/airflow:3.0.1

USER root

# Cài thêm package hệ thống nếu cần
RUN apt-get update && apt-get install -y vim nano && rm -rf /var/lib/apt/lists/*

# Cài thêm Python package nếu có
COPY requirements.txt /requirements.txt

# Copy entrypoint script vào image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER airflow
RUN pip install --no-cache-dir -r /requirements.txt
WORKDIR /opt/airflow

# Dùng entrypoint mới
ENTRYPOINT ["/entrypoint.sh"]
CMD ["api-server"]

