from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.salesforce_service import salesforce_service

router = APIRouter(
    prefix="/salesforce",
    tags=["Salesforce Integration"],
)

# ==================================================
# SALESFORCE INTEGRATION STATUS
# ==================================================

@router.get("/status")
def get_salesforce_status():
    """
    Check if Salesforce API credentials are set and active.
    """
    has_creds = all([
        salesforce_service.client_id,
        salesforce_service.client_secret,
        salesforce_service.username,
        salesforce_service.password
    ])
    
    return {
        "connected": has_creds,
        "credentials_configured": has_creds,
        "integration_mode": "Salesforce REST API (Production)" if has_creds else "Salesforce Developer Sandbox (Simulated)",
        "instance_url": salesforce_service.instance_url or "https://login.salesforce.com",
        "api_version": "v60.0",
        "sync_objects": ["Lead"]
    }

# ==================================================
# TRIGGER LEAD SYNCHRONIZATION
# ==================================================

@router.post("/sync")
def trigger_salesforce_sync(db: Session = Depends(get_db)):
    """
    Manually trigger leads sync from Salesforce into PostgreSQL leads table.
    """
    try:
        result = salesforce_service.sync_leads_to_db(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Salesforce sync failed: {str(e)}")
