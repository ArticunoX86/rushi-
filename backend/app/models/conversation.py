import uuid
from sqlalchemy import ForeignKey

from sqlalchemy import (
    Text,
    Enum,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base

from app.database.base_model import TimestampMixin

from app.models.enums import (
    MessageSender,
    MessageIntent,
)



class Conversation(
    Base,
    TimestampMixin
):

    """
    Stores AI and Customer messages
    """

    __tablename__ = "conversations"
    tenant_id = mapped_column(ForeignKey('tenants.id'), nullable=True)



    id: Mapped[uuid.UUID] = mapped_column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4,

    )



    call_id: Mapped[uuid.UUID] = mapped_column(

        UUID(as_uuid=True),

        ForeignKey(
            "calls.id"
        ),

        nullable=False,

    )



    sender: Mapped[MessageSender] = mapped_column(

        Enum(MessageSender),

        nullable=False,

    )



    message: Mapped[str] = mapped_column(

        Text,

        nullable=False,

    )



    intent: Mapped[MessageIntent] = mapped_column(

        Enum(MessageIntent),

        default=MessageIntent.UNKNOWN,

    )



    call = relationship(

        "Call",

        back_populates="conversations",

    )



    def __repr__(self):

        return f"<Conversation {self.sender}>"