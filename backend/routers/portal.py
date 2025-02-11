from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from datetime import datetime
from urllib.parse import unquote
from core.config import settings

router = APIRouter()

@router.get("/healthz")
async def healthz():
    return {"message": "OK"}

@router.get("/redirect/{site_name}")
async def redirect_with_logging(
    site_name: str,
    url: str = Query(..., description="The URL to redirect to"),
    session_id: str = Query(..., description="Streamlit Session ID")
):
    try:
        # URLデコード
        decoded_url = unquote(url)
        decoded_site_name = unquote(site_name)
        
        try:
            # DynamoDBにクリックログを記録
            dynamodb = settings.dynamodb_client
            table = dynamodb.Table(settings.DYNAMODB_TABLE)
            # コンテナの環境変数TZがAsia/Tokyoに設定されているので、datetime.now()は自動的にJSTを返す
            item = {
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'site_name': decoded_site_name,
                'url': decoded_url
            }
            response = table.put_item(Item=item)            
        except Exception as db_error:
            print(f"DynamoDB error: {str(db_error)}")
                    
        # 指定されたURLにリダイレクト（DynamoDBのエラーがあってもリダイレクトは続行）
        return RedirectResponse(url=decoded_url)
    except Exception as e:
        return {"status": "error", "message": str(e)}