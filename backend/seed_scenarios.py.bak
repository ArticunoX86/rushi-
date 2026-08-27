import os
import sys

# Add backend directory to sys.path
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
                "title": "Wrong Person Objection",
                "category": TrainingCategory.OBJECTION_HANDLING,
                "trigger_phrase": "wrong number, wrong person, not prathamesh",
                "situation_context": "Customer says we called the wrong person",
                "ideal_response": "I am so sorry about that! It seems we had the wrong number in our records. I won't bother you further. Have a great day ahead!",
                "tags": ["wrong_number", "wrong_person"],
                "priority": 9,
            },
            {
                "title": "Bad Connection Objection",
                "category": TrainingCategory.OBJECTION_HANDLING,
                "trigger_phrase": "breaking, bad connection, can't hear, network",
                "situation_context": "Customer can't hear due to bad network",
                "ideal_response": "I am sorry for the bad connection! I'll quickly send the property details on WhatsApp so you don't miss out. Does that work?",
                "tags": ["bad_connection", "voice_breaking", "whatsapp_follow_up"],
                "priority": 9,
            },
            {
                "title": "Suspicious / Scam Objection",
                "category": TrainingCategory.OBJECTION_HANDLING,
                "trigger_phrase": "scam, trust, real, how do i know",
                "situation_context": "Customer is suspicious and thinks it's a scam",
                "ideal_response": "I completely understand your concern! We are a RERA registered developer. I'd be happy to send our official brochure and RERA registration details right now on WhatsApp for you to verify.",
                "tags": ["scam", "suspicious", "trust"],
                "priority": 9,
            },
            {
                "title": "Specific Requirement - Ground Floor",
                "category": TrainingCategory.FAQ,
                "trigger_phrase": "ground floor, bad knees, elderly",
                "situation_context": "Customer needs ground floor for specific reasons",
                "ideal_response": "We definitely have ground floor units available specifically designed for easy accessibility! They come with private garden spaces too. Should I send you the layout?",
                "tags": ["ground_floor", "accessibility"],
                "priority": 8,
            },
            {
                "title": "Investor Playbook",
                "category": TrainingCategory.SALES_PLAYBOOK,
                "trigger_phrase": "invest, investor, rental, roi",
                "situation_context": "Customer is an investor looking for ROI",
                "ideal_response": "For investors, this is a prime opportunity! The area has a 6-7% rental yield and property values are appreciating fast due to the upcoming metro. We have premium commercial and residential units. Would you prefer pre-leased commercial spaces or residential?",
                "tags": ["investor", "roi", "rental_yield"],
                "priority": 8,
            }
        ]
        
        seeded = 0
        for entry_data in entries:
            if entry_data["title"] not in existing_titles:
                crud.create(db, AITrainingDataCreate(**entry_data))
                seeded += 1
            
        print(f"Successfully seeded {seeded} scenario training entries!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_scenarios()
