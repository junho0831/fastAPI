from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends

from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.db.session import get_db

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> UserResponse:
        # 이미 존재하는지 체크
        if self.repository.get_by_email(user_in.email):
            raise ValueError("Email already registered")
        
        return self.repository.create(user_in)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        return self.repository.get_by_id(user_id)

# Service를 의존성으로 주입받기 위한 팩토리 함수 (Spring의 Bean 주입과 유사)
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)