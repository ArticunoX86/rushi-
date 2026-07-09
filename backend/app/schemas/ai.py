import uuid

from pydantic import BaseModel



class AIChatRequest(BaseModel):

    lead_id: uuid.UUID

    call_id: uuid.UUID

    message: str



class AIChatResponse(BaseModel):

    reply: str

    detected_city: str | None = None

    detected_budget: int | None = None

    detected_bedrooms: int | None = None