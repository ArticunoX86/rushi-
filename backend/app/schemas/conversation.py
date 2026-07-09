import uuid

from datetime import datetime

from pydantic import BaseModel

from app.models.enums import (
    MessageSender,
    MessageIntent,
)


# ======================================
# BASE
# ======================================

class ConversationBase(BaseModel):

    call_id: uuid.UUID

    sender: MessageSender

    message: str


# ======================================
# CREATE MESSAGE
# ======================================

class ConversationCreate(
    ConversationBase
):
    pass



# ======================================
# UPDATE MESSAGE
# ======================================

class ConversationUpdate(BaseModel):

    message: str | None = None

    intent: MessageIntent | None = None



# ======================================
# RESPONSE
# ======================================

class ConversationResponse(
    ConversationBase
):

    id: uuid.UUID

    intent: MessageIntent

    created_at: datetime

    updated_at: datetime | None


    class Config:

        from_attributes = True