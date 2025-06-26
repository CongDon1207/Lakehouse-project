
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, regexp_replace
from pyspark.sql.types import IntegerType, DoubleType

def main():
    """
    Main function to run the Spark job.
    Reads data from the Bronze layer, cleans and transforms it,
    and writes it to the Silver layer.
    """
    spark = SparkSession.builder         .appName("Bronze to Silver ETL for Footwear Sales")         .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")         .config("spark.hadoop.fs.s3a.access.key", "minio")         .config("spark.hadoop.fs.s3a.secret.key", "minio123")         .config("spark.hadoop.fs.s3a.path.style.access", "true")         .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")         .getOrCreate()

    # Define paths
    bronze_path = "s3a://footware-sales/bronze/sales_data"
    silver_path = "s3a://footware-sales/silver/sales_data"

    # Read data from Bronze layer
    df_bronze = spark.read.format("delta").load(bronze_path)

    # --- Transformations and Cleaning ---

    # 1. Rename columns to be more friendly
    df_renamed = df_bronze         .withColumnRenamed("Unit Price (₹)", "unit_price")         .withColumnRenamed("Margin (%)", "margin_percentage")         .withColumnRenamed("Profit (₹)", "profit")         .withColumnRenamed("Net Profit (₹)", "net_profit")         .withColumnRenamed("Total Revenue (₹)", "total_revenue")         .withColumnRenamed("Tax (GST % )", "tax_gst_percentage")         .withColumnRenamed("Tax Amount (₹)", "tax_amount")         .withColumnRenamed("Net Tax (₹)", "net_tax")         .withColumnRenamed("Quantity Sold", "quantity_sold")         .withColumnRenamed("Stock Availability", "stock_availability")         .withColumnRenamed("Dealer Location", "dealer_location")

    # 2. Correct data types
    df_typed = df_renamed         .withColumn("order_date", to_date(col("Date"), "dd-MM-yyyy"))         .withColumn("unit_price", col("unit_price").cast(DoubleType()))         .withColumn("margin_percentage", col("margin_percentage").cast(DoubleType()))         .withColumn("profit", col("profit").cast(DoubleType()))         .withColumn("net_profit", col("net_profit").cast(DoubleType()))         .withColumn("total_revenue", col("total_revenue").cast(DoubleType()))         .withColumn("tax_gst_percentage", col("tax_gst_percentage").cast(DoubleType()))         .withColumn("tax_amount", col("tax_amount").cast(DoubleType()))         .withColumn("net_tax", col("net_tax").cast(DoubleType()))         .withColumn("quantity_sold", col("quantity_sold").cast(IntegerType()))         .withColumn("stock_availability", col("stock_availability").cast(IntegerType()))         .withColumn("Size", col("Size").cast(IntegerType()))

    # 3. Handle nulls and duplicates
    # For this example, we'll drop rows with nulls in key columns like 'order_date' or 'Product'
    df_cleaned = df_typed.na.drop(subset=["order_date", "Product", "total_revenue"])
    df_final = df_cleaned.dropDuplicates()

    # Select final columns and partition by date for efficiency
    df_silver = df_final.select(
        "order_date",
        "Product",
        "Brand",
        "Size",
        "quantity_sold",
        "unit_price",
        "margin_percentage",
        "profit",
        "net_profit",
        "total_revenue",
        "tax_gst_percentage",
        "tax_amount",
        "net_tax",
        "Dealer",
        "stock_availability",
        "dealer_location"
    )

    # Write data to Silver layer in Parquet format, partitioned by order_date
    print("Writing cleaned data to Silver layer...")
    df_silver.write         .mode("overwrite")         .partitionBy("order_date")         .format("delta")         .save(silver_path)

    print("Bronze to Silver ETL job completed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()
