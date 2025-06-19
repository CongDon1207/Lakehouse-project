# tools/produce_csv_to_kafka.py
import csv, json, sys, os, argparse
from kafka import KafkaProducer

# Parse arguments
parser = argparse.ArgumentParser(description='Produce CSV data to Kafka')
parser.add_argument('--bootstrap-server', default='kafka:9092', help='Kafka bootstrap server')
parser.add_argument('--topic', default='footware_sales', help='Kafka topic')
parser.add_argument('--file', required=True, help='CSV file path')
args = parser.parse_args()

# Sử dụng các tham số từ command line
csv_file = args.file
topic = args.topic
bootstrap = args.bootstrap_server

print(f"▶️  Khởi tạo KafkaProducer tới {bootstrap}…")
try:
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print(f"▶️  Bắt đầu đọc CSV {csv_file} và gửi tới topic `{topic}`…")
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            producer.send(topic, row)
            if i % 100 == 0:
                print(f"  • Đã gửi {i} messages…")
        print(f"▶️  Đã gửi xong {i} messages, chuẩn bị flush…")

    # Flush với timeout 30 giây
    try:
        producer.flush(timeout=30)
        print("✔️  Flush thành công.")
    except Exception as e:
        print("⚠️  Flush bị timeout hoặc lỗi:", e)

    # Close với timeout 10 giây
    try:
        producer.close(timeout=10)
        print("✔️  Producer close thành công.")
    except Exception as e:
        print("⚠️  Close bị timeout hoặc lỗi:", e)

    print("✅ Đã đẩy toàn bộ dữ liệu, script sẽ exit ngay.")
    sys.exit(0)  # Sử dụng sys.exit thay vì os._exit để an toàn hơn

except Exception as e:
    print("❌ Lỗi khi đẩy dữ liệu:", e)
    try:
        if 'producer' in locals():
            producer.close(timeout=5)
    except:
        pass
    sys.exit(1)