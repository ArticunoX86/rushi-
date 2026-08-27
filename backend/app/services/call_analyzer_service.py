import json
import asyncio
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.call import Call
from app.models.enums import CallOutcome, CallStatus
from app.integrations.gemini.client import model
from app.models.ai_training_data import AITrainingData, TrainingCategory

async def analyze_call_async(call_id: str):
    """
    Background task to analyze a completed call, generate a summary, and extract the outcome.
    """
    db: Session = SessionLocal()
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if not call:
            print(f"Call {call_id} not found for analysis.")
            return

        # Fetch transcript
        # We need to get the conversations for this call
        conversations = call.conversations
        if not conversations:
            print(f"No conversations found for call {call_id}. Skipping analysis.")
            return

        # Sort by created_at just in case
        conversations.sort(key=lambda x: x.created_at)
        
        transcript_lines = []
        for conv in conversations:
            speaker = "AI" if conv.sender == "ai" else "Customer"
            transcript_lines.append(f"{speaker}: {conv.message}")
            
        full_transcript = "\n".join(transcript_lines)
        
        # Save transcript to call record
        call.transcript = full_transcript
        
        prompt = f"""
You are an expert sales analyst reviewing a transcript of an AI voice call with a real estate lead.
Your job is to analyze the conversation and provide a JSON response.

Here is the transcript:
{full_transcript}

Please output ONLY a raw JSON object with no markdown formatting and no backticks.
The JSON must have the following keys:
1. "summary": A concise 2-3 sentence summary of the interaction.
2. "outcome": Choose exactly ONE of the following outcomes based on the customer's intent:
   - "interested" (Customer showed positive interest in properties)
   - "not_interested" (Customer explicitly said no or was hostile)
   - "callback_requested" (Customer asked to be called back later)
   - "no_response" (Customer didn't answer or hung up immediately)
   - "converted" (Customer agreed to a meeting or site visit)
3. "learning_opportunities": A list of objects if the AI failed to handle an objection or lacked knowledge. Otherwise empty list []. Each object should have:
   - "trigger_phrase": The exact phrase or core objection the customer raised.
   - "situation_context": A brief description of the context.
   - "ideal_response": A better way the AI SHOULD have responded to this objection/question.
"""
        
        try:
            response = model.generate_content(prompt)
            cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            
            call.summary = result.get("summary")
            
            outcome_str = result.get("outcome", "").upper()
            if hasattr(CallOutcome, outcome_str):
                call.outcome = CallOutcome[outcome_str]
            else:
                call.outcome = CallOutcome.INTERESTED if outcome_str == "INTERESTED" else None
                
            print(f"Analyzed call {call_id}: {call.outcome}")

            # Auto-generate AI Training Data for learning opportunities
            learning_ops = result.get("learning_opportunities", [])
            for op in learning_ops:
                new_training = AITrainingData(
                    title=f"Auto-Learning: {op.get('trigger_phrase', 'Unknown')[:30]}",
                    category=TrainingCategory.OBJECTION_HANDLING,
                    trigger_phrase=op.get("trigger_phrase", ""),
                    situation_context=op.get("situation_context", ""),
                    ideal_response=op.get("ideal_response", ""),
                    tags=["Auto-Generated"],
                    priority=5,
                    is_active=False # Requires human approval
                )
                db.add(new_training)
                print(f"Drafted new AI Training entry: {new_training.title}")
            
        except Exception as e:
            print(f"Failed to analyze call {call_id} with Gemini: {e}")
            
        db.commit()
    except Exception as e:
        print(f"Error in analyze_call_async: {e}")
        db.rollback()
    finally:
        db.close()
