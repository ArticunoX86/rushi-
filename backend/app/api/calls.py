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
    StartCallRequest,
)

from app.services.call_service import (
    start_call,
    get_call,
    get_lead_calls,
    list_calls,
    finish_call,
    remove_call,
)

from app.services.call_dispatcher import (
    start_ai_call,
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


# ==================================================
# START REAL AI CALL
# ==================================================

@router.post(
    "/start",
)
async def start_real_ai_call(
    request: StartCallRequest,
    db: Session = Depends(get_db),
):

    return await start_ai_call(
        db,
        request.lead_id,
    )


# ==================================================
# SUPERVISOR WHISPER HINT INJECTION
# ==================================================

@router.post("/{call_id}/whisper")
def send_whisper_hint(
    call_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
):
    hint = payload.get("hint")
    if not hint:
        raise HTTPException(status_code=400, detail="Hint is required")
        
    from app.services.ai_service import active_whispers
    active_whispers[str(call_id)] = hint
    print(f"[SUPERVISOR CONSOLE] Whisper hint queued for call {call_id}: {hint}")
    
    # Broadcast to all connected WebSockets
    from app.services.device_connection_manager import device_manager
    import asyncio
    asyncio.create_task(device_manager.broadcast_all({
        "action": "WHISPER_INJECTED",
        "event": "WHISPER_INJECTED",
        "payload": {
            "call_id": str(call_id),
            "hint": hint
        }
    }))
    
    return {"status": "success", "hint": hint}


# ==================================================
# SUPERVISOR CALL TAKEOVER BRIDGE
# ==================================================

@router.post("/{call_id}/takeover")
def force_call_takeover(
    call_id: UUID,
    db: Session = Depends(get_db),
):
    from app.services.device_connection_manager import device_manager
    import asyncio
    
    # Broadcast TAKEOVER command
    asyncio.create_task(device_manager.broadcast_all({
        "action": "SUPERVISOR_TAKEOVER",
        "event": "SUPERVISOR_TAKEOVER",
        "payload": {
            "call_id": str(call_id)
        }
    }))
    print(f"[SUPERVISOR CONSOLE] Broadcasted TAKE_OVER request for call {call_id}")
    
    return {"status": "success", "call_id": str(call_id)}