from uuid import UUID
import uuid

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.crud.lead import get_lead

from app.services.tata_telephony_service import tata_telephony_service

from app.models.call import Call

from app.models.enums import (
    CallDirection,
    CallStatus,
)


# ==================================================
# START AI CALL
# ==================================================

async def start_ai_call(

    db: Session,

    lead_id: UUID,

):


    # ==================================================
    # GET CUSTOMER
    # ==================================================

    lead = get_lead(

        db,

        lead_id,

    )


    if not lead:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Lead not found",

        )


    # ==================================================
    # CREATE CALL SESSION
    # ==================================================

    import uuid
    from app.models.enums import CallDirection, CallStatus
    from app.models.call import Call

    call = Call(
        id=uuid.uuid4(),
        lead_id=lead.id,
        direction=CallDirection.OUTBOUND,
        status=CallStatus.SCHEDULED,
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    # ==================================================
    # FORWARD CALL TO FLUTTER APPLICATION
    # ==================================================

    from app.services.device_connection_manager import device_manager
    import asyncio

    asyncio.create_task(device_manager.broadcast_all({
        "action": "CALL_ASSIGNED",
        "payload": {
            "call_id": str(call.id),
            "customer_name": f"{lead.first_name} {lead.last_name or ''}".strip(),
            "phone_number": lead.phone,
            "status": call.status,
            "priority": lead.priority,
            "script_name": "AI Qualification",
            "created_at": call.created_at.isoformat()
        }
    }))

    # ==================================================
    # RETURN RESULT
    # ==================================================

    return {
        "message": "Call forwarded to mobile application for dispatch",
        "call_id": call.id,
    }