from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count, to_date, month, year


def main():
    """
    ETL job: đọc lớp Silver (Delta), tính các bảng tổng hợp cho Gold:
    1. Doanh thu, lợi nhuận theo ngày (daily_summary)
    2. Doanh thu, lợi nhuận theo thương hiệu (brand_performance)
    3. Doanh thu, lợi nhuận theo đại lý (dealer_performance)
    4. Tổng quan hàng tháng (monthly_summary)
    Ghi ra s3a://footware/gold dưới dạng Delta partitioned by năm và tháng.
    """
    spark = SparkSession.builder \
        .appName("Silver to Gold ETL for Footwear Sales") \
        .getOrCreate()

    silver_path = "s3a://footware/silver"
    gold_path = "s3a://footware/gold"

    # Đọc Silver
    df = spark.read.format("delta").load(silver_path)

    # Chuẩn bị cột năm, tháng
    df = df.withColumn("year", year(col("order_date"))) \
           .withColumn("month", month(col("order_date")))

    # 1. Tổng hợp hàng ngày
    daily_summary = df.groupBy("order_date").agg(
        _sum("total_revenue").alias("daily_revenue"),
        _sum("profit").alias("daily_profit"),
        _sum("quantity_sold").alias("daily_quantity")
    )

    # 2. Hiệu suất theo thương hiệu
    brand_performance = df.groupBy("Brand").agg(
        _sum("total_revenue").alias("revenue"),
        _sum("profit").alias("profit"),
        _sum("quantity_sold").alias("quantity_sold"),
        ( _sum("profit") / _sum("total_revenue") * 100 ).alias("profit_margin_pct")
    )

    # 3. Hiệu suất theo đại lý
    dealer_performance = df.groupBy("Dealer").agg(
        _sum("total_revenue").alias("revenue"),
        _sum("profit").alias("profit"),
        count("Dealer").alias("transactions"),
        _sum("quantity_sold").alias("quantity_sold")
    )

    # 4. Tổng quan hàng tháng
    monthly_summary = df.groupBy("year", "month").agg(
        _sum("total_revenue").alias("monthly_revenue"),
        _sum("profit").alias("monthly_profit"),
        _sum("quantity_sold").alias("monthly_quantity")
    )

    # Ghi các bảng ra Gold
    (daily_summary.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("order_date")
        .save(f"{gold_path}/daily_summary"))

    (brand_performance.write
        .format("delta")
        .mode("overwrite")
        .save(f"{gold_path}/brand_performance"))

    (dealer_performance.write
        .format("delta")
        .mode("overwrite")
        .save(f"{gold_path}/dealer_performance"))

    (monthly_summary.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("year", "month")
        .save(f"{gold_path}/monthly_summary"))

    spark.stop()


if __name__ == "__main__":
    main()
