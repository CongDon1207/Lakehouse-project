# Cài đặt

Để bắt đầu với dự án, bạn cần cài đặt Docker và Docker Compose trên hệ thống của mình.

1. **Clone repository:**
   ```bash
   git clone https://github.com/your-username/Lakehouse-project.git
   cd Lakehouse-project
   ```

2. **Build các Docker image:**
   ```bash
   docker-compose -f docker-compose.build.yml build
   ```

3. **Chạy các service:**
   ```bash
   docker-compose -f docker-compose.run.yml up -d
   ```
