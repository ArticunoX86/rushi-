from uuid import UUID

from sqlalchemy.orm import Session


from app.crud.conversation import (
    create_conversation,
    get_conversation_by_id,
    get_conversations_by_call,
    update_conversation,
    delete_conversation,
)


from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
)


from app.models.enums import (
    MessageIntent,
)


# ==================================================
# SAVE AI / CUSTOMER MESSAGE
# ==================================================

def save_message(
    db: Session,
    conversation_data: ConversationCreate,
):

    message_text = conversation_data.message.lower()


    # Basic AI intent detection v1

    if (
        "bhk" in message_text
        or "flat" in message_text
        or "apartment" in message_text
        or "budget" in message_text
    ):

        intent = MessageIntent.PROPERTY_REQUIREMENT


    elif (
        "call later" in message_text
        or "callback" in message_text
        or "later" in message_text
    ):

        intent = MessageIntent.CALLBACK_REQUEST


    elif (
        "not interested" in message_text
        or "don't want" in message_text
    ):

        intent = MessageIntent.NOT_INTERESTED


    elif (
        "hello" in message_text
        or "hi" in message_text
    ):

        intent = MessageIntent.GREETING


    else:

        intent = MessageIntent.UNKNOWN



    conversation = create_conversation(
        db,
        conversation_data,
    )


    conversation.intent = intent


    db.commit()


    db.refresh(
        conversation
    )


    return conversation



# ==================================================
# GET SINGLE MESSAGE
# ==================================================

def get_message(
    db: Session,
    conversation_id: UUID,
):

    return get_conversation_by_id(
        db,
        conversation_id,
    )



# ==================================================
# GET COMPLETE CALL MEMORY
# ==================================================

def get_call_memory(
    db: Session,
    call_id: UUID,
):

    return get_conversations_by_call(
        db,
        call_id,
    )



# ==================================================
# UPDATE MESSAGE
# ==================================================

def edit_message(
    db: Session,
    conversation_id: UUID,
    conversation_data: ConversationUpdate,
):

    return update_conversation(
        db,
        conversation_id,
        conversation_data,
    )



# ==================================================
# DELETE MESSAGE
# ==================================================

def remove_message(
    db: Session,
    conversation_id: UUID,
):

    return delete_conversation(
        db,
        conversation_id,
    )