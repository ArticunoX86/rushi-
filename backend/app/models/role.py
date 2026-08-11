import uuid
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.database.base import Base
from app.database.base_model import TimestampMixin

class Role(Base, TimestampMixin):
    """
    Role model for dynamic Role-Based Access Control (RBAC).
    """

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    permissions: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(name='{self.name}')>"
