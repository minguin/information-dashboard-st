from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import portal

def create_app():
    """FastAPI アプリを作成"""
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )

    # ルーターの登録
    app.include_router(portal.router, prefix="/api", tags=["portal"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,  # 開発時は reload=True, 本番では False
    )
