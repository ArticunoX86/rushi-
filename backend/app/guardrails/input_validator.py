"""
Input Validator — Pre-processing guardrail for customer messages.

Runs BEFORE the customer's transcribed text reaches Gemini.
Detects prompt injection attacks and toxic/abusive content.
"""

import re
from dataclasses import dataclass, field
from app.core.config import settings


# ==================================================
# VALIDATION RESULT
# ==================================================

@dataclass
class InputValidationResult:
    """Result of input validation check."""
    is_safe: bool = True
    reason: str = ""
    sanitized_text: str = ""
    violation_type: str = ""  # "prompt_injection" | "toxic_content" | ""


# ==================================================
# PROMPT INJECTION PATTERNS
# ==================================================

PROMPT_INJECTION_PATTERNS = [
    # Direct instruction override attempts
    r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|directions?)",
    r"disregard\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|directions?)",
    r"forget\s+(everything|all|your)\s*(instructions?|prompts?|rules?|training)?",
    r"you\s+are\s+now\s+(a|an|my)\s+",
    r"act\s+as\s+(if\s+you\s+are|a|an|my)\s+",
    r"pretend\s+(to\s+be|you\s+are|that)\s+",
    r"new\s+(instructions?|rules?|prompt)\s*[:=]",
    r"system\s*prompt\s*[:=]",
    r"override\s+(your|the|all)\s+(instructions?|rules?|settings?|prompt)",

    # Roleplay / jailbreak patterns
    r"do\s+anything\s+now",
    r"DAN\s+mode",
    r"developer\s+mode",
    r"jailbreak",
    r"bypass\s+(your|the|all)\s+(filters?|restrictions?|safety|guardrails?)",
    r"(remove|disable|turn\s+off)\s+(your|the|all)\s+(filters?|restrictions?|safety|limits?)",

    # Data exfiltration attempts
    r"(what|tell\s+me|show|reveal|repeat|display)\s+(is\s+)?(your|the)\s+(system\s+)?prompt",
    r"(what|tell\s+me|show|reveal)\s+(are\s+)?(your|the)\s+(instructions?|rules?|guidelines?)",
    r"(print|output|display|show)\s+(your|the)\s+(system\s+)?(message|prompt|instructions?)",
]

# Pre-compile for performance
_INJECTION_REGEX = [
    re.compile(pattern, re.IGNORECASE) for pattern in PROMPT_INJECTION_PATTERNS
]


# ==================================================
# TOXIC CONTENT PATTERNS
# ==================================================

TOXIC_KEYWORDS = [
    # Threats
    "kill you", "murder", "bomb", "terrorist", "shoot you",
    "blow up", "i will hurt", "i will find you",
    # Extreme profanity (subset — extend as needed)
    "motherfucker", "fuck you", "piece of shit",
    # Harassment
    "you're stupid", "you idiot", "dumb bot", "useless machine",
]

_TOXIC_REGEX = [
    re.compile(re.escape(keyword), re.IGNORECASE) for keyword in TOXIC_KEYWORDS
]


# ==================================================
# VALIDATION FUNCTION
# ==================================================

def validate_input(customer_message: str) -> InputValidationResult:
    """
    Validate customer input before it reaches the LLM.

    Returns an InputValidationResult indicating whether the message is safe,
    and a sanitized version if needed.
    """

    if not settings.AI_ENABLE_INPUT_GUARDRAILS:
        return InputValidationResult(
            is_safe=True,
            sanitized_text=customer_message,
        )

    # Empty or very short messages are safe
    if not customer_message or len(customer_message.strip()) < 2:
        return InputValidationResult(
            is_safe=True,
            sanitized_text=customer_message or "",
        )

    # -------------------------------------------
    # CHECK 1: Prompt Injection Detection
    # -------------------------------------------
    for pattern in _INJECTION_REGEX:
        if pattern.search(customer_message):
            return InputValidationResult(
                is_safe=False,
                reason=f"Prompt injection detected: matched pattern '{pattern.pattern}'",
                sanitized_text="[Message blocked by safety filter]",
                violation_type="prompt_injection",
            )

    # -------------------------------------------
    # CHECK 2: Toxic Content Detection
    # -------------------------------------------
    for pattern in _TOXIC_REGEX:
        if pattern.search(customer_message):
            return InputValidationResult(
                is_safe=False,
                reason=f"Toxic content detected: '{pattern.pattern}'",
                sanitized_text="[Message blocked by safety filter]",
                violation_type="toxic_content",
            )

    # -------------------------------------------
    # CHECK 3: Abnormally long messages (possible attack)
    # -------------------------------------------
    if len(customer_message) > 2000:
        return InputValidationResult(
            is_safe=False,
            reason=f"Message too long ({len(customer_message)} chars). Possible attack vector.",
            sanitized_text=customer_message[:500] + "...",
            violation_type="excessive_length",
        )

    # Message passed all checks
    return InputValidationResult(
        is_safe=True,
        sanitized_text=customer_message,
    )
