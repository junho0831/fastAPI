from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user: UserCreate) -> User:
        # Entity 생성 (Builder 패턴 대신 생성자 사용)
        db_user = User(
            email=user.email,
            password=user.password, # 실제로는 해싱해야 함
            full_name=user.full_name,
            is_active=True
        )
        self.db.add(db_user)   # persist
        self.db.commit()       # transaction commit
        self.db.refresh(db_user) # ID 등 DB 생성 값 갱신
        return db_user
