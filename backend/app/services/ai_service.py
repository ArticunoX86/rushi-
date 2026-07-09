from sqlalchemy.orm import Session


from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
)


from app.crud.lead import (
    get_lead,
)


from app.services.recommendation_service import (
    get_property_recommendations,
)


from app.schemas.conversation import (
    ConversationCreate,
)


from app.services.conversation_service import (
    save_message,
)


from app.models.enums import (
    MessageSender,
)


from app.integrations.gemini.client import (
    analyze_customer_message,
)


# ==================================================
# AI CHAT ENGINE WITH GEMINI MEMORY
# ==================================================

def process_customer_message(
    db: Session,
    request: AIChatRequest,
):


    # ==================================================
    # Get Lead
    # ==================================================

    lead = get_lead(
        db,
        request.lead_id,
    )


    if not lead:

        return AIChatResponse(
            reply="Lead not found"
        )


    # ==================================================
    # Save Customer Message
    # ==================================================

    save_message(
        db,
        ConversationCreate(

            call_id=request.call_id,

            sender=MessageSender.CUSTOMER,

            message=request.message,

        ),
    )


    # ==================================================
    # Gemini LLM Understanding
    # ==================================================

    extracted = analyze_customer_message(
        request.message
    )


    # ==================================================
    # Update Lead CRM Automatically
    # ==================================================

    if extracted.get("city"):

        lead.preferred_city = extracted.get(
            "city"
        )


    if extracted.get("bedrooms"):

        lead.bedrooms = extracted.get(
            "bedrooms"
        )


    if extracted.get("budget"):

        lead.budget_max = extracted.get(
            "budget"
        )


    if extracted.get("summary"):

        lead.conversation_summary = extracted.get(
            "summary"
        )


    db.commit()


    db.refresh(
        lead
    )


    # ==================================================
    # Property Recommendation Engine
    # ==================================================

    recommendations = get_property_recommendations(
        db,
        lead.id,
    )


    matches = recommendations[
        "matches_found"
    ]


    # ==================================================
    # Generate AI Reply
    # ==================================================

    if matches > 0:


        reply = (
            f"I found {matches} properties "
            f"matching your requirements."
        )


    else:


        reply = (
            "I have understood and saved your requirements. "
            "Our team will help you find suitable properties."
        )


    # ==================================================
    # Save AI Response
    # ==================================================

    save_message(
        db,
        ConversationCreate(

            call_id=request.call_id,

            sender=MessageSender.AI,

            message=reply,

        ),
    )


    # ==================================================
    # Return Response
    # ==================================================

    return AIChatResponse(

        reply=reply,

        detected_city=extracted.get(
            "city"
        ),

        detected_budget=extracted.get(
            "budget"
        ),

        detected_bedrooms=extracted.get(
            "bedrooms"
        ),

    )