from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, regexp_replace
from pyspark.sql.types import IntegerType, DoubleType


def main():
    """
    ETL job: đọc dữ liệu Bronze (Parquet), kiểm tra schema, xử lý và ghi ra Silver dưới dạng Delta partitioned by order_date.
    """
    spark = SparkSession.builder \
        .appName("Bronze to Silver ETL for Footwear Sales") \
        .getOrCreate()

    bronze_path = "s3a://footware/bronze"
    silver_path = "s3a://footware/silver"

    # 1. Đọc Bronze và kiểm tra schema
    df = spark.read.format("parquet").load(bronze_path)
    print("=== Bronze Schema ===")
    df.printSchema()
    print("=== Bronze Sample ===")
    df.show(5, truncate=False)

    # 2. Rename cột để dễ sử dụng
    df = (df
        .withColumnRenamed("Quantity Sold",        "quantity_sold")
        .withColumnRenamed("Unit Price (\u20b9)",  "unit_price")
        .withColumnRenamed("Margin (%)",           "margin_percentage")
        .withColumnRenamed("Profit (\u20b9)",      "profit")
        .withColumnRenamed("Net Profit (\u20b9)",  "net_profit")
        .withColumnRenamed("Total Revenue (\u20b9)","total_revenue")
        .withColumnRenamed("Tax (GST % )",         "tax_gst_percentage")
        .withColumnRenamed("Tax Amount (\u20b9)",  "tax_amount")
        .withColumnRenamed("Net Tax (\u20b9)",     "net_tax")
        .withColumnRenamed("Dealer",               "dealer")
        .withColumnRenamed("Stock Availability",   "stock_availability")
        .withColumnRenamed("Dealer Location",      "dealer_location")
    )

    # 3. Loại bỏ '%' và cast các cột percent sang Double
    df = (df
        .withColumn("margin_percentage", regexp_replace(col("margin_percentage"), "%", "").cast(DoubleType()))
        .withColumn("tax_gst_percentage", regexp_replace(col("tax_gst_percentage"), "%", "").cast(DoubleType()))
    )

    # 4. Chuyển kiểu dữ liệu còn lại
    df = (df
        .withColumn("order_date", to_date(col("Date"), "dd-MM-yyyy"))
        .withColumn("unit_price", col("unit_price").cast(DoubleType()))
        .withColumn("profit", col("profit").cast(DoubleType()))
        .withColumn("net_profit", col("net_profit").cast(DoubleType()))
        .withColumn("total_revenue", col("total_revenue").cast(DoubleType()))
        .withColumn("tax_amount", col("tax_amount").cast(DoubleType()))
        .withColumn("net_tax", col("net_tax").cast(DoubleType()))
        .withColumn("quantity_sold", col("quantity_sold").cast(IntegerType()))
        .withColumn("stock_availability", col("stock_availability").cast(IntegerType()))
        .withColumn("Size", col("Size").cast(IntegerType()))
    )

    # 5. Loại bỏ nulls ở order_date
    df_clean = df.na.drop(subset=["order_date"])
    print(f"Rows after drop null order_date: {df_clean.count()}")

    # 6. Chọn cột final và ghi ra Silver
    df_silver = df_clean.select(
        "order_date", "Product", "Brand", "Size", "quantity_sold",
        "unit_price", "margin_percentage", "profit", "net_profit",
        "total_revenue", "tax_gst_percentage", "tax_amount", "net_tax",
        "Dealer", "stock_availability", "dealer_location"
    )

    df_silver.write \
        .format("delta") \
        .mode("overwrite") \
        .partitionBy("order_date") \
        .save(silver_path)

    print("ETL completed: Silver layer written with partitions.")
    spark.stop()


if __name__ == "__main__":
    main()
