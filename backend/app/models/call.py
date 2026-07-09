import uuid

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    ForeignKey,
    Text,
    Enum,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base
from app.database.base_model import TimestampMixin

from app.models.enums import (
    CallStatus,
    CallDirection,
    CallOutcome,
)


class Call(Base, TimestampMixin):
    """
    AI Voice Call Session Model
    """

    __tablename__ = "calls"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id"),
        nullable=False,
    )


    direction: Mapped[CallDirection] = mapped_column(
        Enum(CallDirection),
        default=CallDirection.OUTBOUND,
    )


    status: Mapped[CallStatus] = mapped_column(
        Enum(CallStatus),
        default=CallStatus.SCHEDULED,
    )


    start_time = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    end_time = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )


    recording_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )


    transcript: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    outcome: Mapped[CallOutcome | None] = mapped_column(
        Enum(CallOutcome),
        nullable=True,
    )


    lead = relationship(
        "Lead",
        back_populates="calls",
    )

    conversations = relationship(
    "Conversation",
    back_populates="call",
    cascade="all, delete-orphan",
    )