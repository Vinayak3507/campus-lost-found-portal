""""Purpose:
Define authentication API endpoints.

**Responsibilities:
Handle requests for:
POST /register
POST /login

---> The route calls the auth service."""

from fastapi import APIRouter, HTTPException, status, Depends
from app.schema.auth_schema import (UserRegisterRequest,UserRegisterResponse,UserLoginRequest,
UserResponse,UserLoginResponse)
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth",tags=["Authentication"],)

@router.post("/register",response_model=UserRegisterResponse,status_code=status.HTTP_201_CREATED,)
def register(user: UserRegisterRequest):
    try:
        return AuthService.register_user(user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e),)


@router.post("/login",response_model=UserLoginResponse,status_code=status.HTTP_200_OK,)
def login(user: UserLoginRequest):
    try:
        return AuthService.login_user(user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e),)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: str = Depends(get_current_user)):
    user = get_user_by_id(current_user)
    if not user:
        raise HTTPException(status_code=404,detail="User not found.")

    return user