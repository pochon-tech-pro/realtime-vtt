# Dockerfile
FROM php:8.2-apache

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python仮想環境の作成とアクティベート
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 仮想環境内に必要なPythonパッケージをインストール
RUN pip install openai websockets asyncio python-dotenv

# PHP WebSocket拡張のインストール
RUN pecl install ev \
    && docker-php-ext-enable ev

# Apacheの設定
RUN a2enmod headers
RUN a2enmod rewrite

# 作業ディレクトリの設定
WORKDIR /var/www/html

# ポート開放
EXPOSE 80 8765

# WebSocketサーバーを起動するためのエントリーポイントスクリプト
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]