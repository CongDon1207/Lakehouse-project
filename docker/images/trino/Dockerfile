FROM trinodb/trino:468

USER root

# Cập nhật và cài thêm tool bằng apt
RUN apt-get update \
 && apt-get install -y \
      curl \
      jq \
      wget \
      unzip \
      python3 \
      python3-pip \
 && pip3 install --no-cache-dir awscli \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/trino/catalog

USER trino
