# Information Dashboard

ポータルサイトへのアクセスを追跡・記録するダッシュボードアプリケーション

## プロジェクト構成

```
information-dashboard-st/
  ├── backend/              # FastAPI バックエンド
  │   ├── main.py          # メインエントリーポイント
  │   ├── routers/         # APIルーター
  │   │   └── portal.py    # ポータルサイト関連のエンドポイント
  │   └── core/
  │       └── config.py    # 設定管理
  ├── frontend/            # Streamlit フロントエンド
  │   └── app.py          # ポータルサイト一覧ページ
  └── requirements.txt     # 依存パッケージ
```

## セットアップ

1. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

2. AWS認証情報の設定:
~/.aws/credentials に以下の設定が必要です
```ini
[default]
aws_access_key_id = あなたのアクセスキー
aws_secret_access_key = あなたのシークレットキー
```

3. DynamoDBテーブルの作成:
- テーブル名: portal_clicks
- パーティションキー: timestamp (String)
- ソートキー: session_id (String)

## 実行方法

1. バックエンドサーバーの起動:
```bash
cd backend
python main.py
```

2. フロントエンドの起動（新しいターミナルで）:
```bash
cd frontend
streamlit run app.py
```

## 機能

- ポータルサイト一覧の表示
- クリックイベントの追跡
- DynamoDBへのログ記録
- セッション管理

## 技術スタック

- Frontend: Streamlit
- Backend: FastAPI
- Database: Amazon DynamoDB
- その他: boto3, uvicorn