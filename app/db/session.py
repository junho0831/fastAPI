from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB 파일 경로 (Spring의 spring.datasource.url)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 커넥션 풀 생성 (Spring의 DataSource)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True  # 학습용: 실행되는 SQL을 로그에 출력
)

# 세션 팩토리 생성 (Spring의 EntityManagerFactory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Entity의 기본 클래스 (JPA의 최상위 클래스 개념)
Base = declarative_base()

# DB 세션 의존성 주입용 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
