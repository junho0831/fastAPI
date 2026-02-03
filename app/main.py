from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.api import study_labs
from app.db.session import engine, Base

# 앱 시작 시 DB 테이블 생성 (Spring의 ddl-auto: update 효과)
Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    # 학습용 랩 라우터 등록
    app.include_router(study_labs.router, prefix="/study", tags=["Study Labs"])

    return app

app = create_app()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI with Spring-like Architecture & DB Support"}