import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.integrations.gemini.client import process_conversation_turn

def run_mock_conversation():
    print("============================================================")
    print("  Testing AI Responses (Isolated Mode / No DB)")
    print("============================================================\n")

    lead_info = {
        "first_name": "Rohan",
        "preferred_city": "Mumbai",
        "budget_max": 10000000.0,
        "bedrooms": 2,
        "recommended_properties": []
    }

    # Mock Training Context (Objection Handling injected by RAG)
    training_context = [
        {
            "category": "OBJECTION_HANDLING",
            "title": "Too Expensive / Budget Objection",
            "trigger_phrase": "too expensive",
            "situation_context": "Customer says property is out of budget",
            "ideal_response": "I completely hear you! The good news is this project offers flexible EMI options starting from just Rs 25,000/month. Would that make it more comfortable?"
        },
        {
            "category": "PERSONA_RULE",
            "title": "Always speak like a human friend",
            "trigger_phrase": "",
            "situation_context": "Always applies",
            "ideal_response": "Keep every response to 1-2 sentences maximum. Be direct and conversational. Address the customer by name."
        },
        {
            "category": "PRODUCT_KNOWLEDGE",
            "title": "Amenities & Lifestyle Pitch",
            "trigger_phrase": "amenities",
            "situation_context": "Customer asks about amenities",
            "ideal_response": "The project has world-class amenities — a fully equipped gym, swimming pool, clubhouse, and 24/7 security. It's really designed for a premium lifestyle. Would you like me to send the full list?"
        },
        {
            "category": "FAQ",
            "title": "FAQ: Site Visit",
            "trigger_phrase": "can I visit",
            "situation_context": "Customer asks about visiting the site",
            "ideal_response": "Absolutely, we'd love to have you visit! Site visits are available Monday to Saturday, 10 AM to 6 PM. Which day works best for you?"
        },
        {
            "category": "SALES_PLAYBOOK",
            "title": "Property Pitch Script",
            "trigger_phrase": "tell me more",
            "situation_context": "Customer asks about available properties",
            "ideal_response": "I have a fantastic option for you! A 2 BHK at just 1 Crore. It comes with premium amenities and is just 10 mins from the station. Shall I send you the floor plan?"
        },
        {
            "category": "SALES_PLAYBOOK",
            "title": "Opening Call Script",
            "trigger_phrase": "",
            "situation_context": "The very beginning of a call, before any context is established",
            "ideal_response": "Hi Rohan, this is your Real Estate Sales Person from [Company Name]. I hope I caught you at a good time! I'm reaching out because we have some really exciting property options in Mumbai that I thought you'd love. Could I take just 2 minutes to share one that might be perfect for you?"
        },
        {
            "category": "OBJECTION_HANDLING",
            "title": "Call Me Later / Busy Objection",
            "trigger_phrase": "busy, call later",
            "situation_context": "Customer is busy",
            "ideal_response": "Of course, no problem at all! When would be a good time to reconnect — would tomorrow morning or evening work better for you?"
        }
    ]

    scenarios = [
        {
            "name": "OUTBOUND SCENARIO 1: Opening & Busy Objection",
            "messages": [
                "Hello?",
                "I'm actually quite busy right now, can you call me later?",
                "Tomorrow morning is fine."
            ]
        },
        {
            "name": "OUTBOUND SCENARIO 2: Opening & Immediate Interest",
            "messages": [
                "Hello?",
                "Sure, I have 2 minutes. What do you have?",
                "Send me the floor plan on WhatsApp."
            ]
        }
    ]

    for scenario in scenarios:
        print(f"\n{'-'*60}")
        print(f"  {scenario['name']}")
        print(f"{'-'*60}\n")
        history = []
        for msg in scenario['messages']:
            print(f"Customer: {msg}")
            
            # Call the AI Engine
            try:
                result = process_conversation_turn(
                    history=history,
                    customer_message=msg,
                    lead_info=lead_info,
                    whisper_hint=None,
                    system_prompt="You are a highly persuasive and friendly human Real Estate Sales Person.",
                    training_context=training_context
                )
                
                ai_reply = result.get("conversational_reply", "")
                crm_update = result.get("crm_update", {})
                
                print(f"AI Agent: {ai_reply}")
                if crm_update:
                    print(f"[CRM EXTRACTED]: {crm_update}")
                    
                print("-" * 50)
                
                # Update history
                history.append(f"Customer: {msg}")
                history.append(f"AI: {ai_reply}")
                
            except Exception as e:
                print(f"Error: {e}")
                
            import time
            time.sleep(12)

if __name__ == "__main__":
    run_mock_conversation()
