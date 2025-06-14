FROM apache/superset:4.1.2

USER root
# Cài thêm các thư viện cần thiết
RUN pip install --no-cache-dir \
    trino[sqlalchemy] \
    pandas \
    openpyxl \
    pillow \
    flask_cors

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER superset
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
