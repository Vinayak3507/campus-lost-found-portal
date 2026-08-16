""""Purpose:
Define authentication API endpoints.

**Responsibilities:
Handle requests for:
POST /register
POST /login

---> The route calls the auth service."""

from fastapi import APIRouter, HTTPException, status, Depends
from app.schema.auth_schema import (UserRegisterRequest,UserRegisterResponse,UserLoginRequest,
UserUpdateRequest,UserResponse,UserLoginResponse,)
from app.repositories.auth_repository import get_user_by_id
from app.dependencies.roles import require_admin
from app.services.auth_service import AuthService
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

@router.put("/update_me",response_model=UserResponse,)
def update_me(user_data: UserUpdateRequest,current_user: str = Depends(get_current_user),):
    try:
        return AuthService.update_user(current_user["id"],user_data)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e),)

@router.get("/admin-test")
def admin_test(current_user: dict = Depends(require_admin)):
    return {"message": "Welcome Admin!","user_id": current_user["id"],"role": current_user["role"],}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: str = Depends(get_current_user)):
    user = get_user_by_id(current_user)
    if not user:
        raise HTTPException(status_code=404,detail="User not found.")
    return user