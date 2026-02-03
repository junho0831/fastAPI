from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService, get_user_service

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    try:
        return service.create_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100,
    service: UserService = Depends(get_user_service)
):
    return service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user