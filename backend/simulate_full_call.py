import os
import sys
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.services.ai_service import process_customer_message
from app.schemas.ai import AIChatRequest
from app.crud.lead import get_lead

def run_simulation():
    db = SessionLocal()
    
    # Use existing test lead or create one
    test_email = "full_call_test@example.com"
    from app.models.lead import Lead
    lead = db.query(Lead).filter(Lead.email == test_email).first()
    if not lead:
        lead = Lead(
            first_name="John",
            last_name="Doe",
            email=test_email,
            phone="+919876543210"
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)

    call_id = uuid.uuid4()
    print("==========================================================")
    print("📞 INITIATING FULL SIMULATED CALL (ULTRA-REALISTIC HUMAN)")
    print("==========================================================")
    
    conversation = [
        "Hello? Who is this?",
        "Oh, wait, are you a real person or a bot? Sounds like a robot.",
        "Ah okay, gotcha. Yeah I was looking at some apartments.",
        "I'm mostly looking for a 3 BHK in Mumbai, budget is around 1.5 Crores.",
        "Actually, what are the exact legal fees and stamp duty costs?",
        "Alright, sounds good. Sure, send me the details on WhatsApp.",
    ]
    
    for turn, msg in enumerate(conversation):
        print(f"\n👨 Customer: {msg}")
        
        req = AIChatRequest(
            lead_id=lead.id,
            call_id=call_id,
            message=msg
        )
        
        response = process_customer_message(db, req)
        
        print(f"🤖 AI Agent:  {response.reply}")
        if response.detected_city or response.detected_bedrooms or response.detected_budget:
            crm = []
            if response.detected_city: crm.append(f"City: {response.detected_city}")
            if response.detected_bedrooms: crm.append(f"Beds: {response.detected_bedrooms}")
            if response.detected_budget: crm.append(f"Budget: {response.detected_budget}")
            print(f"   [CRM Extracted]: {', '.join(crm)}")

    print("\n==========================================================")
    print("✅ CALL COMPLETED SUCCESSFULLY")
    print("==========================================================")
    db.close()

if __name__ == "__main__":
    run_simulation()
