from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
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
def get_dashboard_stats(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    """
    Returns real-time dashboard analytics and performance metrics.
    """
    if start_date:
        filter_start = datetime.combine(start_date, datetime.min.time())
    else:
        filter_start = datetime.combine(date.today(), datetime.min.time())
        
    if end_date:
        filter_end = datetime.combine(end_date, datetime.max.time())
    else:
        filter_end = datetime.now()

    # Calls in period
    calls_period_count = db.query(Call).filter(Call.created_at >= filter_start, Call.created_at <= filter_end).count()
    
    # Active calls
    active_calls_query = db.query(Call).filter(
        Call.status.in_([CallStatus.SCHEDULED, CallStatus.IN_PROGRESS])
    )
    active_calls_count = active_calls_query.count()
    active_call = active_calls_query.first()
    active_call_id = str(active_call.id) if active_call else None

    # Completed calls in period
    completed_calls_period = db.query(Call).filter(
        Call.created_at >= filter_start,
        Call.created_at <= filter_end,
        Call.status == CallStatus.COMPLETED
    ).count()

    # Total call duration in period
    calls_period = db.query(Call).filter(Call.created_at >= filter_start, Call.created_at <= filter_end).all()
    total_seconds = sum((c.duration_seconds or 0) for c in calls_period)
    
    avg_seconds = (total_seconds // max(1, len(calls_period))) if calls_period else 0
    avg_minutes_str = f"{avg_seconds // 60:02d}:{avg_seconds % 60:02d}"

    # Total leads & Devices
    total_leads = db.query(Lead).count()
    online_devices = db.query(Device).filter(Device.status == DeviceStatus.ONLINE).count()

    # Conversion Rate calculation
    total_calls_all = db.query(Call).count()
    total_completed_all = db.query(Call).filter(Call.status == CallStatus.COMPLETED).count()
    conversion_rate = round((total_completed_all / max(1, total_calls_all)) * 100, 1)

    from datetime import timedelta
    # Chart Data: Call Volume for Last 7 Days
    today = date.today()
    chart_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        chart_data.append({"name": d.strftime("%a"), "date": d.isoformat(), "calls": 0})
        
    start_7d = datetime.combine(today - timedelta(days=6), datetime.min.time())
    calls_last_7d = db.query(func.date(Call.created_at), func.count(Call.id)).filter(Call.created_at >= start_7d).group_by(func.date(Call.created_at)).all()
    
    call_counts = {d.isoformat() if hasattr(d, 'isoformat') else str(d): count for d, count in calls_last_7d}
    for entry in chart_data:
        entry["calls"] = call_counts.get(entry["date"], 0)

    # Chart Data: Lead Status Breakdown
    lead_status_counts = db.query(Lead.status, func.count(Lead.id)).group_by(Lead.status).all()
    lead_breakdown = [{"name": status.value.title().replace("_", " "), "value": count} for status, count in lead_status_counts]
    if not lead_breakdown:
        # Default placeholder if no leads exist to prevent empty pie chart
        lead_breakdown = [{"name": "No Data", "value": 1}]

    return {
        "status": "success",
        "data": {
            "calls_today": calls_period_count,
            "active_calls": active_calls_count,
            "active_call_id": active_call_id,
            "completed_calls": completed_calls_period,
            "avg_duration": avg_minutes_str,
            "total_duration_seconds": total_seconds,
            "total_leads": total_leads,
            "online_devices": online_devices,
            "conversion_rate_pct": conversion_rate,
            "ai_agents_active": 1,
            "chart_data": chart_data,
            "lead_breakdown": lead_breakdown,
        }
    }
