import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import (
    CallStatus,
    CallDirection,
    CallOutcome,
)


# =====================================
# BASE SCHEMA
# =====================================

class CallBase(BaseModel):

    lead_id: uuid.UUID

    direction: CallDirection = CallDirection.OUTBOUND



# =====================================
# CREATE CALL
# =====================================

class CallCreate(CallBase):
    pass



# =====================================
# UPDATE CALL
# =====================================

class CallUpdate(BaseModel):

    status: CallStatus | None = None

    end_time: datetime | None = None

    duration_seconds: int | None = None

    recording_url: str | None = None

    transcript: str | None = None

    summary: str | None = None

    outcome: CallOutcome | None = None



# =====================================
# RESPONSE
# =====================================

class CallResponse(CallBase):

    id: uuid.UUID

    status: CallStatus

    start_time: datetime | None

    end_time: datetime | None

    duration_seconds: int

    recording_url: str | None

    transcript: str | None

    summary: str | None

    outcome: CallOutcome | None

    created_at: datetime
    updated_at: datetime | None


    class Config:
        from_attributes = True