import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.item import Item
from app.schemas.user import UserResponse

router = APIRouter()

# --- Lab 0: 데이터 준비 ---
@router.post("/setup")
def setup_data(db: Session = Depends(get_db)):
    """실습용 데이터 생성 (User 1명 + Item 5개)"""
    if db.query(User).filter(User.email == "test@example.com").first():
        return {"message": "이미 데이터가 존재합니다."}
        
    user = User(email="test@example.com", password="pw", full_name="Tester")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    items = [Item(title=f"Item {i}", owner_id=user.id) for i in range(5)]
    db.add_all(items)
    db.commit()
    return {"message": "데이터 생성 완료 (User ID: 1, Items: 5개)"}


# --- Lab 1: DI Scope (Quiz 1) ---
class MyService:
    def __init__(self):
        # 이 로그가 언제, 몇 번 찍히는지 확인하세요.
        print(f"✅ MyService 인스턴스 생성됨! (Time: {time.time()})")

@router.get("/lab1/scope")
def lab1_scope_test(service: MyService = Depends(MyService)):
    """
    Spring의 @Service(Singleton)와 달리, 
    FastAPI의 Depends는 요청마다 인스턴스를 생성하는지 테스트합니다.
    """
    return {"message": "Check your console logs!"}


# --- Lab 2: Lazy Loading & N+1 (Quiz 2) ---
@router.get("/lab2/lazy-loading/{user_id}", response_model=UserResponse)
def lab2_lazy_test(user_id: int, db: Session = Depends(get_db)):
    """
    Pydantic 모델(UserResponse)에 'items' 필드가 포함되어 있습니다.
    SQLAlchemy는 'lazy=select'이므로, items에 접근할 때 추가 쿼리가 발생하는지 확인하세요.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 여기서 return 되는 시점에 Pydantic이 user.items를 읽으려 시도합니다.
    return user


# --- Lab 3: Async Blocking (Quiz 3) ---
@router.get("/lab3/sync-sleep")
def lab3_sync_sleep():
    """
    일반 def 함수에서 time.sleep(5) 실행.
    FastAPI는 이를 쓰레드풀에서 실행하므로 서버가 멈추지 않습니다.
    """
    time.sleep(5)
    return {"message": "Sync sleep finished"}

@router.get("/lab3/async-sleep-blocking")
async def lab3_async_sleep_blocking():
    """
    async def 함수에서 동기식 time.sleep(5) 실행.
    이벤트 루프를 차단(Block)하여 다른 요청까지 멈추게 만드는지 확인하세요.
    """
    time.sleep(5) 
    return {"message": "Async Blocking sleep finished (Dangerous!)"}
