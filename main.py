import uvicorn
from app.main import app

if __name__ == "__main__":
    # Spring Boot의 내장 Tomcat 실행과 유사합니다.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
