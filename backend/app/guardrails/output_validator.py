"""
Output Validator — Post-processing guardrail for AI responses.

Runs AFTER Gemini generates a reply, BEFORE it's sent to ElevenLabs TTS.
Checks for banned phrases, excessive length, and off-topic content.
"""

import re
from dataclasses import dataclass
from app.core.config import settings


# ==================================================
# VALIDATION RESULT
# ==================================================

@dataclass
class OutputValidationResult:
    """Result of output validation check."""
    is_safe: bool = True
    reason: str = ""
    original_text: str = ""
    safe_text: str = ""
    violation_type: str = ""  # "banned_phrase" | "excessive_length" | "off_topic" | ""


# ==================================================
# BANNED PHRASES
# ==================================================

BANNED_PHRASES = [
    # False promises / guarantees
    r"i\s+promise",
    r"i\s+guarantee",
    r"100\s*%\s*(guarantee|sure|certain|return|appreciation)",
    r"guaranteed\s+(returns?|profit|appreciation|value)",
    r"you\s+will\s+definitely",
    r"absolutely\s+certain",
    r"no\s+risk\s+(at\s+all|whatsoever|involved)",
    r"money\s+back\s+guarantee",
    r"double\s+your\s+(money|investment)",
    r"zero\s+risk",

    # Legal / financial advice the AI must NOT give
    r"(this\s+is\s+)?legal\s+advice",
    r"(this\s+is\s+)?financial\s+advice",
    r"tax\s+(benefit|deduction|saving)s?\s+(you\s+will|you'll)\s+get",
    r"i\s+am\s+(a|your)\s+(lawyer|advocate|financial\s+advisor|chartered\s+accountant)",

    # Identity disclosure
    r"i\s+am\s+(an?\s+)?(artificial\s+intelligence|AI|bot|robot|machine|language\s+model|LLM)",
    r"i('m|\s+am)\s+not\s+(a\s+)?human",
    r"(as\s+)?an\s+AI(\s+model|\s+assistant)?",
    r"i\s+don'?t\s+have\s+(feelings|emotions|a\s+body)",

    # Aggressive / pressuring language
    r"you('re|\s+are)\s+(making\s+a\s+)?big\s+mistake",
    r"you('ll|\s+will)\s+regret",
    r"this\s+is\s+your\s+last\s+chance",
    r"(don'?t|do\s+not)\s+be\s+(stupid|foolish|an?\s+idiot)",
    r"everyone\s+(else\s+)?is\s+buying",
    r"you('re|\s+are)\s+missing\s+out",

    # Real estate specific banned phrases
    r"guaranteed\s+(rental|ROI|return\s+on\s+investment)",
    r"prices?\s+(will\s+)?(definitely|surely|certainly)\s+(go\s+up|increase|double|triple)",
    r"(this|the)\s+area\s+will\s+definitely\s+develop",
]

_BANNED_REGEX = [
    re.compile(pattern, re.IGNORECASE) for pattern in BANNED_PHRASES
]


# ==================================================
# OFF-TOPIC INDICATORS
# ==================================================

OFF_TOPIC_PATTERNS = [
    r"(here'?s?\s+)?(a\s+)?recipe\s+for",
    r"(let\s+me\s+)?write\s+(you\s+)?(a\s+)?(poem|song|story|code|essay)",
    r"(here'?s?\s+)?how\s+to\s+(hack|break\s+into|steal)",
    r"(the\s+meaning\s+of\s+life|meaning\s+of\s+existence)",
    r"(let'?s?\s+)?(talk|discuss)\s+about\s+(politics|religion|sports|movies|games)",
]

_OFF_TOPIC_REGEX = [
    re.compile(pattern, re.IGNORECASE) for pattern in OFF_TOPIC_PATTERNS
]


# ==================================================
# SAFE FALLBACK RESPONSES
# ==================================================

SAFE_FALLBACKS = {
    "banned_phrase": "I understand your concern! Let me connect you with our team who can give you all the specific details. Would that work for you?",
    "excessive_length": "That's a great question! Let me keep it simple — shall I send you a quick summary on WhatsApp with all the details?",
    "off_topic": "Ha, that's interesting! But hey, coming back to the properties — I have some really great options for you. Can I share a few?",
    "default": "I appreciate your interest! Let me check on that and get back to you with the right information.",
}


# ==================================================
# VALIDATION FUNCTION
# ==================================================

def validate_output(ai_response: str) -> OutputValidationResult:
    """
    Validate AI-generated response before it reaches TTS.

    Returns an OutputValidationResult with the original text and a safe
    replacement if the response violates any guardrails.
    """

    if not settings.AI_ENABLE_OUTPUT_GUARDRAILS:
        return OutputValidationResult(
            is_safe=True,
            original_text=ai_response,
            safe_text=ai_response,
        )

    if not ai_response:
        return OutputValidationResult(
            is_safe=True,
            original_text="",
            safe_text="I understand. Give me a moment.",
        )

    # -------------------------------------------
    # CHECK 1: Banned Phrase Detection
    # -------------------------------------------
    for pattern in _BANNED_REGEX:
        match = pattern.search(ai_response)
        if match:
            return OutputValidationResult(
                is_safe=False,
                reason=f"Banned phrase detected: '{match.group()}'",
                original_text=ai_response,
                safe_text=SAFE_FALLBACKS["banned_phrase"],
                violation_type="banned_phrase",
            )

    # -------------------------------------------
    # CHECK 2: Off-Topic Content Detection
    # -------------------------------------------
    for pattern in _OFF_TOPIC_REGEX:
        match = pattern.search(ai_response)
        if match:
            return OutputValidationResult(
                is_safe=False,
                reason=f"Off-topic content detected: '{match.group()}'",
                original_text=ai_response,
                safe_text=SAFE_FALLBACKS["off_topic"],
                violation_type="off_topic",
            )

    # -------------------------------------------
    # CHECK 3: Response Length Limiter
    # -------------------------------------------
    max_length = settings.AI_MAX_RESPONSE_LENGTH
    if len(ai_response) > max_length:
        # Try to truncate at a sentence boundary
        truncated = ai_response[:max_length]
        last_period = truncated.rfind(".")
        last_question = truncated.rfind("?")
        last_exclaim = truncated.rfind("!")
        cut_point = max(last_period, last_question, last_exclaim)

        if cut_point > max_length // 2:
            safe = truncated[:cut_point + 1]
        else:
            safe = truncated.rstrip() + "..."

        return OutputValidationResult(
            is_safe=False,
            reason=f"Response too long ({len(ai_response)} chars, max {max_length})",
            original_text=ai_response,
            safe_text=safe,
            violation_type="excessive_length",
        )

    # Response passed all checks
    return OutputValidationResult(
        is_safe=True,
        original_text=ai_response,
        safe_text=ai_response,
    )
