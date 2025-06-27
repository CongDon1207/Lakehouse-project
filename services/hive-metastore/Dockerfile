FROM apache/hive:4.0.0

# —— Versions ——
ARG HADOOP_VER=3.3.6
ARG AWS_BUNDLE_VER=1.12.641

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Hive config
COPY conf/hive-site.xml /opt/hive/conf/hive-site.xml

# MySQL driver + S3A
RUN wget -qO /opt/hive/lib/mysql-connector-j-8.3.0.jar \
        https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.3.0/mysql-connector-j-8.3.0.jar && \
    wget -qO /opt/hive/lib/hadoop-aws-${HADOOP_VER}.jar \
        https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VER}/hadoop-aws-${HADOOP_VER}.jar && \
    wget -qO /opt/hive/lib/aws-java-sdk-bundle-${AWS_BUNDLE_VER}.jar \
        https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_BUNDLE_VER}/aws-java-sdk-bundle-${AWS_BUNDLE_VER}.jar

ENV HIVE_AUX_JARS_PATH=/opt/hive/lib

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER 1000
ENTRYPOINT ["/entrypoint.sh"]
