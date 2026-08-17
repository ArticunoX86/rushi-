from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.database.base_model import TimestampMixin
import uuid

class Campaign(Base, TimestampMixin):
    __tablename__ = "campaigns"

    name = Column(String, nullable=False)
    status = Column(String, default="draft") # draft, active, paused, completed
    total_leads = Column(Integer, default=0)
    calls_completed = Column(Integer, default=0)
    voice_agent_id = Column(UUID(as_uuid=True), ForeignKey("voice_agents.id"), nullable=True)

    voice_agent = relationship("VoiceAgent")
    # relationships to leads and calls could be added, but keeping it simple for now
