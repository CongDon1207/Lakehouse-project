# services/spark/jobs/test/test_s3a.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TestS3A").getOrCreate()

# Test tạo một file đơn giản
df = spark.createDataFrame([{"test": "hello"}])
df.write.mode("overwrite").parquet("s3a://footware/test/")
print("✅ S3A connection works!")

spark.stop()