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
    # SEND COMMAND TO TATA SMARTFLO
    # ==================================================

    tata_response = tata_telephony_service.make_outbound_call(
        phone_number=lead.phone,
        call_id=str(call.id)
    )

    # ==================================================
    # RETURN RESULT
    # ==================================================

    return {
        "message": "Call initiated via TATA Smartflo",
        "tata_call_id": tata_response["tata_call_id"],
        "call_id": call.id,
    }