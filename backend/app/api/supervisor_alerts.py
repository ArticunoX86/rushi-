"""
Supervisor Alerts API — Human-in-the-loop safety layer.

Provides endpoints for:
- Supervisor takeover of active AI calls
- Viewing guardrail violation alerts
- Real-time sentiment monitoring
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional

from app.core.dependencies import get_db
from app.services.device_connection_manager import device_manager
from app.guardrails.call_timeout_manager import (
    force_end_call,
    get_session_info,
)
from app.guardrails.sentiment_analyzer import (
    get_call_sentiment_trend,
)
from app.guardrails.call_state_machine import (
    get_or_create_state_machine,
)


router = APIRouter(
    prefix="/api/v1/supervisor",
    tags=["Supervisor Safety"],
)


# ==================================================
# IN-MEMORY ALERT STORE
# ==================================================

class GuardrailAlert:
    """Represents a single guardrail violation alert."""
    def __init__(
        self,
        call_id: str,
        alert_type: str,
        message: str,
        severity: str = "WARNING",
    ):
        self.id = f"{call_id}-{datetime.now(timezone.utc).timestamp()}"
        self.call_id = call_id
        self.alert_type = alert_type  # "prompt_injection" | "banned_phrase" | "sentiment_drop" | "timeout" | "takeover"
        self.message = message
        self.severity = severity      # "INFO" | "WARNING" | "CRITICAL"
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.acknowledged = False


# Global alert store (in production, use Redis or DB)
_alerts: list[GuardrailAlert] = []
MAX_ALERTS = 200  # Retain last 200 alerts


def add_alert(
    call_id: str,
    alert_type: str,
    message: str,
    severity: str = "WARNING",
):
    """Add a guardrail alert and broadcast to connected supervisors."""
    alert = GuardrailAlert(
        call_id=call_id,
        alert_type=alert_type,
        message=message,
        severity=severity,
    )
    _alerts.append(alert)

    # Trim old alerts
    if len(_alerts) > MAX_ALERTS:
        _alerts.pop(0)

    # Broadcast to all connected supervisor devices
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(device_manager.broadcast_all({
                "action": "SUPERVISOR_ALERT",
                "event": "SUPERVISOR_ALERT",
                "payload": {
                    "id": alert.id,
                    "call_id": call_id,
                    "alert_type": alert_type,
                    "message": message,
                    "severity": severity,
                    "timestamp": alert.timestamp,
                }
            }))
    except Exception as e:
        print(f"[GUARDRAIL] Failed to broadcast alert: {e}")

    return alert


# ==================================================
# API ENDPOINTS
# ==================================================

class TakeoverRequest(BaseModel):
    reason: Optional[str] = "Manual supervisor takeover"


@router.post("/takeover/{call_id}")
async def supervisor_takeover(
    call_id: str,
    request: TakeoverRequest = TakeoverRequest(),
):
    """
    Force-end the AI session for a call, allowing a human supervisor to take over.

    This will:
    1. Mark the call as forcefully ended in the timeout manager.
    2. Broadcast a SUPERVISOR_TAKEOVER event to the mobile app.
    3. Log the takeover as an alert.
    """

    # Mark call as forcefully ended
    force_end_call(call_id)

    # Log alert
    add_alert(
        call_id=call_id,
        alert_type="takeover",
        message=f"Supervisor takeover initiated: {request.reason}",
        severity="CRITICAL",
    )

    # Broadcast takeover event to Flutter app
    await device_manager.broadcast_all({
        "action": "SUPERVISOR_TAKEOVER",
        "event": "SUPERVISOR_TAKEOVER",
        "payload": {
            "call_id": call_id,
            "reason": request.reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    })

    return {
        "status": "success",
        "message": f"Takeover initiated for call {call_id}",
        "call_id": call_id,
    }


@router.get("/alerts")
async def get_alerts(
    limit: int = 50,
    severity: str = None,
    call_id: str = None,
):
    """
    Get recent guardrail violation alerts.

    Query params:
    - limit: Number of alerts to return (default 50)
    - severity: Filter by severity (INFO, WARNING, CRITICAL)
    - call_id: Filter by specific call
    """
    filtered = _alerts.copy()

    if severity:
        filtered = [a for a in filtered if a.severity == severity.upper()]

    if call_id:
        filtered = [a for a in filtered if a.call_id == call_id]

    # Return most recent first
    filtered.reverse()
    filtered = filtered[:limit]

    return {
        "total": len(filtered),
        "alerts": [
            {
                "id": a.id,
                "call_id": a.call_id,
                "alert_type": a.alert_type,
                "message": a.message,
                "severity": a.severity,
                "timestamp": a.timestamp,
                "acknowledged": a.acknowledged,
            }
            for a in filtered
        ],
    }


@router.get("/call-safety/{call_id}")
async def get_call_safety_status(call_id: str):
    """
    Get the full safety status for a specific active call.

    Returns sentiment trend, state machine status, and timeout info.
    """
    sentiment = get_call_sentiment_trend(call_id)
    session_info = get_session_info(call_id)

    try:
        state_machine = get_or_create_state_machine(call_id)
        state_info = state_machine.get_summary()
    except Exception:
        state_info = {"status": "NOT_FOUND"}

    # Get alerts for this call
    call_alerts = [
        {
            "alert_type": a.alert_type,
            "message": a.message,
            "severity": a.severity,
            "timestamp": a.timestamp,
        }
        for a in _alerts if a.call_id == call_id
    ]

    return {
        "call_id": call_id,
        "sentiment": sentiment,
        "session": session_info,
        "state_machine": state_info,
        "alerts": call_alerts[-10:],  # Last 10 alerts for this call
    }


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """Mark an alert as acknowledged by the supervisor."""
    for alert in _alerts:
        if alert.id == alert_id:
            alert.acknowledged = True
            return {"status": "acknowledged", "alert_id": alert_id}

    raise HTTPException(status_code=404, detail="Alert not found")
