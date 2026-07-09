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