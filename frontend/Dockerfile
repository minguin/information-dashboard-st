FROM python:3.11-slim

WORKDIR /app

# 依存パッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY frontend/ .

# 実行時の設定
EXPOSE 8501

# ヘルスチェック。だが上手くワークしない。
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#     CMD curl -f http://localhost:8501/healthz || exit 1

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
