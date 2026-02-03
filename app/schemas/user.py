from pydantic import BaseModel
from typing import Optional, List
from app.schemas.item import Item

# User DTO (Data Transfer Object)
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    items: List[Item] = [] # 연관된 Item 목록 포함 (Lazy Loading 테스트용)

    class Config:
        from_attributes = True  # Spring의 BeanUtils.copyProperties와 유사하게 ORM 객체 매핑 지원
