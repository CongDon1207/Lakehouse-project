#!/bin/bash
set -e

echo "[Bitnami Kafka] Waiting for broker to be ready..."
while ! nc -z kafka 9092; do
  sleep 1
done

TOPIC=footware_sales

echo "[Bitnami Kafka] Deleting topic if it exists: $TOPIC"
/opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --delete \
  --topic "$TOPIC" || true

# Đợi topic thực sự bị xóa
echo "[Bitnami Kafka] Waiting for topic '$TOPIC' to be deleted..."
while /opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list | grep -q "^$TOPIC$"; do
  sleep 1
done

echo "[Bitnami Kafka] Creating topic: $TOPIC"
/opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --create \
  --replication-factor 1 \
  --partitions 1 \
  --topic "$TOPIC"

echo "[Bitnami Kafka] Topic recreated clean."
