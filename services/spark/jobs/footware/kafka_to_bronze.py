from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType

spark = SparkSession.builder.appName("KafkaToBronzeFootware").getOrCreate()

# Định nghĩa schema cho dữ liệu
from pyspark.sql.types import *

schema = StructType() \
    .add("Date", StringType()) \
    .add("Product", StringType()) \
    .add("Brand", StringType()) \
    .add("Size", IntegerType()) \
    .add("Quantity Sold", IntegerType()) \
    .add("Unit Price (₹)", FloatType()) \
    .add("Margin (%)", StringType()) \
    .add("Profit (₹)", FloatType()) \
    .add("Net Profit (₹)", FloatType()) \
    .add("Total Revenue (₹)", FloatType()) \
    .add("Tax (GST % )", StringType()) \
    .add("Tax Amount (₹)", FloatType()) \
    .add("Net Tax (₹)", FloatType()) \
    .add("Dealer", StringType()) \
    .add("Stock Availability", IntegerType()) \
    .add("Dealer Location", StringType())


# Đọc stream từ Kafka
df_raw = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "footware_sales") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse dữ liệu JSON
df = df_raw.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

# Ghi ra MinIO (bronze layer, Parquet hoặc Delta)
df.writeStream \
    .format("parquet") \
    .option("path", "s3a://footware/bronze/") \
    .option("checkpointLocation", "s3a://footware/bronze/_checkpoint") \
    .outputMode("append") \
    .start() \
    .awaitTermination(timeout=10)
