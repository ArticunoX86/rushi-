import os
import sys
import uuid
import time

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.lead import Lead
from app.models.conversation import Conversation
from app.models.call import Call
from app.schemas.ai import AIChatRequest
from app.services.ai_service import process_customer_message

# ... skipping scenario definition lines which are okay ...
# We only need to edit the import lines and the run_scenario function. Wait, let me replace multiple parts using multi_replace_file_content.

SCENARIOS = [
    {
        "name": " WRONG PERSON - Customer says wrong number",
        "messages": [
            "Hello?",
            "I think you have the wrong number, my name is not Prathamesh.",
            "No, I never looked for any properties."
        ]
    },
    {
        "name": " BAD CONNECTION - Customer can't hear well",
        "messages": [
            "Hello?",
            "Hello? Your voice is breaking, I can't hear you properly.",
            "Can you just message me instead? The network is really bad."
        ]
    },
    {
        "name": "🔴 SUSPICIOUS - Customer thinks it's a scam",
        "messages": [
            "Hello?",
            "Wait, how do I know you are really from the company? Is this a scam?",
            "I don't want to share any details over the phone."
        ]
    },
    {
        "name": "🔵 SPECIFIC REQUIREMENT - Ground floor only",
        "messages": [
            "Hello?",
            "Yes I am looking, but I strictly need a ground floor apartment because of my bad knees.",
            "Budget is around 80 Lakhs in Pune. Send me what you have."
        ]
    },
    {
        "name": " INVESTOR - Looking for high ROI, not to live in",
        "messages": [
            "Yes, speaking.",
            "I'm not looking to move in. I just want to invest for rental yield.",
            "Do you have commercial properties or just residential? Budget is 2 Crores."
        ]
    }
]

def setup_test_lead(db: Session):
    lead = db.query(Lead).filter(Lead.email == "test_scenario_v2@example.com").first()
    if not lead:
        lead = Lead(
            first_name="Prathamesh",
            last_name="Test",
            email="test_scenario_v2@example.com",
            phone="+919876543211",
            preferred_city="Mumbai",
            budget_max=10000000.0,
            bedrooms=2,
            status="NEW"
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
    return lead

def run_scenario(db: Session, lead: Lead, scenario: dict):
    print(f"\n{'='*60}")
    print(f"  {scenario['name']}")
    print(f"{'='*60}")
    
    call_id = str(uuid.uuid4())
    call = Call(id=call_id, lead_id=str(lead.id), direction="OUTBOUND", status="IN_PROGRESS", duration_seconds=0)
    db.add(call)
    db.commit()
    db.refresh(call)
    
    for msg in scenario["messages"]:
        print(f"  Customer: {msg}")
        
        request = AIChatRequest(
            call_id=call_id,
            message=msg,
            lead_id=str(lead.id)
        )
        
        try:
            response = process_customer_message(db, request)
            
            db.refresh(lead)
            crm_data = []
            if lead.preferred_city: crm_data.append(f"City={lead.preferred_city}")
            if lead.bedrooms: crm_data.append(f"Beds={lead.bedrooms}")
            if lead.budget_max: crm_data.append(f"Budget={lead.budget_max}")
            
            crm_str = f"\n     [CRM: {', '.join(crm_data)}]" if crm_data else ""
            print(f"  AI Agent: {response.reply}{crm_str}")
        except Exception as e:
            print(f"  ERROR: {e}")
            try:
                db.rollback()
            except:
                pass
        
        time.sleep(1)

    print(f"  {'_'*56}")
    print(f"  Scenario Complete")

def main():
    db = SessionLocal()
    try:
        lead = setup_test_lead(db)
        
        print("\n============================================================")
        print(f"  City: {lead.preferred_city} | Beds: {lead.bedrooms} | Budget: {lead.budget_max}")
        print("============================================================")
        
        for scenario in SCENARIOS:
            # Reset lead state before each scenario
            lead.preferred_city = "Mumbai"
            lead.bedrooms = 2
            lead.budget_max = 10000000.0
            db.commit()
            
            run_scenario(db, lead, scenario)
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
