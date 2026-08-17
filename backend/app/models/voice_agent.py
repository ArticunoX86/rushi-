import uuid
from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base
from app.database.base_model import TimestampMixin

class VoiceAgent(Base, TimestampMixin):
    __tablename__ = "voice_agents"

    name = Column(String, nullable=False)
    provider = Column(String, default="ElevenLabs")
    voice_id = Column(String, default="rachel")
    language = Column(String, default="en-US")
    prompt = Column(Text, nullable=False)
    first_message = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    interruptible = Column(Boolean, default=True)
