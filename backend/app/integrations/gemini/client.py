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
# CUSTOMER MESSAGE ANALYZER
# ==================================================

def analyze_customer_message(
    message: str,
):

    prompt = f"""
You are an AI real estate calling assistant.

Your job is to understand customer property requirements
from a phone conversation.


Customer Message:

"{message}"


Extract information and return ONLY valid JSON.


Required JSON format:


{{
    "city": null,
    "locality": null,
    "budget": null,
    "bedrooms": null,
    "property_type": null,
    "intent": null,
    "sentiment": null,
    "summary": null
}}


Extraction Rules:

1. Convert budget into INR integer.

Examples:

"1.5 crore"
=
15000000


"80 lakh"
=
8000000



2. Extract bedrooms:

"3BHK"
=
3



3. Understand:

- English
- Hindi
- Hinglish



Intent options:

BUY_PROPERTY
RENT_PROPERTY
CALLBACK
NOT_INTERESTED
UNKNOWN



Sentiment options:

HOT
WARM
COLD



Return only JSON.
No explanation.
No markdown.

"""


    # ==================================================
    # GEMINI API CALL
    # ==================================================

    try:

        response = model.generate_content(prompt)

        cleaned_response = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned_response)


    # ==================================================
    # FALLBACK IF GEMINI FAILS
    # ==================================================

    except Exception as e:

        print("Gemini Error:", e)

        return {

            "city": None,

            "locality": None,

            "budget": None,

            "bedrooms": None,

            "property_type": None,

            "intent": "UNKNOWN",

            "sentiment": "COLD",

            "summary": (
                "AI analysis unavailable"
            ),

        }


# ==================================================
# CONVERSATIONAL VOICE REPLY GENERATOR (WITH WHISPERS)
# ==================================================

def generate_conversational_reply(
    history: list[str],
    customer_message: str,
    lead_info: dict,
    whisper_hint: str = None,
) -> str:
    system_prompt = f"""
You are an expert AI real estate sales calling assistant pitch agent.
Keep your responses conversational, natural, friendly, and very concise (1-2 short sentences maximum since it's a voice phone call).

Customer Lead Info:
- Name: {lead_info.get("first_name", "there")}
- Target City: {lead_info.get("preferred_city", "Mumbai")}
- Budget Limit: {lead_info.get("budget_max", "Flexible")}
- BHK Target: {lead_info.get("bedrooms", "Flexible")}

Recent Dialogue History:
{chr(10).join(history[-5:])}

Customer's Message: "{customer_message}"
"""

    if whisper_hint:
        system_prompt += f"\n[SUPERVISOR INSTRUCTION]: {whisper_hint}\nYou MUST naturally incorporate this supervisor hint or offer into your response as if it was your own idea."

    try:
        response = model.generate_content(system_prompt)
        return response.text.strip().replace('"', '')
    except Exception as e:
        print("Gemini voice response error:", e)
        return "I understand your requirements. Let me fetch the best real estate matches for you."