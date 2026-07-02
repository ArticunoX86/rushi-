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
from app.models.enums import UserRole
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)


class AuthService:
    """
    Authentication business logic.
    """

    @staticmethod
    def register(db: Session, data: RegisterRequest) -> User:
        """
        Register a new user.
        """

        # Check email
        if get_user_by_email(db, data.email):
            raise ValueError("Email already exists.")

        # Check phone
        if get_user_by_phone(db, data.phone):
            raise ValueError("Phone number already exists.")

        # Create user object
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(data.password),
            role=UserRole.SALES_EXECUTIVE,
            is_active=True,
        )

        return create_user(db, user)

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

        token = create_access_token(
            subject=str(user.id),
        )

        update_last_login(db, user)

        return LoginResponse(
            access_token=token,
            token_type="bearer",
        )