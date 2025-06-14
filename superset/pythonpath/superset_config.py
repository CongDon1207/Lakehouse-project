# superset_config.py

# Secret key (đặt giống biến env SUPERSET_SECRET_KEY để tránh warning)
SECRET_KEY = "thisisaverysecretkey"

# Sử dụng file SQLite cho metadata (dev/test), có thể chuyển sang Postgres/MySQL cho production
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

# Bật tính năng sample dashboard (nếu cần)
ENABLE_LOAD_EXAMPLES = True

# Cho phép CORS (dev/test API)
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": ["*"]
}

# Giới hạn upload file (MB)
MAX_UPLOAD_SIZE = 100

# Custom logo (tuỳ chọn)
# APP_ICON = "/static/assets/images/superset-logo-horiz.png"

# Email settings (tuỳ chọn)
# EMAIL_NOTIFICATIONS = True
# SMTP_HOST = "smtp.yourmail.com"
# SMTP_STARTTLS = True
# SMTP_SSL = False
# SMTP_USER = "user"
# SMTP_PORT = 587
# SMTP_PASSWORD = "password"
# SMTP_MAIL_FROM = "superset@yourdomain.com"
