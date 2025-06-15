#!/bin/bash
set -e

echo "[Bitnami Kafka] Waiting for broker to be ready..."
while ! nc -z kafka 9092; do
  sleep 1
done

echo "[Bitnami Kafka] Creating topic: quick_test"
/opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --create \
  --if-not-exists \
  --replication-factor 1 \
  --partitions 1 \
  --topic quick_test

echo "[Bitnami Kafka] Topic created."

