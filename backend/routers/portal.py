from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from datetime import datetime
from urllib.parse import unquote
from core.config import settings

router = APIRouter()

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
            if dynamodb:
                table = dynamodb.Table(settings.DYNAMODB_TABLE)
                response = table.put_item(
                    Item={
                        'timestamp': datetime.now().isoformat(),
                        'session_id': session_id,
                        'site_name': decoded_site_name,
                        'url': decoded_url
                    }
                )
        except Exception as db_error:
            print(f"DynamoDB error: {str(db_error)}")
            # DynamoDBのエラーがあってもリダイレクトは続行
        
        # 指定されたURLにリダイレクト
        return RedirectResponse(url=decoded_url)
    except Exception as e:
        return {"status": "error", "message": str(e)}