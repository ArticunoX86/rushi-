import uuid
from sqlalchemy.orm import Session
from app.models.voice_agent import VoiceAgent
from app.schemas.voice_agent import VoiceAgentCreate, VoiceAgentUpdate

class CRUDVoiceAgent:
    def get(self, db: Session, agent_id: uuid.UUID):
        return db.query(VoiceAgent).filter(VoiceAgent.id == agent_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(VoiceAgent).offset(skip).limit(limit).all()
        
    def get_active(self, db: Session):
        return db.query(VoiceAgent).filter(VoiceAgent.is_active == True).all()

    def create(self, db: Session, obj_in: VoiceAgentCreate):
        db_obj = VoiceAgent(
            name=obj_in.name,
            provider=obj_in.provider,
            voice_id=obj_in.voice_id,
            language=obj_in.language,
            prompt=obj_in.prompt,
            is_active=obj_in.is_active,
            interruptible=obj_in.interruptible
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: VoiceAgent, obj_in: VoiceAgentUpdate):
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, agent_id: uuid.UUID):
        obj = db.query(VoiceAgent).filter(VoiceAgent.id == agent_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

voice_agent = CRUDVoiceAgent()
