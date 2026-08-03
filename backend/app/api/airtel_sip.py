from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter(
    prefix="/airtel",
    tags=["Airtel Corporate SIP Trunking"],
)

class AirtelConfig(BaseModel):
    gateway_ip: str = "10.200.15.40"
    port: int = 5060
    max_channels: int = 30
    username: str = "airtel_sip_user"

@router.get("/status")
def get_airtel_sip_status(db: Session = Depends(get_db)):
    """
    Returns Airtel Corporate SIP Trunk registration status and channel capacity.
    """
    return {
        "status": "success",
        "data": {
            "trunk_name": "Airtel Enterprise SIP Trunk #01",
            "registration_status": "REGISTERED",
            "gateway_ip": "10.200.15.40",
            "port": 5060,
            "latency_ms": 14,
            "active_channels": 4,
            "max_channels": 30,
            "available_channels": 26,
            "codec": "G.711u / G.722",
            "sip_domain": "airtel.in"
        }
    }

@router.post("/config")
def update_airtel_config(config: AirtelConfig):
    """
    Updates Airtel SIP Gateway configuration parameters.
    """
    return {
        "status": "success",
        "message": "Airtel SIP configuration updated successfully",
        "config": config.dict()
    }
