from uuid import UUID
import uuid

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.crud.lead import get_lead

from app.services.device_service import (
    find_available_calling_device,
)

from app.services.device_connection_manager import (
    device_manager,
)

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
    # FIND AVAILABLE DEVICE
    # ==================================================

    device = find_available_calling_device(

        db,

        active_identifiers=list(device_manager.active_devices.keys())

    )


    # ==================================================
    # CREATE CALL SESSION
    # ==================================================

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
    # SEND COMMAND TO ANDROID
    # ==================================================

    success = await device_manager.send_command(

        device.device_identifier,

        {

            "action": "CALL",

            "call_id": str(call.id),

            "lead_id": str(lead.id),

            "customer_name": f"{lead.first_name} {lead.last_name}",

            "phone": lead.phone,

        },

    )


    if not success:

        raise HTTPException(

            status_code=500,

            detail="Android device is offline",

        )


    # ==================================================
    # RETURN RESULT
    # ==================================================

    return {

        "message": "Call command sent successfully",

        "device": device.device_name,

        "call_id": call.id,

    }