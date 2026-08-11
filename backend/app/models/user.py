import datetime

import uuid
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.base_model import TimestampMixin


class User(Base, TimestampMixin):
    """
    User model for employees of the Real Estate AI Calling Platform.
    """

    __tablename__ = "users"
    tenant_id = mapped_column(ForeignKey('tenants.id'), nullable=True)

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    role = relationship("Role", back_populates="users")

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superadmin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    otp_code: Mapped[str | None] = mapped_column(
        String(6),
        nullable=True,
    )

    otp_expires_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<User("
            f"email='{self.email}', "
            f"role_id='{self.role_id}', "
            f"active={self.is_active})>"
        )