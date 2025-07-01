#!/bin/bash
set -e

echo "[Bitnami Kafka] Waiting for broker to be ready..."
while ! nc -z kafka 9092; do
  sleep 1
done

TOPIC=footware_sales

echo "[Bitnami Kafka] Checking if topic exists before delete…"
if /opt/bitnami/kafka/bin/kafka-topics.sh \
     --bootstrap-server kafka:9092 \
     --list | grep -q "^$TOPIC$"; then
  echo "[Bitnami Kafka] Deleting topic: $TOPIC"
  /opt/bitnami/kafka/bin/kafka-topics.sh \
    --bootstrap-server kafka:9092 \
    --delete \
    --topic "$TOPIC"
else
  echo "[Bitnami Kafka] Topic '$TOPIC' not found, skipping delete"
fi

# phần tạo topic cứ để nguyên như trước…
echo "[Bitnami Kafka] Creating topic: $TOPIC"
/opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --create \
  --replication-factor 1 \
  --partitions 1 \
  --topic "$TOPIC"

echo "[Bitnami Kafka] Topic recreated clean."