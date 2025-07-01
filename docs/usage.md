# Sử dụng

Khi các service đã hoạt động, bạn có thể truy cập các thành phần khác nhau:

- **MinIO Console:** http://localhost:9001
- **Trino UI:** http://localhost:8081
- **Airflow UI:** http://localhost:8082
- **Spark UI:** http://localhost:4040
- **Superset UI:** http://localhost:8088

## Đường ống dữ liệu (Data Pipeline)

Đường ống dữ liệu được điều phối bởi Airflow và bao gồm các giai đoạn sau:

1. **Ingestion:** DAG `lakehouse_ingest_pipeline` trong Airflow đọc dữ liệu bán hàng giày dép từ tệp CSV và đưa vào một Kafka topic.
2. **Lớp Bronze:** Một Spark streaming job đọc dữ liệu từ Kafka và ghi vào lớp Bronze trong data lake ở định dạng Delta.
3. **Lớp Silver:** Một Spark job khác đọc dữ liệu từ lớp Bronze, thực hiện làm sạch và chuyển đổi dữ liệu, và ghi vào lớp Silver.
4. **Lớp Gold:** Một Spark job cuối cùng tổng hợp dữ liệu từ lớp Silver để tạo ra các bảng cấp doanh nghiệp trong lớp Gold, được tối ưu hóa cho việc phân tích.

## Phân tích

Bạn có thể sử dụng Trino để truy vấn dữ liệu trong lakehouse và Superset để tạo các dashboard và trực quan hóa.
