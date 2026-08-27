import json
import warnings

# Suppress all FutureWarnings (including google.generativeai deprecation)
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai

from app.core.config import settings



# ==================================================
# GEMINI CONFIGURATION
# ==================================================

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    settings.AI_MODEL
)


# ==================================================
# SAFETY SETTINGS — Block harmful content
# ==================================================

SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]


# ==================================================
# GENERATION CONFIG — Low temperature for determinism
# ==================================================

GENERATION_CONFIG = genai.types.GenerationConfig(
    temperature=settings.AI_TEMPERATURE,
    max_output_tokens=settings.AI_MAX_TOKENS,
    top_p=0.9,
    top_k=40,
)



# ==================================================
# CUSTOMER MESSAGE ANALYZER
# ==================================================

# ==================================================
# SINGLE-TURN UNIFIED ENGINE
# ==================================================
def process_conversation_turn(
    history: list[str],
    customer_message: str,
    lead_info: dict,
    whisper_hint: str = None,
    system_prompt: str = None,
    training_context: list[dict] = None,
    state_prompt: str = None,
) -> dict:
    """
    Single-turn unified AI engine.

    Parameters
    ----------
    history         : Recent conversation dialogue lines
    customer_message: Latest customer utterance
    lead_info       : CRM data for the lead (name, city, budget, etc.)
    whisper_hint    : Optional supervisor instruction to inject
    system_prompt   : Custom voice agent system prompt from DB
    training_context: List of AITrainingData dicts injected from the knowledge base.
                      Each dict should have keys: category, title, trigger_phrase,
                      situation_context, ideal_response.
    state_prompt    : Optional state-specific prompt from the call state machine.
    """
    
    default_prompt_text = """You are a highly persuasive and friendly human Real Estate Sales Person.
Your task is to analyze the customer's message to extract their CRM requirements AND generate your conversational reply."""
    
    base_instructions = system_prompt if system_prompt else default_prompt_text

    # ==================================================
    # Build Training Knowledge Base Section
    # ==================================================
    training_section = ""
    if training_context:
        lines = []
        for entry in training_context:
            cat = entry.get("category", "").replace("_", " ").title()
            title = entry.get("title", "")
            trigger = entry.get("trigger_phrase", "")
            response = entry.get("ideal_response", "")
            situation = entry.get("situation_context", "")

            if trigger:
                lines.append(f"[{cat}] WHEN: \"{trigger}\" — DO: {response}")
            else:
                lines.append(f"[{cat}] {title}: {response}")

        if lines:
            training_section = "\n### AI Knowledge Base (MUST follow these scripts):\n" + "\n".join(lines) + "\n"

    # ==================================================
    # Safety Constitution (injected into every prompt)
    # ==================================================
    safety_constitution = """
### ABSOLUTE SAFETY RULES (NEVER VIOLATE):
1. You are a HUMAN sales consultant. NEVER reveal you are an AI, bot, or machine.
2. NEVER make promises, guarantees, or price predictions.
3. NEVER give legal, financial, or tax advice.
4. NEVER fabricate properties, prices, amenities, or facts not in your context.
5. NEVER be aggressive, guilt-trip, or use high-pressure tactics.
6. NEVER discuss topics unrelated to real estate.
7. If you don't know something, say "Let me check and get back to you."
8. Keep EVERY response to 1-2 short sentences maximum.
9. NEVER use words: "AI", "bot", "algorithm", "model", "lead", "CRM", "pipeline".
"""

    prompt = f"""
{base_instructions}

{safety_constitution}

### Sales Playbook & Objection Handling:
1. **Be Persuasive but Natural:** Act like a friendly human, not a pushy robot. Never use words like "leads", "CRM", or "AI".
2. **Handle Objections:** If the customer says "not now" or tries to brush you off, DO NOT immediately give up. Acknowledge their time and offer a low-friction alternative (e.g., "I know you're busy! How about I send a quick WhatsApp with photos for later?").
3. **Pitching:** Pitch the Available Properties listed below naturally.
4. **Length:** Keep your conversational reply extremely concise and punchy (1-2 short sentences maximum).
{training_section}
{state_prompt if state_prompt else ""}

Customer Lead Info:
- Name: {lead_info.get("first_name", "there")}
- Target City: {lead_info.get("preferred_city", "Flexible")}
- Budget Limit: {lead_info.get("budget_max", "Flexible")}
- BHK Target: {lead_info.get("bedrooms", "Flexible")}

Available Properties to Pitch:
- {", ".join(lead_info.get("recommended_properties", [])) if lead_info.get("recommended_properties") else "No exact matches in system right now."}

Recent Dialogue History:
{chr(10).join(history[-5:])}

Customer's Message: "{customer_message}"

{chr(10) + f'[SUPERVISOR INSTRUCTION]: {whisper_hint}' + chr(10) + 'You MUST naturally incorporate this supervisor hint into your response.' if whisper_hint else ""}

You must return ONLY a raw JSON object with no markdown formatting.
{{
  "crm_update": {{
    "city": null,
    "budget": null,
    "bedrooms": null,
    "intent": "UNKNOWN",
    "summary": "Short summary of their needs"
  }},
  "conversational_reply": "Your 1-2 sentence response here"
}}
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
        )
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except Exception as e:
        print("Gemini voice response error:", e)
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