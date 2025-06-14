FROM trinodb/trino:468

USER root

# Cập nhật và cài tool thông qua microdnf (ảnh UBI minimal không có apt)
RUN microdnf update -y \
 && microdnf install -y \
      curl \
      jq \
      wget \
      unzip \
      python3 \
      python3-pip \
 && microdnf clean all \
 && pip3 install --no-cache-dir awscli

RUN mkdir -p /etc/trino/catalog

USER trino
