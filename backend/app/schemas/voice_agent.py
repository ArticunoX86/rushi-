import uuid
from pydantic import BaseModel

class VoiceAgentBase(BaseModel):
    name: str
    provider: str = "ElevenLabs"
    voice_id: str = "rachel"
    language: str = "en-US"
    prompt: str
    first_message: str | None = None
    is_active: bool = True
    interruptible: bool = True

class VoiceAgentCreate(VoiceAgentBase):
    pass

class VoiceAgentUpdate(BaseModel):
    name: str | None = None
    provider: str | None = None
    voice_id: str | None = None
    language: str | None = None
    prompt: str | None = None
    first_message: str | None = None
    is_active: bool | None = None
    interruptible: bool | None = None

class VoiceAgentResponse(VoiceAgentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
