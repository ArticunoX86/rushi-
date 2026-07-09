from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conversation import Conversation

from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
)


# ==================================================
# SAVE MESSAGE
# ==================================================

def create_conversation(
    db: Session,
    conversation_data: ConversationCreate,
):

    conversation = Conversation(
        **conversation_data.model_dump()
    )


    db.add(
        conversation
    )


    db.commit()


    db.refresh(
        conversation
    )


    return conversation



# ==================================================
# GET MESSAGE BY ID
# ==================================================

def get_conversation_by_id(
    db: Session,
    conversation_id: UUID,
):

    return (
        db.query(
            Conversation
        )
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )



# ==================================================
# GET CALL CONVERSATION HISTORY
# ==================================================

def get_conversations_by_call(
    db: Session,
    call_id: UUID,
):

    return (
        db.query(
            Conversation
        )
        .filter(
            Conversation.call_id == call_id
        )
        .order_by(
            Conversation.created_at.asc()
        )
        .all()
    )



# ==================================================
# UPDATE MESSAGE
# ==================================================

def update_conversation(
    db: Session,
    conversation_id: UUID,
    conversation_data: ConversationUpdate,
):

    conversation = get_conversation_by_id(
        db,
        conversation_id,
    )


    if not conversation:

        return None


    update_data = conversation_data.model_dump(
        exclude_unset=True
    )


    for key, value in update_data.items():

        setattr(
            conversation,
            key,
            value,
        )


    db.commit()


    db.refresh(
        conversation
    )


    return conversation



# ==================================================
# DELETE MESSAGE
# ==================================================

def delete_conversation(
    db: Session,
    conversation_id: UUID,
):

    conversation = get_conversation_by_id(
        db,
        conversation_id,
    )


    if not conversation:

        return None


    db.delete(
        conversation
    )


    db.commit()


    return conversation