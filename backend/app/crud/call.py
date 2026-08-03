from uuid import UUID

from sqlalchemy.orm import Session

from app.models.call import Call
from app.schemas.call import (
    CallCreate,
    CallUpdate,
)


# ==========================================
# CREATE CALL SESSION
# ==========================================

def create_call(
    db: Session,
    call_data: CallCreate,
):

    call = Call(
        **call_data.model_dump()
    )


    db.add(call)

    db.commit()

    db.refresh(call)


    return call



# ==========================================
# GET CALL BY ID
# ==========================================

def get_call_by_id(
    db: Session,
    call_id: UUID,
):

    return (
        db.query(Call)
        .filter(Call.id == call_id)
        .first()
    )



# ==========================================
# GET LEAD CALL HISTORY
# ==========================================

def get_calls_by_lead(
    db: Session,
    lead_id: UUID,
):

    return (
        db.query(Call)
        .filter(Call.lead_id == lead_id)
        .order_by(Call.created_at.desc())
        .all()
    )



# ==========================================
# GET ALL CALLS
# ==========================================

def get_all_calls(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):

    return (
        db.query(Call)
        .order_by(Call.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )



# ==========================================
# UPDATE CALL
# ==========================================

def update_call(
    db: Session,
    call_id: UUID,
    call_data: CallUpdate,
):

    call = get_call_by_id(
        db,
        call_id
    )


    if not call:

        return None


    update_data = call_data.model_dump(
        exclude_unset=True
    )


    for key, value in update_data.items():

        setattr(
            call,
            key,
            value
        )


    db.commit()

    db.refresh(call)


    return call



# ==========================================
# DELETE CALL
# ==========================================

def delete_call(
    db: Session,
    call_id: UUID,
):

    call = get_call_by_id(
        db,
        call_id
    )


    if not call:

        return None


    db.delete(call)

    db.commit()


    return call