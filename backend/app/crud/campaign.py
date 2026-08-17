import uuid
from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate

class CRUDCampaign:
    def get(self, db: Session, campaign_id: uuid.UUID):
        return db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Campaign).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CampaignCreate):
        db_obj = Campaign(
            name=obj_in.name,
            status=obj_in.status,
            voice_agent_id=obj_in.voice_agent_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Campaign, obj_in: CampaignUpdate):
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, campaign_id: uuid.UUID):
        obj = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

campaign = CRUDCampaign()
