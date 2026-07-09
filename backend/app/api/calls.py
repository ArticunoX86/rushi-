from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.call import (
    CallCreate,
    CallUpdate,
    CallResponse,
)

from app.services.call_service import (
    start_call,
    get_call,
    get_lead_calls,
    list_calls,
    finish_call,
    remove_call,
)


router = APIRouter(
    prefix="/calls",
    tags=["AI Calls"],
)


# ==================================================
# START AI CALL SESSION
# ==================================================

@router.post(
    "/",
    response_model=CallResponse,
)
def create_ai_call(
    call_data: CallCreate,
    db: Session = Depends(get_db),
):

    return start_call(
        db,
        call_data,
    )


# ==================================================
# GET ALL CALLS
# ==================================================

@router.get(
    "/",
    response_model=list[CallResponse],
)
def get_all_ai_calls(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):

    return list_calls(
        db,
        skip,
        limit,
    )


# ==================================================
# GET CALL DETAILS
# ==================================================

@router.get(
    "/{call_id}",
    response_model=CallResponse,
)
def get_ai_call(
    call_id: UUID,
    db: Session = Depends(get_db),
):

    call = get_call(
        db,
        call_id,
    )


    if not call:

        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )


    return call


# ==================================================
# GET CUSTOMER CALL HISTORY
# ==================================================

@router.get(
    "/lead/{lead_id}",
    response_model=list[CallResponse],
)
def get_customer_calls(
    lead_id: UUID,
    db: Session = Depends(get_db),
):

    return get_lead_calls(
        db,
        lead_id,
    )


# ==================================================
# FINISH CALL
# ==================================================

@router.put(
    "/{call_id}",
    response_model=CallResponse,
)
def finish_ai_call(
    call_id: UUID,
    call_data: CallUpdate,
    db: Session = Depends(get_db),
):

    call = finish_call(
        db,
        call_id,
        call_data,
    )


    if not call:

        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )


    return call


# ==================================================
# DELETE CALL
# ==================================================

@router.delete(
    "/{call_id}",
)
def delete_ai_call(
    call_id: UUID,
    db: Session = Depends(get_db),
):

    call = remove_call(
        db,
        call_id,
    )


    if not call:

        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )


    return {
        "message": "Call deleted successfully"
    }