import uuid
from sqlalchemy import ForeignKey
from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.base_model import TimestampMixin

from app.models.enums import (
    PropertyType,
    LeadStatus,
    LeadPriority,
    LeadSource,
)


class Lead(Base, TimestampMixin):
    """
    Customer Lead Model
    """

    __tablename__ = "leads"
    tenant_id = mapped_column(ForeignKey('tenants.id'), nullable=True)


    # ==================================================
    # Customer Information
    # ==================================================

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )


    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )


    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )


    # ==================================================
    # Property Requirement
    # ==================================================

    preferred_city: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
        nullable=True,
    )


    preferred_locality: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )


    budget_min: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )


    budget_max: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )


    bedrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )


    property_type: Mapped[PropertyType | None] = mapped_column(
        Enum(PropertyType),
        nullable=True,
    )


    # ==================================================
    # Lead Management
    # ==================================================

    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus),
        default=LeadStatus.NEW,
        nullable=False,
    )


    priority: Mapped[LeadPriority] = mapped_column(
        Enum(LeadPriority),
        default=LeadPriority.MEDIUM,
        nullable=False,
    )


    source: Mapped[LeadSource] = mapped_column(
        Enum(LeadSource),
        default=LeadSource.MANUAL,
        nullable=False,
    )


    # ==================================================
    # AI Calling Information
    # ==================================================

    call_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )


    last_call_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    next_followup_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    conversation_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    # ==================================================
    # Assignment
    # ==================================================

    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )


    assigned_user = relationship(
        "User",
        backref="leads",
    )


    # ==================================================
    # AI Call Relationship
    # ==================================================

    calls = relationship(
        "Call",
        back_populates="lead",
        cascade="all, delete-orphan",
    )


    def __repr__(self):

        return f"<Lead {self.first_name} {self.phone}>"