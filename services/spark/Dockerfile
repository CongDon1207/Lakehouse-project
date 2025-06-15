# ----- Base: Spark + Hadoop 3.3 + OpenJDK 17 --------------------
FROM bitnami/spark:3.5.0

USER root

# Copy cấu hình Spark mặc định (S3a → MinIO)
COPY spark-defaults.conf /opt/bitnami/spark/conf/

# Cài thêm Python libs cho job
RUN pip install --no-cache-dir \
        boto3==1.34.81 \
        pandas==2.2.2

# (tuỳ chọn) Copy job mẫu để test
# COPY ../../spark_jobs /opt/spark_jobs
RUN echo "sparkuser:x:1001:0:Spark User:/opt/bitnami/spark:/bin/bash" >> /etc/passwd

RUN apt-get update && \
    apt-get install -y nano vim less && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
USER 1001   
# quay lại non-root (Bitnami convention)
