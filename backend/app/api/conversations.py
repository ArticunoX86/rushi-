from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import get_db


from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
)


from app.services.conversation_service import (
    save_message,
    get_message,
    get_call_memory,
    edit_message,
    remove_message,
)



router = APIRouter(
    prefix="/conversations",
    tags=["AI Conversations"],
)



# ==================================================
# SAVE AI / CUSTOMER MESSAGE
# ==================================================

@router.post(
    "/",
    response_model=ConversationResponse,
)
def create_message(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
):

    return save_message(
        db,
        conversation_data,
    )



# ==================================================
# GET MESSAGE
# ==================================================

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):

    message = get_message(
        db,
        conversation_id,
    )


    if not message:

        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )


    return message



# ==================================================
# GET FULL CALL MEMORY
# ==================================================

@router.get(
    "/call/{call_id}",
    response_model=list[ConversationResponse],
)
def get_conversation_history(
    call_id: UUID,
    db: Session = Depends(get_db),
):

    return get_call_memory(
        db,
        call_id,
    )



# ==================================================
# UPDATE MESSAGE
# ==================================================

@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def update_message(
    conversation_id: UUID,
    conversation_data: ConversationUpdate,
    db: Session = Depends(get_db),
):

    message = edit_message(
        db,
        conversation_id,
        conversation_data,
    )


    if not message:

        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )


    return message



# ==================================================
# DELETE MESSAGE
# ==================================================

@router.delete(
    "/{conversation_id}",
)
def delete_message(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):

    message = remove_message(
        db,
        conversation_id,
    )


    if not message:

        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )


    return {
        "message": "Conversation deleted successfully"
    }