import boto3
from typing import Optional, List

class Settings:
    # プロジェクト情報
    PROJECT_NAME: str = "Information Dashboard"
    VERSION: str = "1.0.0"

    # API サーバー設定
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # AWS 設定
    AWS_REGION: str = "ap-northeast-1"
    AWS_PROFILE: str = "default"
    DYNAMODB_TABLE: str = "portal_clicks"

    # 環境設定
    DEBUG: bool = True  # 開発時は True, 本番では False にする

    # CORS 設定（開発環境ではすべて許可、本番では特定ドメインのみ）
    ALLOW_ORIGINS: List[str] = ["*"] if DEBUG else ["https://example.com"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

    @property
    def dynamodb_client(self) -> Optional[boto3.resource]:
        """DynamoDB クライアントを取得"""
        try:
            session = boto3.Session(
                profile_name=self.AWS_PROFILE,
                region_name=self.AWS_REGION
            )
            return session.resource('dynamodb')
        except Exception as e:
            print(f"Failed to initialize DynamoDB client: {e}")
            return None

settings = Settings()
