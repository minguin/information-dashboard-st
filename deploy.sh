#!/bin/bash

# エラーが発生したら即座に終了
set -e

# AWS Account IDを取得
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: ${AWS_ACCOUNT_ID}"

# リージョンの設定
export AWS_REGION=${AWS_REGION:-"ap-northeast-1"}
echo "AWS Region: ${AWS_REGION}"

# ECRリポジトリの作成（既に存在する場合はスキップ）
echo "Creating ECR repository..."
aws ecr create-repository \
    --repository-name information-dashboard \
    --image-scanning-configuration scanOnPush=true || true

# ECRへのログイン
echo "Logging in to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# イメージのビルド
echo "Building Docker images..."
docker-compose build

# イメージのタグ付け
echo "Tagging images..."
docker tag information-dashboard-st-backend ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/information-dashboard:backend
docker tag information-dashboard-st-frontend ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/information-dashboard:frontend

# イメージのプッシュ
echo "Pushing images to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/information-dashboard:backend
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/information-dashboard:frontend

# イメージのプッシュ
echo "force-new-deployment..."
aws ecs update-service --cluster information-dashboard --service information-dashboard-backend2 --force-new-deployment
aws ecs update-service --cluster information-dashboard --service information-dashboard-frontend2 --force-new-deployment

echo "Deployment completed successfully!"