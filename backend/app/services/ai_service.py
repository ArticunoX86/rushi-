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
    process_conversation_turn,
)
from app.crud.conversation import get_conversations_by_call

# Global in-memory dictionary for active supervisor whispers
active_whispers = {}


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
    # Ensure Call Exists (for testing scripts that send random call_ids)
    # ==================================================
    from app.models.call import Call
    from app.models.enums import CallDirection, CallStatus
    
    db_call = db.query(Call).filter(Call.id == request.call_id).first()
    if not db_call:
        db_call = Call(
            id=request.call_id,
            lead_id=request.lead_id,
            direction=CallDirection.OUTBOUND,
            status=CallStatus.IN_PROGRESS
        )
        db.add(db_call)
        db.commit()
        db.refresh(db_call)

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
    # Unified Single-Turn AI Engine
    # ==================================================
    
    lead_info = {
        "first_name": lead.first_name,
        "preferred_city": lead.preferred_city,
        "budget_max": lead.budget_max,
        "bedrooms": lead.bedrooms,
        "recommended_properties": []
    }
    
    recommendations = get_property_recommendations(db, lead.id)
    if recommendations and recommendations.get("recommended_properties"):
        for r in recommendations["recommended_properties"]:
            lead_info["recommended_properties"].append(f"{r.title} ({r.locality}) for {r.price} INR")

    # Fetch recent dialog history
    history_lines = []
    try:
        db_history = get_conversations_by_call(db, request.call_id)
        for msg in db_history:
            sender_label = "Customer" if msg.sender == MessageSender.CUSTOMER else "AI"
            history_lines.append(f"{sender_label}: {msg.message}")
    except Exception as e:
        print("Failed to load conversation history:", e)

    whisper_hint = active_whispers.pop(str(request.call_id), None)
    
    # Fetch active Voice Agent from DB to use its prompt
    from app.crud.voice_agent import voice_agent as crud_voice_agent
    active_agents = crud_voice_agent.get_active(db)
    agent_prompt = active_agents[0].prompt if active_agents else None
    
    # ==================================================
    # Fetch Relevant Training Data (Category-Filtered)
    # ==================================================
    from app.crud.ai_training_data import ai_training_data as crud_training
    
    # Extract keywords from the customer message for smart injection
    customer_message_lower = request.message.lower()
    intent_keywords = []
    objection_keywords = ["not interested", "no thanks", "busy", "call later", "expensive",
                          "budget", "too much", "family", "wife", "discuss", "location", "area",
                          "loan", "emi", "possess", "ready", "rera", "visit", "see"]
    for kw in objection_keywords:
        if kw in customer_message_lower:
            intent_keywords.append(kw)
    
    relevant_entries = crud_training.get_relevant(db, intent_keywords)
    training_context = [
        {
            "category": e.category.value if e.category else "",
            "title": e.title,
            "trigger_phrase": e.trigger_phrase or "",
            "situation_context": e.situation_context or "",
            "ideal_response": e.ideal_response,
        }
        for e in relevant_entries
    ]
    training_entry_ids = [e.id for e in relevant_entries]
    
    # SINGLE API CALL: Extracts CRM data AND generates response
    ai_result = process_conversation_turn(
        history=history_lines,
        customer_message=request.message,
        lead_info=lead_info,
        whisper_hint=whisper_hint,
        system_prompt=agent_prompt,
        training_context=training_context,
    )
    
    # Track usage of injected training entries
    if training_entry_ids:
        try:
            crud_training.increment_usage(db, training_entry_ids)
        except Exception as e:
            print("Failed to track training entry usage:", e)
    
    extracted = ai_result.get("crm_update", {})
    reply = ai_result.get("conversational_reply", "I understand. Give me a moment to check.")

    # ==================================================
    # Update Lead CRM Automatically
    # ==================================================

    def parse_budget(raw):
        """Convert Indian currency strings like '1 Crore', '50 Lakhs' to numeric."""
        if raw is None:
            return None
        if isinstance(raw, (int, float)):
            return raw
        s = str(raw).strip().lower().replace(",", "").replace("₹", "").replace("rs", "").replace("inr", "").strip()
        try:
            # Direct numeric
            return float(s)
        except ValueError:
            pass
        import re
        m = re.search(r'([\d.]+)\s*(crore|cr|crores)', s)
        if m:
            return float(m.group(1)) * 10000000
        m = re.search(r'([\d.]+)\s*(lakh|lakhs|lac|lacs|l)', s)
        if m:
            return float(m.group(1)) * 100000
        m = re.search(r'([\d.]+)\s*(k|thousand)', s)
        if m:
            return float(m.group(1)) * 1000
        m = re.search(r'[\d.]+', s)
        if m:
            return float(m.group(0))
        return None

    if extracted.get("city"):
        lead.preferred_city = extracted.get("city")
    if extracted.get("bedrooms"):
        lead.bedrooms = extracted.get("bedrooms")
    if extracted.get("budget"):
        parsed = parse_budget(extracted.get("budget"))
        if parsed is not None:
            lead.budget_max = parsed
    if extracted.get("summary"):
        lead.conversation_summary = extracted.get("summary")

    db.commit()
    db.refresh(lead)

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

    # Broadcast Customer message + AI message immediately to supervisor console WebSocket
    try:
        from app.services.device_connection_manager import device_manager
        import asyncio
        asyncio.create_task(device_manager.broadcast_all({
            "action": "TRANSCRIPT_LIVE",
            "event": "TRANSCRIPT_LIVE",
            "payload": {
                "call_id": str(request.call_id),
                "customer_message": request.message,
                "ai_message": reply
            }
        }))
    except Exception as e:
        print("Failed to broadcast live transcript:", e)

    # ==================================================
    # Return Response
    # ==================================================

    return AIChatResponse(
        reply=reply,
        detected_city=extracted.get("city"),
        detected_budget=extracted.get("budget"),
        detected_bedrooms=extracted.get("bedrooms"),
    )

    # ==================================================
# REAL TIME VOICE AI ENGINE
# Deepgram → Gemini → ElevenLabs Pipeline
# ==================================================

async def process_voice_message(

    message: str,

):


    # ==================================================
    # Gemini Understanding
    # ==================================================

    extracted = analyze_customer_message(

        message

    )



    # ==================================================
    # Generate Natural AI Reply
    # ==================================================

    intent = extracted.get(

        "intent"

    )


    city = extracted.get(

        "city"

    )


    bedrooms = extracted.get(

        "bedrooms"

    )


    budget = extracted.get(

        "budget"

    )



    # Property requirement conversation

    if city or bedrooms or budget:


        reply = (

            "Great, I have noted your property requirement. "

        )


        if bedrooms:


            reply += (

                f"You are looking for a {bedrooms} BHK property. "

            )


        if city:


            reply += (

                f"Location preference is {city}. "

            )


        if budget:


            reply += (

                f"Your budget is around {budget}. "

            )


        reply += (

            "Let me check the best available options for you."

        )


        return reply



    # Callback handling

    if intent == "callback_request":


        return (

            "Sure, I will schedule a callback for you."

        )



    # Not interested

    if intent == "not_interested":


        return (

            "No problem. Thank you for your time."

        )



    # Default conversation

    return (

        "I understand. Could you please share your preferred "
        "location, budget and property requirement?"

    )