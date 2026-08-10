""""Purpose:
Handle authentication business logic.

Responsibilities:
user registration logic
password hashing
password verification
login authentication
token generation

---> This is where actual auth behavior lives."""

import uuid
from app.core.security import (hash_password,verify_password,create_access_token,)
from app.repositories.auth_repository import (create_user,get_user_by_email,get_user_by_student_id,)
from app.schema.auth_schema import (UserRegisterRequest,UserRegisterResponse,UserLoginRequest,UserLoginResponse,)


class AuthService:
    @staticmethod
    def register_user(user: UserRegisterRequest) -> UserRegisterResponse:

        # Check if email already exists
        existing_email = get_user_by_email(user.college_email)
        if existing_email:
            raise ValueError("College email is already registered.")

        # Check if student ID already exists
        existing_student = get_user_by_student_id(user.student_id)
        if existing_student:
            raise ValueError("Student ID is already registered.")

        # Generate UUID
        user_id = str(uuid.uuid4())

        # Hash Password
        password_hash = hash_password(user.password)

        # Prepare Data
        user_data = {
            "id": user_id,
            "student_name": user.student_name,
            "student_id": user.student_id,
            "college_email": user.college_email,
            "password_hash": password_hash,
            "branch": user.branch.value,
            "academic_session": user.academic_session,
            "block": user.block,
            "phone": user.phone,
        }

        # Save User
        create_user(user_data)

        # Response
        return UserRegisterResponse(
            message="User registered successfully.",
            user_id=user_id,
        )

    @staticmethod
    def login_user(user: UserLoginRequest) -> UserLoginResponse:
        existing_user = get_user_by_email(user.college_email)

        if not existing_user:
            raise ValueError("Invalid email or password.")

        password_valid = verify_password(user.password,existing_user["password_hash"])

        if not password_valid:
            raise ValueError("Invalid email or password.")

        access_token = create_access_token({"sub": existing_user["id"]})

        return UserLoginResponse(message="Login successful.",access_token=access_token,token_type="bearer")