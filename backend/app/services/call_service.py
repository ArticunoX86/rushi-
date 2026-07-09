from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.crud.call import (
    create_call,
    get_call_by_id,
    get_calls_by_lead,
    get_all_calls,
    update_call,
    delete_call,
)

from app.schemas.call import (
    CallCreate,
    CallUpdate,
)

from app.models.enums import (
    CallStatus,
)


# ==================================================
# START AI CALL SESSION
# ==================================================

def start_call(
    db: Session,
    call_data: CallCreate,
):

    call = create_call(
        db,
        call_data,
    )


    call.status = CallStatus.IN_PROGRESS

    call.start_time = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(call)


    return call



# ==================================================
# GET SINGLE CALL
# ==================================================

def get_call(
    db: Session,
    call_id: UUID,
):

    return get_call_by_id(
        db,
        call_id,
    )



# ==================================================
# GET CUSTOMER CALL HISTORY
# ==================================================

def get_lead_calls(
    db: Session,
    lead_id: UUID,
):

    return get_calls_by_lead(
        db,
        lead_id,
    )



# ==================================================
# GET ALL CALLS
# ==================================================

def list_calls(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):

    return get_all_calls(
        db,
        skip,
        limit,
    )



# ==================================================
# END AI CALL SESSION
# ==================================================

def finish_call(
    db: Session,
    call_id: UUID,
    call_update: CallUpdate,
):

    call = get_call_by_id(
        db,
        call_id,
    )


    if not call:

        return None


    call_update.status = CallStatus.COMPLETED

    call_update.end_time = datetime.now(
        timezone.utc
    )


    return update_call(
        db,
        call_id,
        call_update,
    )



# ==================================================
# REMOVE CALL
# ==================================================

def remove_call(
    db: Session,
    call_id: UUID,
):

    return delete_call(
        db,
        call_id,
    )