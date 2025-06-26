from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count

def main():
    """
    Main function to run the Spark job.
    Reads data from the Silver layer, creates aggregated tables,
    and writes them to the Gold layer.
    """
    spark = SparkSession.builder         .appName("Silver to Gold ETL for Footwear Sales")         .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")         .config("spark.hadoop.fs.s3a.access.key", "minio")         .config("spark.hadoop.fs.s3a.secret.key", "minio123")         .config("spark.hadoop.fs.s3a.path.style.access", "true")         .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")         .getOrCreate()

    # Define paths
    silver_path = "s3a://footware-sales/silver/sales_data"
    gold_path_daily = "s3a://footware-sales/gold/daily_sales_summary"
    gold_path_product = "s3a://footware-sales/gold/product_sales_summary"

    # Read data from Silver layer
    df_silver = spark.read.format("delta").load(silver_path)

    # --- Aggregations for Gold Layer ---

    # 1. Create Daily Sales Summary table
    print("Creating daily sales summary...")
    df_daily_summary = df_silver         .groupBy("order_date")         .agg(
            sum("total_revenue").alias("total_daily_revenue"),
            sum("quantity_sold").alias("total_daily_quantity_sold"),
            sum("net_profit").alias("total_daily_net_profit"),
            count("*").alias("daily_transaction_count")
        )

    # Write daily summary to Gold layer
    df_daily_summary.write         .mode("overwrite")         .format("delta")         .save(gold_path_daily)
    print(f"Successfully wrote daily sales summary to {gold_path_daily}")

    # 2. Create Product Sales Summary table
    print("Creating product sales summary...")
    df_product_summary = df_silver         .groupBy("Product", "Brand")         .agg(
            sum("total_revenue").alias("total_revenue_per_product"),
            sum("quantity_sold").alias("total_quantity_sold_per_product"),
            sum("net_profit").alias("total_net_profit_per_product"),
            avg("unit_price").alias("average_unit_price")
        )

    # Write product summary to Gold layer
    df_product_summary.write         .mode("overwrite")         .format("delta")         .save(gold_path_product)
    print(f"Successfully wrote product sales summary to {gold_path_product}")

    print("Silver to Gold ETL job completed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()
