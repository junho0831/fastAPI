from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.dependencies import UserControllerDeps, get_user_controller_deps
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()
UserDeps = Annotated[UserControllerDeps, Depends(get_user_controller_deps)]

@router.post("/", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    deps: UserDeps
):
    try:
        return deps.user_service.create_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserResponse])
def read_users(
    deps: UserDeps,
    skip: int = 0, 
    limit: int = 100
):
    return deps.user_service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    deps: UserDeps
):
    user = deps.user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
