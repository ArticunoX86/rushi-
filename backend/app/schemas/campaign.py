import uuid
from pydantic import BaseModel

class CampaignBase(BaseModel):
    name: str
    status: str = "draft"
    voice_agent_id: uuid.UUID | None = None

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    voice_agent_id: uuid.UUID | None = None

class CampaignResponse(CampaignBase):
    id: uuid.UUID
    total_leads: int
    calls_completed: int

    class Config:
        from_attributes = True
