# tools/produce_csv_to_kafka.py
import csv, json, sys, os
from kafka import KafkaProducer

csv_file = "data/FootWare_Sales_Dataset/FootWare_Wholesale_Sales_Dataset.csv"
topic = "footware_sales"
bootstrap = "localhost:9094"

print("▶️  Khởi tạo KafkaProducer…")
producer = KafkaProducer(
    bootstrap_servers=[bootstrap],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

try:
    print(f"▶️  Bắt đầu đọc CSV và gửi tới topic `{topic}`…")
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
    os._exit(0)  # ép exit ngay, bypass mọi hook

except Exception as e:
    print("❌ Lỗi khi đẩy dữ liệu:", e)
    try:
        producer.close(timeout=5)
    except:
        pass
    os._exit(1)
