from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.crud.campaign import campaign as crud_campaign
from app.schemas.campaign import CampaignResponse, CampaignCreate, CampaignUpdate
from app.models.lead import Lead
from typing import List
import csv
import codecs

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)

@router.get("", response_model=List[CampaignResponse])
def get_campaigns(db: Session = Depends(get_db)):
    return crud_campaign.get_all(db)

@router.post("", response_model=CampaignResponse)
def create_campaign(campaign_in: CampaignCreate, db: Session = Depends(get_db)):
    return crud_campaign.create(db, obj_in=campaign_in)

@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: UUID, campaign_in: CampaignUpdate, db: Session = Depends(get_db)):
    campaign_obj = crud_campaign.get(db, campaign_id=campaign_id)
    if not campaign_obj:
        return {"error": "Campaign not found"}
    return crud_campaign.update(db, db_obj=campaign_obj, obj_in=campaign_in)

@router.post("/{campaign_id}/upload-leads")
def upload_campaign_leads(campaign_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    campaign_obj = crud_campaign.get(db, campaign_id=campaign_id)
    if not campaign_obj:
        return {"error": "Campaign not found"}
        
    # Read CSV
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    count = 0
    for row in csvReader:
        # Assuming CSV has first_name, last_name, phone, email
        first_name = row.get('first_name', 'Unknown')
        last_name = row.get('last_name', '')
        phone = row.get('phone', '')
        email = row.get('email', '')
        
        if phone:
            lead = Lead(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                campaign_id=campaign_obj.id,
                source="MANUAL" # or maybe "BULK_UPLOAD"
            )
            db.add(lead)
            count += 1
            
    campaign_obj.total_leads += count
    db.commit()
    
    return {"status": "success", "leads_imported": count}
