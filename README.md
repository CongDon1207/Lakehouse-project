# Dự án Lakehouse

Dự án này triển khai một kiến trúc data lakehouse hiện đại để xử lý và phân tích dữ liệu bán hàng giày dép. Nó tận dụng một bộ công cụ mã nguồn mở mạnh mẽ để xây dựng một đường ống dữ liệu (data pipeline) mạnh mẽ và có khả năng mở rộng, từ việc nhập dữ liệu (data ingestion) đến phân tích và trực quan hóa.


## Kiến trúc

Kiến trúc lakehouse được xây dựng bằng Docker và bao gồm các thành phần sau:

*   **Data Lake:** [MinIO](https://min.io/) được sử dụng làm data lake để lưu trữ dữ liệu thô và đã qua xử lý ở các vùng khác nhau (Bronze, Silver, và Gold).
*   **Xử lý dữ liệu:** [Apache Spark](https://spark.apache.org/) là công cụ xử lý chính để chuyển đổi dữ liệu giữa các lớp khác nhau của lakehouse.
*   **Data Warehouse:** Dự án sử dụng sự kết hợp của [Apache Hive Metastore](https://cwiki.apache.org/confluence/display/hive/hms) và [Delta Lake](https://delta.io/) để cung cấp khả năng của một data warehouse trên nền tảng data lake.
*   **Query Engine:** [Trino](https://trino.io/) (trước đây là PrestoSQL) được sử dụng làm công cụ truy vấn để thực hiện các truy vấn SQL tương tác nhanh trên dữ liệu trong lakehouse.
*   **Orchestration (Điều phối):** [Apache Airflow](https://airflow.apache.org/) được sử dụng để điều phối đường ống dữ liệu, lập lịch và quản lý các tác vụ khác nhau.
*   **Streaming Ingestion (Nhập dữ liệu streaming):** [Apache Kafka](https://kafka.apache.org/) được sử dụng để nhập dữ liệu thời gian thực vào lakehouse.
*   **BI & Trực quan hóa:** [Apache Superset](https://superset.apache.org/) được sử d���ng để khám phá dữ liệu, trực quan hóa và tạo các dashboard tương tác.

### Kiến trúc Medallion

Dữ liệu được tổ chức theo kiến trúc "medallion" nhiều lớp để tinh chỉnh và xử lý dữ liệu một cách lũy tiến:

*   **Lớp Bronze:** Lớp này chứa dữ liệu thô, được nhập từ Kafka topic. Dữ liệu được lưu trữ ở định dạng thô mà không có bất kỳ sự biến đổi nào.
*   **Lớp Silver:** Dữ liệu từ lớp Bronze được làm sạch, xác thực và loại bỏ trùng lặp. Lớp này cung cấp một cái nhìn tinh chỉnh và có thể truy vấn được về dữ liệu.
*   **Lớp Gold:** Lớp này chứa dữ liệu đã được tinh chỉnh và tổng hợp cao, sẵn sàng cho việc phân tích và business intelligence. Dữ liệu được tổ chức theo mô hình chiều để các công cụ BI dễ dàng sử dụng.

## Bắt đầu

Để bắt đầu với dự án, bạn cần cài đặt Docker và Docker Compose trên hệ thống của mình.

1.  **Clone repository:**
    ```bash
    git clone https://github.com/your-username/Lakehouse-project.git
    cd Lakehouse-project
    ```

2.  **Build các Docker image:**
    ```bash
    docker-compose -f docker-compose.build.yml build
    ```

3.  **Chạy các service:**
    ```bash
    docker-compose -f docker-compose.run.yml up -d
    ```

## Sử dụng

Khi các service đã hoạt động, bạn có thể truy cập các thành phần khác nhau:

*   **MinIO Console:** http://localhost:9001
*   **Trino UI:** http://localhost:8081
*   **Airflow UI:** http://localhost:8082
*   **Spark UI:** http://localhost:4040
*   **Superset UI:** http://localhost:8088

### Đường ống dữ liệu

Đường ống dữ liệu được điều phối bởi Airflow và bao gồm các giai đoạn sau:

1.  **Ingestion:** DAG `lakehouse_ingest_pipeline` trong Airflow đọc dữ liệu bán hàng giày dép từ tệp CSV và đưa vào một Kafka topic.
2.  **Lớp Bronze:** Một Spark streaming job đọc dữ liệu từ Kafka và ghi vào lớp Bronze trong data lake ở định dạng Delta.
3.  **Lớp Silver:** Một Spark job khác đọc dữ liệu từ lớp Bronze, thực hiện làm sạch và chuyển đổi dữ liệu, và ghi vào lớp Silver.
4.  **Lớp Gold:** Một Spark job cuối cùng tổng hợp dữ liệu từ lớp Silver để tạo ra các bảng cấp doanh nghiệp trong lớp Gold, được tối ưu hóa cho việc phân tích.

### Phân tích

Bạn có thể sử dụng Trino để truy vấn dữ liệu trong lakehouse và Superset để tạo các dashboard và trực quan hóa.
![image alt](https://github.com/CongDon1207/Lakehouse-project/blob/727c1e14e5abc9572d8722c2e4d9cb26239183b7/docs/images/dashboard%201.png)

## Các công cụ đã sử dụng

*   [Docker](https://www.docker.com/)
*   [MinIO](https://min.io/)
*   [Apache Spark](https://spark.apache.org/)
*   [Apache Hive Metastore](https://cwiki.apache.org/confluence/display/hive/hms)
*   [Delta Lake](https://delta.io/)
*   [Trino](https://trino.io/)
*   [Apache Airflow](https://airflow.apache.org/)
*   [Apache Kafka](https://kafka.apache.org/)
*   [Apache Superset](https://superset.apache.org/)
