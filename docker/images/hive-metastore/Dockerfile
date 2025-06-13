FROM apache/hive:4.0.0

USER root

# Copy file hive-site.xml vào image (bạn tự tạo file này ở cùng Dockerfile)
COPY hive-site.xml /opt/hive/conf/hive-site.xml

# Tải driver MySQL
RUN wget -qO /opt/hive/lib/mysql-connector-j-8.3.0.jar \
    https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.3.0/mysql-connector-j-8.3.0.jar

USER 1000
ENV SERVICE_NAME=metastore
