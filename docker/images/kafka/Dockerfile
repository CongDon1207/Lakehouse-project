FROM bitnami/kafka:3.9.0

USER root

# Cài thêm tool nếu cần
RUN install_packages curl jq netcat-openbsd

# Copy script tạo topic
COPY create-topic.sh /opt/bitnami/kafka/create-topic.sh
RUN chmod +x /opt/bitnami/kafka/create-topic.sh

USER 1001
