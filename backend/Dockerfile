FROM python:3.11-slim

WORKDIR /app

# 依存パッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY backend/ .

# 実行時の設定
EXPOSE 8000

# ヘルスチェック。だが上手くワークしない。
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#     CMD curl -f http://localhost:8000/api/healthz || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]