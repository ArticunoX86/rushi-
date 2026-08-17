import sys
import os
import uuid
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.schemas.ai import AIChatRequest
from app.services.ai_service import process_customer_message
from app.models.lead import Lead

def test_engine_locally():
    print("======================================================")
    print("🤖 Local AI Engine Test (Calling python service directly)")
    print("======================================================\n")
    
    db = SessionLocal()
    
    # Check for a lead, if none exists, create a dummy one
    lead = db.query(Lead).first()
    if not lead:
        print("Creating a temporary dummy lead for testing...")
        lead = Lead(
            id=uuid.uuid4(),
            first_name="Test",
            last_name="Customer",
            phone="+919000000000",
            preferred_city="Mumbai",
            budget_max="1.5 Crore",
            bedrooms="2 BHK"
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
    lead_id = lead.id
    call_id = uuid.uuid4()
    
    print(f"✅ Using Lead: {lead.first_name} {lead.last_name} (ID: {lead_id})")
    print(f"✅ Active Call ID: {call_id}\n")
    
    messages = [
        "Hello, who is this?",
        "Yeah, I'm looking for something in Mumbai.",
        "Um, I need a 2 BHK apartment.",
        "Around 1 crore, maybe a bit more.",
        "Oh nice, that sounds interesting! When can I see it?",
        "Saturday afternoon works for me.",
    ]
    
    for msg in messages:
        print(f"👨 Customer: {msg}")
        
        request = AIChatRequest(
            lead_id=lead_id,
            call_id=call_id,
            message=msg
        )
        
        try:
            response = process_customer_message(db, request)
            print(f"🤖 AI Agent: {response.reply}")
            if response.detected_city or response.detected_bedrooms or response.detected_budget:
                print(f"   [CRM Extracted]: City={response.detected_city}, Beds={response.detected_bedrooms}, Budget={response.detected_budget}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            import traceback
            traceback.print_exc()
            break
            
        print()
        
    db.close()

if __name__ == "__main__":
    test_engine_locally()
