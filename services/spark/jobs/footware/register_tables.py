# services/spark/jobs/footware/register_tables.py
from pyspark.sql import SparkSession


def main():
    """Đăng ký các bảng Silver và Gold vào Hive Metastore."""
    spark = (
        SparkSession.builder
        .appName("RegisterFootwareTables")
        .enableHiveSupport()
        .getOrCreate()
    )

    # Tạo database nếu chưa có
    spark.sql("CREATE DATABASE IF NOT EXISTS footware")

    # Bảng Silver
    spark.sql(
        """
        CREATE TABLE IF NOT EXISTS footware.silver_sales
        USING DELTA
        LOCATION 's3a://footware/silver'
        """
    )

    # Các bảng Gold
    spark.sql(
        """
        CREATE TABLE IF NOT EXISTS footware.daily_summary
        USING DELTA
        LOCATION 's3a://footware/gold/daily_summary'
        """
    )

    spark.sql(
        """
        CREATE TABLE IF NOT EXISTS footware.brand_performance
        USING DELTA
        LOCATION 's3a://footware/gold/brand_performance'
        """
    )

    spark.sql(
        """
        CREATE TABLE IF NOT EXISTS footware.dealer_performance
        USING DELTA
        LOCATION 's3a://footware/gold/dealer_performance'
        """
    )

    spark.sql(
        """
        CREATE TABLE IF NOT EXISTS footware.monthly_summary
        USING DELTA
        LOCATION 's3a://footware/gold/monthly_summary'
        """
    )

    print("\u2705 \u0110\u00e3 \u0111\u0103ng k\u00fd b\u1ea3ng Silver v\u00e0 Gold v\u00e0o Hive Metastore.")
    spark.stop()


if __name__ == "__main__":
    main()
