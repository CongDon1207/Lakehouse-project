from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

spark = (SparkSession.builder
         .appName("KafkaToBronzeFootware")
         .getOrCreate())

# 1️⃣ Schema thô – tất cả String
raw_schema = (StructType()
    .add("Date",               StringType())
    .add("Product",            StringType())
    .add("Brand",              StringType())
    .add("Size",               StringType())
    .add("Quantity Sold",      StringType())
    .add("Unit Price (\u20b9)",StringType())
    .add("Margin (%)",         StringType())
    .add("Profit (\u20b9)",    StringType())
    .add("Net Profit (\u20b9)",StringType())
    .add("Total Revenue (\u20b9)", StringType())
    .add("Tax (GST % )",       StringType())
    .add("Tax Amount (\u20b9)",StringType())
    .add("Net Tax (\u20b9)",   StringType())
    .add("Dealer",             StringType())
    .add("Stock Availability", StringType())
    .add("Dealer Location",    StringType())
)

# 2️⃣ Đọc từ Kafka
kafka_stream = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "footware_sales")
    .option("startingOffsets", "earliest")
    .load())

# 3️⃣ Parse JSON → DataFrame thô (bronze)
bronze = (kafka_stream
    .selectExpr("CAST(value AS STRING) AS json_str")
    .select(from_json(col("json_str"), raw_schema).alias("data"))
    .select("data.*"))

# 4️⃣ Ghi xuống MinIO (Parquet – đổi thành "delta" nếu dùng Delta Lake)
(bronze.writeStream
    .format("parquet")
    .option("path", "s3a://footware/bronze/")         # thư mục dữ liệu thô
    .option("checkpointLocation", "s3a://footware/bronze/_checkpoint")
    .outputMode("append")
    .start()
    .awaitTermination(timeout = 60))                              # chạy liên tục; dừng Ctrl-C
