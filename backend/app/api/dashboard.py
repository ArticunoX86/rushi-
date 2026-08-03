from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database.session import get_db
from app.models.call import Call
from app.models.lead import Lead
from app.models.device import Device
from app.models.enums import CallStatus, DeviceStatus

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard & Metrics"],
)

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Returns real-time dashboard analytics and performance metrics.
    """
    today_start = datetime.combine(date.today(), datetime.min.time())

    # Calls today
    calls_today_count = db.query(Call).filter(Call.created_at >= today_start).count()
    
    # Active calls
    active_calls_count = db.query(Call).filter(
        Call.status.in_([CallStatus.SCHEDULED, CallStatus.IN_PROGRESS])
    ).count()

    # Completed calls today
    completed_calls_today = db.query(Call).filter(
        Call.created_at >= today_start,
        Call.status == CallStatus.COMPLETED
    ).count()

    # Total call duration today
    calls_today = db.query(Call).filter(Call.created_at >= today_start).all()
    total_seconds = sum((c.duration_seconds or 0) for c in calls_today)
    
    avg_seconds = (total_seconds // max(1, len(calls_today))) if calls_today else 0
    avg_minutes_str = f"{avg_seconds // 60:02d}:{avg_seconds % 60:02d}"

    # Total leads & Devices
    total_leads = db.query(Lead).count()
    online_devices = db.query(Device).filter(Device.status == DeviceStatus.ONLINE).count()

    # Conversion Rate calculation
    total_calls_all = db.query(Call).count()
    total_completed_all = db.query(Call).filter(Call.status == CallStatus.COMPLETED).count()
    conversion_rate = round((total_completed_all / max(1, total_calls_all)) * 100, 1)

    return {
        "status": "success",
        "data": {
            "calls_today": calls_today_count,
            "active_calls": active_calls_count,
            "completed_calls": completed_calls_today,
            "avg_duration": avg_minutes_str,
            "total_duration_seconds": total_seconds,
            "total_leads": total_leads,
            "online_devices": online_devices,
            "conversion_rate_pct": conversion_rate,
            "ai_agents_active": 1,
        }
    }
