"""
🧪 Comprehensive AI Engine Scenario Tester
Tests all types of customer scenarios against the Sales Playbook.
"""
import sys, os, uuid, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.lead import Lead
from app.models.call import Call
from app.services.ai_service import process_customer_message
from app.schemas.ai import AIChatRequest

# ═══════════════════════════════════════════════════════════
# 🎯 SCENARIO DEFINITIONS
# ═══════════════════════════════════════════════════════════

SCENARIOS = [
    {
        "name": "🟢 HAPPY PATH — Interested customer books a site visit",
        "messages": [
            "Hello?",
            "Yeah I'm still looking for a place in Mumbai.",
            "A 2 BHK apartment would be ideal.",
            "Hmm around 1 crore or so.",
            "Oh really? That sounds great, I'd love to see it!",
            "Saturday works for me, maybe around 3 PM?",
        ]
    },
    {
        "name": "🔴 HOSTILE REJECTION — Not interested, wants to hang up",
        "messages": [
            "Who is this? How did you get my number?",
            "I'm not interested. Stop calling me.",
        ]
    },
    {
        "name": "🟡 BUSY CUSTOMER — No time to talk, falls back to WhatsApp",
        "messages": [
            "Hello?",
            "Yeah look I'm in a meeting right now, can't talk.",
            "Sure, just send it on WhatsApp.",
        ]
    },
    {
        "name": "🟠 BUDGET OBJECTION — Everything is too expensive",
        "messages": [
            "Hi, yes I was looking.",
            "I need a 2 BHK in Pune.",
            "Honestly, my budget is very tight, maybe 40-50 lakhs max.",
            "No I don't think I can afford anything right now. Maybe later.",
            "Okay fine, send me whatever you have on WhatsApp.",
        ]
    },
    {
        "name": "🔵 JUST BROWSING — Not ready to buy yet",
        "messages": [
            "Yeah hi.",
            "I'm not really in a rush, just casually checking the market.",
            "Maybe in 6 months or so.",
            "Sure, you can send me listings on WhatsApp, that's fine.",
        ]
    },
    {
        "name": "🟣 COMPETITOR MENTION — Already talking to another agent",
        "messages": [
            "Hello?",
            "Actually I'm already working with another broker, MagicBricks wala.",
            "Well, what do you have that's different?",
            "Hmm okay, I can take a look. Send it over.",
        ]
    },
    {
        "name": "⚪ PRICE HUNTER — Keeps asking about exact prices",
        "messages": [
            "Hi yes, I'm looking for a 3 BHK in Mumbai.",
            "What's the exact price of the properties you have?",
            "Come on, just tell me the price range at least.",
            "Okay fine, send me the details on WhatsApp with prices.",
        ]
    },
    {
        "name": "🟤 RENTAL ENQUIRY — Wants to rent, not buy",
        "messages": [
            "Hello, yes I was looking for a place.",
            "Actually I want to rent, not buy. Do you have rentals?",
            "Oh okay, a 1 BHK in Bangalore for rent.",
            "Sure, WhatsApp me the options.",
        ]
    },
    {
        "name": "⚫ ALREADY BOUGHT — No longer in the market",
        "messages": [
            "Hello?",
            "Oh actually I already bought a flat last month. I'm not looking anymore.",
        ]
    },
    {
        "name": "🔶 INDECISIVE — Keeps going back and forth",
        "messages": [
            "Hi yes, I'm looking.",
            "Mumbai, but also maybe Pune. I'm not sure.",
            "2 BHK... or maybe 3 BHK. Depends on the price.",
            "Hmm I don't know, let me think about it.",
            "Okay actually, just send me both Mumbai and Pune options on WhatsApp.",
        ]
    },
]

# ═══════════════════════════════════════════════════════════
# 🏃 TEST RUNNER
# ═══════════════════════════════════════════════════════════

def run_scenario(db, lead, scenario):
    call_id = str(uuid.uuid4())
    call = Call(id=call_id, lead_id=str(lead.id), direction="OUTBOUND", status="IN_PROGRESS", duration_seconds=0)
    db.add(call)
    db.commit()
    db.refresh(call)

    print(f"\n{'='*60}")
    print(f"  {scenario['name']}")
    print(f"{'='*60}")

    for msg in scenario["messages"]:
        print(f"\n  Customer: {msg}")
        try:
            request = AIChatRequest(
                lead_id=str(lead.id),
                call_id=call_id,
                message=msg
            )
            response = process_customer_message(db, request)
            crm_str = ""
            if response.detected_city or response.detected_bedrooms or response.detected_budget:
                parts = []
                if response.detected_city: parts.append(f"City={response.detected_city}")
                if response.detected_bedrooms: parts.append(f"Beds={response.detected_bedrooms}")
                if response.detected_budget: parts.append(f"Budget={response.detected_budget}")
                crm_str = f"\n     [CRM: {', '.join(parts)}]"
            print(f"  AI Agent: {response.reply}{crm_str}")
        except Exception as e:
            print(f"  ERROR: {e}")
            try:
                db.rollback()
            except:
                pass
        
        time.sleep(15)

    print(f"\n  {'_'*56}")
    print(f"  Scenario Complete")


def main():
    print("=" * 60)
    print("  COMPREHENSIVE AI ENGINE SCENARIO TESTER")
    print("  Testing all customer scenarios against Sales Playbook")
    print("=" * 60)

    db = SessionLocal()
    lead = db.query(Lead).first()

    if not lead:
        print("No leads found in database!")
        return

    print(f"\n  Using Lead: {lead.first_name} {lead.last_name}")
    print(f"  City: {lead.preferred_city} | Beds: {lead.bedrooms} | Budget: {lead.budget_max}")
    print(f"  Running {len(SCENARIOS)} scenarios...\n")

    results = []
    for i, scenario in enumerate(SCENARIOS[4:]):
        run_scenario(db, lead, scenario)
        results.append(scenario["name"])

    print(f"\n\n{'='*60}")
    print(f"  ALL {len(results)} SCENARIOS COMPLETED")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r}")
    print()

    db.close()

if __name__ == "__main__":
    main()
