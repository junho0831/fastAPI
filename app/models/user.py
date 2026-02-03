from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"  # @Table(name="users")

    id = Column(Integer, primary_key=True, index=True) # @Id @GeneratedValue
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # 퀴즈 2번 학습용: 1:N 관계 설정 (Lazy Loading)
    items = relationship("Item", back_populates="owner", lazy="select")
