import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base

class AppLog(Base):
    """
    Application Logs Model
    """

    __tablename__ = "app_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    device_identifier: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    log_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        return f"<AppLog {self.log_level} - {self.device_identifier}>"
