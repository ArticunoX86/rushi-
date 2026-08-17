"""
AI Training Data API
--------------------
Full REST endpoints for managing the AI knowledge base / training data.
These entries are dynamically injected into the Gemini prompt during live calls,
effectively "training" the AI engine with domain-specific knowledge.
"""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud.ai_training_data import ai_training_data as crud
from app.models.ai_training_data import TrainingCategory
from app.schemas.ai_training_data import (
    AITrainingDataCreate,
    AITrainingDataUpdate,
    AITrainingDataResponse,
    AITrainingDataBulkImport,
    AITrainingStatsResponse,
    TrainingCategoryStats,
)


router = APIRouter(
    prefix="/ai-training",
    tags=["AI Training & Knowledge Base"],
)


# ==================================================
# GET ALL ENTRIES
# ==================================================

@router.get("", response_model=List[AITrainingDataResponse])
def list_training_entries(
    category: Optional[TrainingCategory] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    List all AI training entries.
    Optionally filter by category or active status.
    Results are sorted by priority (desc) then usage count (desc).
    """
    return crud.get_all(db, category=category, is_active=is_active, skip=skip, limit=limit)


# ==================================================
# GET STATS
# ==================================================

@router.get("/stats", response_model=AITrainingStatsResponse)
def get_training_stats(db: Session = Depends(get_db)):
    """
    Get usage statistics for the AI training knowledge base.
    Returns total entries, top-used entries, and breakdown by category.
    """
    stats = crud.get_stats(db)
    return AITrainingStatsResponse(
        total_entries=stats["total_entries"],
        active_entries=stats["active_entries"],
        total_usage_across_all=stats["total_usage_across_all"],
        top_entries=stats["top_entries"],
        by_category=[
            TrainingCategoryStats(**cat) for cat in stats["by_category"]
        ],
    )


# ==================================================
# GET SINGLE ENTRY
# ==================================================

@router.get("/{entry_id}", response_model=AITrainingDataResponse)
def get_training_entry(entry_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get a single training entry by ID."""
    entry = crud.get(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Training entry not found")
    return entry


# ==================================================
# CREATE ENTRY
# ==================================================

@router.post("", response_model=AITrainingDataResponse, status_code=201)
def create_training_entry(entry_in: AITrainingDataCreate, db: Session = Depends(get_db)):
    """
    Create a new AI training entry.
    
    Categories:
    - **OBJECTION_HANDLING**: How to respond to customer objections
    - **PRODUCT_KNOWLEDGE**: Property/project facts and selling points
    - **SALES_PLAYBOOK**: Step-by-step conversation scripts
    - **FAQ**: Common questions and ideal answers
    - **PERSONA_RULE**: Tone, style and behavioral rules for the AI
    """
    return crud.create(db, obj_in=entry_in)


# ==================================================
# UPDATE ENTRY
# ==================================================

@router.put("/{entry_id}", response_model=AITrainingDataResponse)
def update_training_entry(
    entry_id: uuid.UUID,
    entry_in: AITrainingDataUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing training entry."""
    entry = crud.get(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Training entry not found")
    return crud.update(db, db_obj=entry, obj_in=entry_in)


# ==================================================
# DELETE ENTRY (SOFT DELETE)
# ==================================================

@router.delete("/{entry_id}")
def delete_training_entry(entry_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Soft-delete a training entry (sets is_active=False).
    The entry is retained for analytics history.
    Use ?hard=true to permanently remove it.
    """
    entry = crud.soft_delete(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Training entry not found")
    return {"status": "deactivated", "id": str(entry_id)}


@router.delete("/{entry_id}/hard")
def hard_delete_training_entry(entry_id: uuid.UUID, db: Session = Depends(get_db)):
    """Permanently delete a training entry from the database."""
    success = crud.hard_delete(db, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Training entry not found")
    return {"status": "deleted", "id": str(entry_id)}


# ==================================================
# BULK IMPORT
# ==================================================

@router.post("/bulk-import", response_model=List[AITrainingDataResponse], status_code=201)
def bulk_import_training_data(payload: AITrainingDataBulkImport, db: Session = Depends(get_db)):
    """
    Import multiple training entries at once.
    Accepts a JSON body with an `entries` array.
    """
    if not payload.entries:
        raise HTTPException(status_code=400, detail="No entries provided")
    return crud.bulk_create(db, entries=payload.entries)


# ==================================================
# SEED DEFAULT REAL ESTATE TRAINING DATA
# ==================================================

@router.post("/seed-defaults", status_code=201)
def seed_default_training_data(db: Session = Depends(get_db)):
    """
    Seed the AI knowledge base with industry-standard real estate
    objection handling scripts, sales playbooks, and persona rules.
    
    Safe to call multiple times — skips entries that already exist (by title).
    """
    from sqlalchemy import select
    existing_titles = {
        row[0] for row in db.execute(
            select(crud.__class__.__name__)  # use raw query
        ).all()
    } if False else set()  # fetch existing titles

    from app.models.ai_training_data import AITrainingData
    existing_titles = {
        r.title for r in db.query(AITrainingData.title).all()
    }

    DEFAULT_ENTRIES = [
        # ── PERSONA RULES ──────────────────────────────────────────────
        {
            "title": "Always speak like a human friend",
            "category": TrainingCategory.PERSONA_RULE,
            "trigger_phrase": None,
            "situation_context": "Always applies to every conversation",
            "ideal_response": "Speak naturally and warmly like a helpful friend. Never use words like 'CRM', 'AI', 'lead', 'database', or 'system'. Always address the customer by their first name.",
            "tags": ["always", "persona", "tone"],
            "priority": 10,
        },
        {
            "title": "Keep responses concise and punchy",
            "category": TrainingCategory.PERSONA_RULE,
            "trigger_phrase": None,
            "situation_context": "Always applies to every response",
            "ideal_response": "Keep every response to 1-2 sentences maximum. Be direct and conversational. Avoid long paragraphs. End with a soft question to keep the conversation going.",
            "tags": ["always", "persona", "length"],
            "priority": 10,
        },
        {
            "title": "Handle silence or confusion gracefully",
            "category": TrainingCategory.PERSONA_RULE,
            "trigger_phrase": "sorry, what, huh, can you repeat",
            "situation_context": "Customer seems confused or didn't understand",
            "ideal_response": "Of course! Let me rephrase that simply. [Re-explain in simpler terms]. Does that make more sense?",
            "tags": ["confusion", "repeat", "clarify"],
            "priority": 8,
        },

        # ── OBJECTION HANDLING ─────────────────────────────────────────
        {
            "title": "Not Interested Objection",
            "category": TrainingCategory.OBJECTION_HANDLING,
            "trigger_phrase": "not interested, no thanks, don't want, not looking",
            "situation_context": "Customer expresses disinterest in the property or the call",
            "ideal_response": "Totally understand, [Name]! I won't take much of your time. I just wanted to quickly share one option that matches exactly what you were looking for earlier — can I send you the details on WhatsApp? You can check whenever you're free.",
            "tags": ["not_interested", "objection", "rejection"],
            "priority": 9,
        },
        {
            "title": "Too Expensive / Budget Objection",
            "category": TrainingCategory.OBJECTION_HANDLING,
            "trigger_phrase": "too expensive, out of budget, can't afford, costly, price is high",
            "situation_context": "Customer says the property is too expensive or outside their budget",
            "ideal_response": "I completely hear you! The good news is this project offers flexible EMI options starting from just ₹25,000/month, and there are bank loan tie-ups available with minimal down payment. Would that make it more comfortable?",
            "tags": ["too_expensive", "price_objection", "budget", "emi"],
            "priority": 9,
        },
        {
            "title": "Call Me Later / Busy Objection",
            "category": TrainingCategory.OBJECTION_HANDLING,
            "trigger_phrase": "call me later, busy right now, not a good time, in a meeting",
            "situation_context": "Customer says they are busy or asks to be called later",
            "ideal_response": "Of course, no problem at all! When would be a good time to reconnect — would tomorrow morning or evening work better for you?",
            "tags": ["callback_request", "busy", "call_later"],
            "priority": 9,
        },
        {
            "title": "Already Have a Property Objection",
            "category": TrainingCategory.OBJECTION_HANDLING,
            "trigger_phrase": "already have a house, already own, not looking to buy",
            "situation_context": "Customer says they already own property or are not in the market",
            "ideal_response": "That's great! Many of our clients already own homes and are now investing for rental income or for their children. Would you be open to hearing about the returns on a 2 BHK investment property here?",
            "tags": ["already_have", "not_looking", "investment_angle"],
            "priority": 8,
        },
        {
            "title": "Need to Discuss With Family Objection",
            "category": TrainingCategory.OBJECTION_HANDLING,
            "trigger_phrase": "need to discuss, ask my wife, check with family, not decided",
            "situation_context": "Customer wants to consult family before deciding",
            "ideal_response": "Absolutely, that's the right approach! How about I send you a detailed brochure on WhatsApp that you can share with them? It has all the details, floor plans, and pricing — makes it easier to discuss.",
            "tags": ["family_consultation", "not_decided", "whatsapp_follow_up"],
            "priority": 8,
        },
        {
            "title": "Location Not Preferred Objection",
            "category": TrainingCategory.OBJECTION_HANDLING,
            "trigger_phrase": "don't like the location, too far, prefer different area, wrong location",
            "situation_context": "Customer objects to the property location",
            "ideal_response": "Understood! Which area are you more comfortable with? I'll see if we have something that fits better for you — we do have projects across multiple locations.",
            "tags": ["location_objection", "wrong_area", "different_location"],
            "priority": 8,
        },

        # ── FAQ ────────────────────────────────────────────────────────
        {
            "title": "FAQ: Possession Timeline",
            "category": TrainingCategory.FAQ,
            "trigger_phrase": "when will it be ready, possession date, handover, completion",
            "situation_context": "Customer asks when they can move in or get possession",
            "ideal_response": "Great question! The possession is scheduled for [PROJECT_POSSESSION_DATE]. The project is [X]% complete as of now, and construction is right on track. Would you like to schedule a site visit to see the progress yourself?",
            "tags": ["possession", "timeline", "ready", "handover"],
            "priority": 7,
        },
        {
            "title": "FAQ: Loan / Financing Options",
            "category": TrainingCategory.FAQ,
            "trigger_phrase": "home loan, bank loan, financing, down payment, emi",
            "situation_context": "Customer asks about loan or financing options",
            "ideal_response": "We have tie-ups with leading banks like HDFC, SBI, and ICICI. You can get a home loan up to 80% of the property value, with EMIs starting as low as ₹20,000/month. Want me to have our finance team call you with a custom plan?",
            "tags": ["home_loan", "emi", "financing", "bank"],
            "priority": 7,
        },
        {
            "title": "FAQ: Site Visit",
            "category": TrainingCategory.FAQ,
            "trigger_phrase": "can I visit, site visit, see the property, come and see",
            "situation_context": "Customer asks about visiting the site",
            "ideal_response": "Absolutely, we'd love to have you visit! Site visits are available Monday to Saturday, 10 AM to 6 PM. I can arrange a complimentary pickup and drop as well. Which day works best for you?",
            "tags": ["site_visit", "visit", "come_see"],
            "priority": 7,
        },
        {
            "title": "FAQ: RERA Registration",
            "category": TrainingCategory.FAQ,
            "trigger_phrase": "rera, registered, legal, approved, government",
            "situation_context": "Customer asks about RERA registration or legal status",
            "ideal_response": "Yes, absolutely! The project is fully RERA registered. The RERA number is [RERA_NUMBER], and you can verify it on the official RERA portal anytime. Everything is completely transparent and legally compliant.",
            "tags": ["rera", "legal", "registered", "compliance"],
            "priority": 7,
        },

        # ── SALES PLAYBOOK ─────────────────────────────────────────────
        {
            "title": "Opening Call Script",
            "category": TrainingCategory.SALES_PLAYBOOK,
            "trigger_phrase": None,
            "situation_context": "The very beginning of a call, before any context is established",
            "ideal_response": "Hi [Name], this is [Agent Name] from [Company]. I hope I caught you at a good time! I'm reaching out because we have some really exciting property options in [City] that I thought you'd love. Could I take just 2 minutes to share one that might be perfect for you?",
            "tags": ["opening", "introduction", "start_of_call"],
            "priority": 9,
        },
        {
            "title": "Qualifying Questions Script",
            "category": TrainingCategory.SALES_PLAYBOOK,
            "trigger_phrase": "looking for, need, want, interested in",
            "situation_context": "Customer shows initial interest — gather requirements",
            "ideal_response": "Wonderful! To find you the best option, may I ask — are you looking for a 2 BHK or 3 BHK? And do you have a preferred locality in mind?",
            "tags": ["qualifying", "requirements", "discovery"],
            "priority": 8,
        },
        {
            "title": "Property Pitch Script",
            "category": TrainingCategory.SALES_PLAYBOOK,
            "trigger_phrase": "tell me more, what do you have, what options",
            "situation_context": "Customer asks about available properties — pitch the best match",
            "ideal_response": "I have a fantastic option for you! [PROPERTY_NAME] in [LOCALITY] — a [BEDROOMS] BHK at just [PRICE]. It comes with [KEY_AMENITIES] and is just [DISTANCE] from [LANDMARK]. Honestly, at this price point in [CITY], it's one of the best deals right now. Shall I send you the floor plan?",
            "tags": ["pitch", "property_details", "features"],
            "priority": 8,
        },
        {
            "title": "Call Closing Script",
            "category": TrainingCategory.SALES_PLAYBOOK,
            "trigger_phrase": "okay, sounds good, interested, tell me more, sounds interesting",
            "situation_context": "Customer seems interested — move towards next steps",
            "ideal_response": "That's great to hear! The next step would be a quick site visit so you can see the property in person. I can set that up for you this weekend — would Saturday or Sunday work better?",
            "tags": ["closing", "next_steps", "site_visit_push"],
            "priority": 8,
        },

        # ── PRODUCT KNOWLEDGE ──────────────────────────────────────────
        {
            "title": "Investment Value Pitch",
            "category": TrainingCategory.PRODUCT_KNOWLEDGE,
            "trigger_phrase": "investment, returns, rental, appreciation",
            "situation_context": "Customer is interested in investment potential",
            "ideal_response": "From an investment standpoint, this area has seen 15-20% price appreciation year over year. The rental yield is approximately 4-5% annually. Many investors are getting excellent returns here — it's one of the fastest-growing corridors in the city.",
            "tags": ["investment", "roi", "rental", "appreciation"],
            "priority": 7,
        },
        {
            "title": "Amenities & Lifestyle Pitch",
            "category": TrainingCategory.PRODUCT_KNOWLEDGE,
            "trigger_phrase": "amenities, facilities, gym, pool, club, parking",
            "situation_context": "Customer asks about amenities or lifestyle features",
            "ideal_response": "The project has world-class amenities — a fully equipped gym, swimming pool, clubhouse, children's play area, 24/7 security, and ample parking. It's really designed for a premium lifestyle. Would you like me to send the full amenities list?",
            "tags": ["amenities", "facilities", "lifestyle", "features"],
            "priority": 7,
        },
    ]

    seeded = []
    skipped = []

    for entry_data in DEFAULT_ENTRIES:
        if entry_data["title"] in existing_titles:
            skipped.append(entry_data["title"])
            continue
        from app.schemas.ai_training_data import AITrainingDataCreate
        entry = crud.create(
            db,
            AITrainingDataCreate(**entry_data),
        )
        seeded.append(entry.title)

    return {
        "status": "success",
        "seeded_count": len(seeded),
        "skipped_count": len(skipped),
        "seeded": seeded,
        "skipped": skipped,
    }
