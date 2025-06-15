FROM apache/hive:4.0.0

USER root

# Copy file hive-site.xml vào image (bạn tự tạo file này ở cùng Dockerfile)
COPY hive-site.xml /opt/hive/conf/hive-site.xml

# Cài wget (nếu ảnh gốc chưa có) và tải driver MySQL
RUN apt-get update && \
    apt-get install -y wget && \
    wget -qO /opt/hive/lib/mysql-connector-j-8.3.0.jar \
        https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.3.0/mysql-connector-j-8.3.0.jar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Không cần SERVICE_NAME nữa vì entrypoint sẽ start metastore
USER 1000
ENTRYPOINT ["/entrypoint.sh"]
