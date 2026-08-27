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

# ==================================================
# GUARDRAIL IMPORTS
# ==================================================
from app.guardrails.input_validator import validate_input
from app.guardrails.output_validator import validate_output
from app.guardrails.call_state_machine import get_or_create_state_machine
from app.guardrails.sentiment_analyzer import analyze_sentiment
from app.core.config import settings


# Global in-memory dictionary for active supervisor whispers
active_whispers = {}


# ==================================================
# SAFE DEFLECTION RESPONSES
# ==================================================
INPUT_BLOCKED_RESPONSES = {
    "prompt_injection": "I appreciate the creative question! But let's get back to finding you the perfect property. What's your preferred location?",
    "toxic_content": "I understand you might be frustrated. I'm here to help — would you like to continue, or shall I have someone call you back at a better time?",
    "excessive_length": "I got a lot of that! Could you give me the short version — what's the most important thing you're looking for in a property?",
    "default": "I didn't quite catch that. Could you tell me a bit about what kind of property you're looking for?",
}


# ==================================================
# AI CHAT ENGINE WITH GEMINI MEMORY + GUARDRAILS
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
    # GUARDRAIL 1: INPUT VALIDATION
    # ==================================================
    input_result = validate_input(request.message)
    
    if not input_result.is_safe:
        print(f"[GUARDRAIL] Input blocked: {input_result.reason}")
        
        # Log the violation as a supervisor alert
        try:
            from app.api.supervisor_alerts import add_alert
            add_alert(
                call_id=str(request.call_id),
                alert_type=input_result.violation_type,
                message=f"Input blocked: {input_result.reason}",
                severity="WARNING" if input_result.violation_type != "prompt_injection" else "CRITICAL",
            )
        except Exception as e:
            print(f"[GUARDRAIL] Failed to create alert: {e}")
        
        # Return a safe deflection instead of calling Gemini
        safe_reply = INPUT_BLOCKED_RESPONSES.get(
            input_result.violation_type,
            INPUT_BLOCKED_RESPONSES["default"],
        )
        
        # Still save both messages for audit trail
        save_message(db, ConversationCreate(
            call_id=request.call_id,
            sender=MessageSender.CUSTOMER,
            message=request.message,
        ))
        save_message(db, ConversationCreate(
            call_id=request.call_id,
            sender=MessageSender.AI,
            message=safe_reply,
        ))
        
        return AIChatResponse(reply=safe_reply)


    # ==================================================
    # GUARDRAIL 2: SENTIMENT ANALYSIS
    # ==================================================
    sentiment_result = analyze_sentiment(
        customer_message=request.message,
        call_id=str(request.call_id),
    )
    
    if sentiment_result.should_alert:
        print(f"[GUARDRAIL] Sentiment alert: {sentiment_result.label} (score: {sentiment_result.score})")
        try:
            from app.api.supervisor_alerts import add_alert
            add_alert(
                call_id=str(request.call_id),
                alert_type="sentiment_drop",
                message=f"Customer sentiment is {sentiment_result.label} (score: {sentiment_result.score}). Trigger: '{sentiment_result.trigger_phrase}'",
                severity="CRITICAL" if sentiment_result.label == "ANGRY" else "WARNING",
            )
        except Exception as e:
            print(f"[GUARDRAIL] Failed to create sentiment alert: {e}")


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
    # GUARDRAIL 3: STATE MACHINE — Get phase-specific prompt
    # ==================================================
    state_prompt = ""
    if settings.AI_ENABLE_STATE_MACHINE:
        state_machine = get_or_create_state_machine(str(request.call_id))
        state_prompt = state_machine.get_state_prompt()


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
    
    # ==================================================
    # Fetch Salesforce Knowledge Base Context (RAG)
    # ==================================================
    from app.api.salesforce_knowledge import generate_embedding
    from app.models.knowledge import DocumentChunk
    
    rag_context_snippets = []
    try:
        # Generate embedding for the incoming customer message
        query_embedding = generate_embedding(request.message)
        
        # Skip query if embedding failed (returned all zeros)
        if not all(v == 0.0 for v in query_embedding):
            # Use pgvector cosine distance to find top 3 relevant chunks
            similar_chunks = db.query(DocumentChunk).order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            ).limit(3).all()
            
            for chunk in similar_chunks:
                rag_context_snippets.append(chunk.chunk_text)
    except Exception as e:
        db.rollback()
        print(f"Failed to fetch RAG context: {e}")

    if rag_context_snippets:
        training_context.append({
            "category": "SALESFORCE_KNOWLEDGE_BASE",
            "title": "Verified Ground Truth Facts from Salesforce",
            "trigger_phrase": "",
            "situation_context": "Use these exact facts to answer any questions about properties, amenities, pricing, or rules.",
            "ideal_response": "\n\n".join(rag_context_snippets)
        })
    
    # SINGLE API CALL: Extracts CRM data AND generates response
    ai_result = process_conversation_turn(
        history=history_lines,
        customer_message=request.message,
        lead_info=lead_info,
        whisper_hint=whisper_hint,
        system_prompt=agent_prompt,
        training_context=training_context,
        state_prompt=state_prompt,
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
    # GUARDRAIL 4: OUTPUT VALIDATION
    # ==================================================
    output_result = validate_output(reply)
    
    if not output_result.is_safe:
        print(f"[GUARDRAIL] Output blocked: {output_result.reason}")
        reply = output_result.safe_text
        
        try:
            from app.api.supervisor_alerts import add_alert
            add_alert(
                call_id=str(request.call_id),
                alert_type=output_result.violation_type,
                message=f"Output modified: {output_result.reason}. Original: '{output_result.original_text[:100]}...'",
                severity="WARNING",
            )
        except Exception as e:
            print(f"[GUARDRAIL] Failed to create output alert: {e}")


    # ==================================================
    # GUARDRAIL 5: STATE MACHINE TRANSITION
    # ==================================================
    if settings.AI_ENABLE_STATE_MACHINE:
        detected_intent = extracted.get("intent", "UNKNOWN")
        state_machine = get_or_create_state_machine(str(request.call_id))
        new_state = state_machine.transition(detected_intent)
        print(f"[STATE MACHINE] Call {request.call_id}: {state_machine.state_history[-2].value if len(state_machine.state_history) > 1 else 'START'} → {new_state.value}")


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
                "ai_message": reply,
                "sentiment": sentiment_result.label if sentiment_result else "NEUTRAL",
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