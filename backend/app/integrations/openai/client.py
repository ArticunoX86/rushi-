import json
from openai import OpenAI
from app.core.config import settings

# ==================================================
# OPENAI CLIENT CONFIGURATION
# ==================================================
try:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
except Exception as e:
    print("Warning: OpenAI API Key not configured correctly.", e)
    client = None

# ==================================================
# UNIFIED CONVERSATION ENGINE (OpenAI)
# ==================================================
def process_conversation_turn(
    history: list[str],
    customer_message: str,
    lead_info: dict,
    whisper_hint: str = None,
) -> dict:
    if not client:
        return _fallback_response(history, lead_info)

    system_prompt = f"""
You are a highly persuasive and friendly human sales representative for a real estate agency.
Your task is to analyze the customer's message to extract their CRM requirements AND generate your conversational reply.

### Sales Playbook & Objection Handling:
1. **Be Persuasive but Natural:** Act like a friendly human, not a pushy robot. Never use words like "leads", "CRM", or "AI".
2. **Handle Objections:** If the customer says "not now" or tries to brush you off, DO NOT immediately give up. Acknowledge their time and offer a low-friction alternative (e.g., "I know you're busy! How about I send a quick WhatsApp with photos for later?").
3. **Pitching:** Pitch the Available Properties listed below naturally.
4. **Length:** Keep your conversational reply extremely concise and punchy (1-2 short sentences maximum).

Customer Lead Info:
- Name: {lead_info.get("first_name", "there")}
- Target City: {lead_info.get("preferred_city", "Flexible")}
- Budget Limit: {lead_info.get("budget_max", "Flexible")}
- BHK Target: {lead_info.get("bedrooms", "Flexible")}

Available Properties to Pitch:
- {", ".join(lead_info.get("recommended_properties", [])) if lead_info.get("recommended_properties") else "No exact matches in system right now."}

{chr(10) + f'[SUPERVISOR INSTRUCTION]: {whisper_hint}' + chr(10) + 'You MUST naturally incorporate this supervisor hint into your response.' if whisper_hint else ""}

You must return ONLY a raw JSON object matching this schema perfectly:
{{
  "crm_update": {{
    "city": "Extracted city or null",
    "budget": "Extracted budget or null",
    "bedrooms": "Extracted BHK or null",
    "intent": "UNKNOWN",
    "summary": "Short summary of their needs"
  }},
  "conversational_reply": "Your 1-2 sentence response here"
}}
"""

    messages = [{"role": "system", "content": system_prompt.strip()}]
    
    # Inject recent history
    for line in history[-6:]:
        if line.startswith("Customer:"):
            messages.append({"role": "user", "content": line.replace("Customer: ", "")})
        elif line.startswith("AI:"):
            messages.append({"role": "assistant", "content": line.replace("AI: ", "")})
            
    # Append current message
    messages.append({"role": "user", "content": customer_message})

    try:
        response = client.chat.completions.create(
            model=settings.AI_MODEL,  # e.g., "gpt-4o-mini"
            messages=messages,
            response_format={"type": "json_object"},
            temperature=settings.AI_TEMPERATURE,
            max_tokens=settings.AI_MAX_TOKENS,
        )
        
        reply_json = response.choices[0].message.content
        return json.loads(reply_json)
        
    except Exception as e:
        print("OpenAI voice response error:", e)
        return _fallback_response(history, lead_info)


def _fallback_response(history: list[str], lead_info: dict) -> dict:
    recent_history = " ".join(history).lower() if history else ""
    if "whatsapp" in recent_history:
        fallback_reply = "Alright, I'll send those details over shortly. Have a great day!"
    elif "schedule a visit" in recent_history or "great option" in recent_history:
        fallback_reply = "No worries at all! I know you're busy. Can I send you some quick details on WhatsApp for later?"
    else:
        props = lead_info.get("recommended_properties", [])
        fallback_reply = f"I actually have a great option right now! {props[0]}. Would you like to schedule a visit?" if props else "I hear you. Give me just a second to pull up some options for you."
        
    return {
        "crm_update": {},
        "conversational_reply": fallback_reply
    }
