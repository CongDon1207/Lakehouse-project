from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleStreaming").getOrCreate()

# Đọc dữ liệu liên tục từ S3 (MinIO)
df = spark.readStream.format("csv") \
    .option("header", "true") \
    .schema("id INT, value STRING") \
    .load("s3a://bronze/stream_input/")

# Xử lý giả lập (ở đây chỉ pass qua)
query = df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "s3a://bronze/checkpoint/") \
    .option("path", "s3a://silver/stream_output/") \
    .outputMode("append") \
    .start()

query.awaitTermination(60)
