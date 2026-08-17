import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.voice_agent import VoiceAgent

def seed():
    db = SessionLocal()
    try:
        existing = db.query(VoiceAgent).first()
        if existing:
            print("Voice Agent already exists in the database.")
            return

        print("Seeding default Voice Agent from AI Engine...")
        
        default_prompt_text = """You are a highly persuasive and friendly human sales representative for a real estate agency.
Your task is to analyze the customer's message to extract their CRM requirements AND generate your conversational reply."""

        agent = VoiceAgent(
            name="Salesforce AI Agent",
            provider="Cartesia",
            voice_id="cartesia_en_1",
            language="en-US",
            prompt=default_prompt_text,
            is_active=True,
            interruptible=True
        )
        
        db.add(agent)
        db.commit()
        print("Default Voice Agent seeded successfully! It will now appear in the UI.")
    except Exception as e:
        print(f"Error seeding voice agent: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
