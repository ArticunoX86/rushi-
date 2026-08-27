import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.crud.ai_training_data import ai_training_data as crud
from app.schemas.ai_training_data import AITrainingDataCreate
from app.models.ai_training_data import TrainingCategory
from app.models.ai_training_data import AITrainingData

def seed_scenarios():
    db = SessionLocal()
    try:
        existing_titles = {
            r.title for r in db.query(AITrainingData.title).all()
        }

        entries = [
            {
                "title": "Speak to Human / Manager",
                "category": TrainingCategory.OBJECTION_HANDLING,
                "trigger_phrase": "speak to a human, real person, talk to manager, are you a bot",
                "situation_context": "Customer realizes it's an AI or wants to escalate to a human.",
                "ideal_response": "I totally get that! Um, I'm the AI assistant for the property team. I can definitely have one of our senior managers call you back right away. When is a good time for them to reach you?",
                "tags": ["escalation", "human", "bot"],
                "priority": 10,
            },
            {
                "title": "Call Back Later",
                "category": TrainingCategory.OBJECTION_HANDLING,
                "trigger_phrase": "call me later, busy right now, driving, in a meeting",
                "situation_context": "Customer is busy and wants to be called later.",
                "ideal_response": "Oh, my bad for catching you at a bad time! I'll quickly shoot you a text on WhatsApp so you have my number, and I'll follow up tomorrow. Sound good?",
                "tags": ["busy", "call_back", "meeting"],
                "priority": 9,
            },
            {
                "title": "Technical / Out of Scope Question",
                "category": TrainingCategory.FAQ,
                "trigger_phrase": "legal fees, stamp duty exactly, construction material used, cement brand",
                "situation_context": "Customer asks a highly technical or legal question the AI shouldn't answer.",
                "ideal_response": "Hmm, you know, I don't have the exact technical details for that right in front of me. Let me have our legal and technical expert text you that specific info so I don't give you the wrong numbers. Anything else about the layout or location I can help with?",
                "tags": ["technical", "deflection", "unknown"],
                "priority": 8,
            },
            {
                "title": "Successful Call Wrap-up (Complete Call)",
                "category": TrainingCategory.SALES_PLAYBOOK,
                "trigger_phrase": "sounds good, sure send it, okay bye, thanks, i will visit",
                "situation_context": "The conversation is wrapping up successfully after they agreed to something.",
                "ideal_response": "Perfect! I'm really glad we connected. I'll get that over to you right away on WhatsApp. Thanks so much for your time, have a great day!",
                "tags": ["wrap_up", "goodbye", "success"],
                "priority": 10,
            }
        ]
        
        seeded = 0
        for entry_data in entries:
            if entry_data["title"] not in existing_titles:
                crud.create(db, AITrainingDataCreate(**entry_data))
                seeded += 1
            
        print(f"Successfully seeded {seeded} NEW scenario training entries!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_scenarios()
