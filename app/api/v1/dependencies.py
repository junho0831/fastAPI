from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.user_service import UserService


@dataclass
class UserControllerDeps:
    user_service: UserService


def get_user_controller_deps(db: Session = Depends(get_db)) -> UserControllerDeps:
    # 여러 의존성을 한 곳에서 조합해 엔드포인트 시그니처를 단순화합니다.
    return UserControllerDeps(user_service=UserService(db))
