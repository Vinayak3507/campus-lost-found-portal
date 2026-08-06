""""Purpose:
Define authentication API endpoints.

**Responsibilities:
Handle requests for:
POST /register
POST /login

---> The route calls the auth service."""

from fastapi import APIRouter, HTTPException, status
from app.schema.auth_schema import (UserRegisterRequest,UserRegisterResponse,)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth",tags=["Authentication"],)

@router.post("/register",response_model=UserRegisterResponse,status_code=status.HTTP_201_CREATED,)
def register(user: UserRegisterRequest):

    try:
        return AuthService.register_user(user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e),)