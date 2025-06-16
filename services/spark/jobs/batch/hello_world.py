from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("HelloWorld").getOrCreate()

df = spark.createDataFrame([{"msg": "hello, lakehouse!"}])
df.write.mode("overwrite").parquet("s3a://bronze/hello.parquet")
print("Done!")

spark.stop()
