from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_phone,
    update_last_login,
)
from app.models.user import User
from app.models.role import Role
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)
from app.core.logger import logger


class AuthService:
    """
    Authentication business logic.
    """


    @staticmethod
    def login(db: Session, data: LoginRequest) -> LoginResponse:
        """
        Authenticate a user.
        """

        user = get_user_by_email(db, data.email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password.")

        if not user.is_active:
            raise ValueError("User account is inactive.")

        if user.role.name != "System Administrator" and "application_access" not in user.role.permissions:
            raise ValueError("Access denied. You do not have permission to access the application.")

        token = create_access_token(
            subject=str(user.id),
        )

        update_last_login(db, user)

        return LoginResponse(
            access_token=token,
            token_type="bearer",
        )