# Information Dashboard
## ローカル環境での実行
### Docker環境での実行
1. プロジェクトディレクトリに移動:
```bash
cd information-dashboard-st
```

2. Docker Composeでサービスを起動:
```bash
docker-compose up --build
```
### 直接実行
1. 依存パッケージのインストール:
```bash
cd information-dashboard-st
pip install -r requirements.txt
```

2. バックエンドサーバーの起動:
```bash
python information-dashboard-st/backend/main.py
```

3. フロントエンドの起動（新しいターミナルで）:
```bash
streamlit run information-dashboard-st/frontend/app.py
```

## ECS on Fargateへのデプロイ
### 自動デプロイ（推奨）
提供されているデプロイスクリプトを使用して、ECRへのイメージのビルドとプッシュを自動化できます：
```bash
# スクリプトに実行権限を付与
chmod +x deploy.sh

# デプロイの実行
./deploy.sh
```

スクリプトは以下の処理を自動的に行います：
- AWS Account IDの取得
- ECRリポジトリの作成
- Dockerイメージのビルドとタグ付け
- ECRへのプッシュ

カスタマイズ可能な環境変数：
- AWS_REGION: AWSリージョン（デフォルト: ap-northeast-1）

### 手動デプロイ
1. AWS Account IDの取得
```bash
# AWS Account IDを環境変数に設定
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
# 確認
echo $AWS_ACCOUNT_ID
```
2. ECRリポジトリの作成
```bash
# アプリケーション用のリポジトリを作成
aws ecr create-repository \
    --repository-name information-dashboard \
    --image-scanning-configuration scanOnPush=true
```
3. ECRへのログイン:
```bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com
```
4. イメージのビルドとタグ付け:
```bash
# docker-composeでイメージをビルド
docker-compose build
# タグ付け（docker-composeのサービス名に基づく）
docker tag information-dashboard-st-backend ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/information-dashboard:backend
docker tag information-dashboard-st-frontend ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/information-dashboard:frontend
```
5. ECRへのプッシュ:
```bash
# 両方のイメージをプッシュ
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/information-dashboard:backend
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/information-dashboard:frontend
```
### ターゲットグループの設定
- フロントエンドとバックエンドの二つ作成する
  - フロントエンド：IPアドレス、portは8501、ヘルスチェックは/healthz
  - バックエンド：IPアドレス、portは8000、ヘルスチェックは/api/healthz
### ロードバランサーの作成
- インターネット向け、リスナーはfrontendでportは80でいったんOK
- リスナールールを追加していく形。バックエンドはパスで/api/*を設定、優先度高くする。defaultは特に変更せずでOK
### ECSの設定
1. タスク実行ロールの作成
- AmazonECSTaskExecutionRolePolicy
- DynamoDBへのアクセス権限

2. タスク定義の作成
- コンテナ定義にECRイメージを指定。二つ作る
  - バックエンド: information-dashboard:backend
  - フロントエンド: information-dashboard:frontend
  - オペレーティングシステム/アーキテクチャは注意。ローカルでのDocker buildした環境とOSの違いがあると動かないケースも。合わせること。
- コンテナポート
  - port 80、8501、8000を適宜追加。port80はフロントエンドだけで良いかも？バックエンドで書かなくても動くことは確認済み
- 環境変数の設定
  - TZ=Asia/Tokyo
  - BACKEND_URL=https://your-alb-dns-name（フロントエンドのみ）
- タスク実行ロールの指定

3. ECSサービスの作成
- フロントエンドとバックエンドで二つ作る
- Application Load Balancerの設定。コンテナポートはそれぞれ8501と8000、、で良いはず。

## 環境変数
以下の環境変数でカスタマイズ可能です：

### バックエンド
- AWS_REGION: AWSリージョン（デフォルト: ap-northeast-1）
- AWS_PROFILE: AWSプロファイル名（デフォルト: default）
- TZ: タイムゾーン（デフォルト: Asia/Tokyo）

### フロントエンド
- TZ: タイムゾーン（デフォルト: Asia/Tokyo）

## DynamoDBテーブルの設定

テーブル設定:
- テーブル名: portal_clicks
- パーティションキー: timestamp (String)
- ソートキー: session_id (String)

### データ形式
```json
{
  "timestamp": "2025-02-11T14:30:00",  // JST (Asia/Tokyo)
  "session_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "site_name": "サイト名",
  "url": "https://example.com"
}
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
- コンテナ化: Docker, Docker Compose
- デプロイ: Amazon ECS on Fargate