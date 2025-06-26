# ----- Base: Spark + Hadoop 3.3 + OpenJDK 17 --------------------
FROM bitnami/spark:3.5.0

USER root

# Cài đặt wget và các tools cần thiết trước
RUN apt-get update && \
    apt-get install -y nano vim less wget curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy cấu hình Spark mặc định (S3a → MinIO)
COPY conf/spark-defaults.conf /opt/bitnami/spark/conf/

# Download Kafka JAR dependencies
RUN wget -O /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    wget -O /opt/bitnami/spark/jars/kafka-clients-3.4.0.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar && \
    wget -O /opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar && \
    wget -O /opt/bitnami/spark/jars/commons-pool2-2.11.1.jar \
    https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar && \
    wget -O /opt/bitnami/spark/jars/hadoop-aws-3.3.6.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar && \
    wget -O /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.641.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.641/aws-java-sdk-bundle-1.12.641.jar

# Cài thêm Python libs cho job
RUN pip install --no-cache-dir \
        boto3==1.34.81 \
        pandas==2.2.2

RUN echo "sparkuser:x:1001:0:Spark User:/opt/bitnami/spark:/bin/bash" >> /etc/passwd

USER 1001