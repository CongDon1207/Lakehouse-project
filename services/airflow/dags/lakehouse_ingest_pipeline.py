from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='lakehouse_ingest_pipeline',
    default_args=default_args,
    description='Nạp dữ liệu CSV vào Kafka, chạy Spark streaming ghi Bronze',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    produce_csv = BashOperator(
        task_id='produce_csv_to_kafka',
        bash_command=(
            "python /opt/airflow/tools/produce_csv_to_kafka.py "
            "--bootstrap-server kafka:9092 "
            "--topic footware_sales "
            "--file /opt/airflow/data/FootWare_Sales_Dataset/FootWare_Wholesale_Sales_Dataset.csv"
        )
    )

    # Chạy Spark job thông qua docker exec vào container spark
    spark_streaming = BashOperator(
        task_id='spark_streaming_bronze',
        bash_command=(
            "docker exec spark "
            "/opt/bitnami/spark/bin/spark-submit "
            "/opt/bitnami/spark/spark_jobs/footware/kafka_to_bronze.py"
        )
    )

    produce_csv >> spark_streaming