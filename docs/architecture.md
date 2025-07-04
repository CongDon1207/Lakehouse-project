# Kiến Trúc Lakehouse

Dự án này triển khai một kiến trúc data lakehouse hiện đại để xử lý và phân tích dữ liệu bán hàng giày dép. Nó tận dụng một bộ công cụ mã nguồn mở mạnh mẽ để xây dựng một đường ống dữ liệu (data pipeline) mạnh mẽ và có khả năng mở rộng, từ việc nhập dữ liệu (data ingestion) đến phân tích và trực quan hóa.

## Sơ đồ kiến trúc

![image alt](https://github.com/CongDon1207/lakehouse-analytics-platform/blob/7dffd00dfb085256fe8b2dfcbd11797400a2a90f/docs/images/architecture_lakehouse.png)

## Các thành phần chính

- **Data Lake (MinIO):** Được sử dụng làm data lake để lưu trữ dữ liệu thô và đã qua xử lý ở các vùng khác nhau (Bronze, Silver, và Gold).
- **Xử lý dữ liệu (Apache Spark):** Là công cụ xử lý chính để chuyển đổi dữ liệu giữa các lớp khác nhau của lakehouse.
- **Data Warehouse (Hive Metastore & Delta Lake):** Sự kết hợp giữa Apache Hive Metastore và Delta Lake cung cấp khả năng của một data warehouse trên nền tảng data lake.
- **Query Engine (Trino):** Được sử dụng làm công cụ truy vấn để thực hiện các truy vấn SQL tương tác nhanh trên dữ liệu trong lakehouse.
- **Orchestration (Apache Airflow):** Được sử dụng để điều phối đường ống dữ liệu, lập lịch và quản lý các tác vụ khác nhau.
- **Streaming Ingestion (Apache Kafka):** Được sử dụng để nhập dữ liệu thời gian thực vào lakehouse.
- **BI & Visualization (Apache Superset):** Được sử dụng để khám phá dữ liệu, trực quan hóa và tạo các dashboard tương tác.

## Kiến trúc Medallion

Dữ liệu được tổ chức theo kiến trúc "medallion" nhiều lớp để tinh chỉnh và xử lý dữ liệu một cách lũy tiến:

- **Lớp Bronze:** Lớp này chứa dữ liệu thô, được nhập từ Kafka topic. Dữ liệu được lưu trữ ở định dạng thô mà không có bất kỳ sự biến đổi nào.
- **Lớp Silver:** Dữ liệu từ lớp Bronze được làm sạch, xác thực và loại bỏ trùng lặp. Lớp này cung cấp một cái nhìn tinh chỉnh và có thể truy vấn được về dữ liệu.
- **Lớp Gold:** Lớp này chứa dữ liệu đã được tinh chỉnh và tổng hợp cao, sẵn sàng cho việc phân tích và business intelligence. Dữ liệu được tổ chức theo mô hình chiều để các công cụ BI dễ dàng sử dụng.
