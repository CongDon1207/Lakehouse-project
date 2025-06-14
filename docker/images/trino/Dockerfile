FROM trinodb/trino:468

USER root

# Cập nhật và cài tool bằng dnf (ảnh UBI sử dụng dnf thay vì apt)
RUN dnf update -y \
 && dnf install -y \
      curl \
      jq \
      wget \
      unzip \
      python3 \
      python3-pip \
 && dnf clean all \
 && pip3 install --no-cache-dir awscli

RUN mkdir -p /etc/trino/catalog

USER trino
