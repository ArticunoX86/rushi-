from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import (
    TokenResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    MessageResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.
    OAuth2 expects 'username' and 'password' as form fields.
    We use the username field to send the user's email.
    """

    data = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    try:
        return AuthService.login(db, data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )





@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_logged_in_user(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """
    return current_user