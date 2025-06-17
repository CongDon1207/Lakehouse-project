from minio import Minio
from minio.error import S3Error

# Thông số MinIO
minio_client = Minio(
    endpoint="localhost:9000",          # Nếu chạy qua docker-compose, có thể là 'minio:9000'
    access_key="minio",
    secret_key="minio123",
    secure=False
)

bucket_name = "footware"
object_name = "bronze/FootWare_Wholesale_Sales_Dataset.csv"
local_file = "data/FootWare_Sales_Dataset/FootWare_Wholesale_Sales_Dataset.csv"

# Tạo bucket nếu chưa có
found = minio_client.bucket_exists(bucket_name)
if not found:
    minio_client.make_bucket(bucket_name)
    print(f"✅ Đã tạo bucket '{bucket_name}'")
else:
    print(f"ℹ️ Bucket '{bucket_name}' đã tồn tại.")

# Upload file
try:
    minio_client.fput_object(
        bucket_name,
        object_name,
        local_file,
        content_type="application/csv"
    )
    print(f"✅ Upload thành công: {local_file} → s3://{bucket_name}/{object_name}")
except S3Error as err:
    print("❌ Upload lỗi:", err)
